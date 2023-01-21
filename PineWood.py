#!/usr/bin/python3

from time import sleep              # Used for sleep()
import time                         # Used for timestamps

#import board                       # Used to reference pins by name on the Pi
#import digitalio                   # Used to control I/Os on the Pi

from gpiozero import Button         # Used for start sensor

import laneInput                    # Used to time a lane
import laneOutput                   # Used to display lane status

from log import *                    # Used to log what's going on


##
# Class to store/run the pinewood races
#
#
# Right now this isn't a class but a function.  Will need to be refactored
class pinewood:

    gate = None
    lanes = []                  # Lanes
    log = None

    timeout = 15


    ##
    # Constructor
    #
    #
    # @var lanes Expects array of lane data - we will construct objects
    #               This is messy and violated OOP principles - clean up
    #               Lanes should likely be it's own object
    # @var gate Expects a starting `gate` object
    #
    def __init__(self, lanes, gate, log):
        self.log = log
        self.gate = gate

        # Construct lane objects
        for lane in lanes:
            ipop = {}
            ipop['ip'] = laneInput.laneInput(lane['no'], lane['input'], self.log)
            ipop['op'] = laneOutput.laneOutput(rLED = lane['rLED'], gLED = lane['gLED'])
            self.lanes.append(ipop)
    

    ##
    #
    #
    def setTimeout(self, timeout):
        self.timeout = timeout
    

    ##
    # Main program to run
    # This is very messy and requires cleanup/refactor
    #
    def race(self):


        # Wait for starting gate to be reset
        self.gate.yellow()
        self.log.info("Waiting for starting gate to be reset.")
        self.gate.blockingReady()


        #
        # Ensure all lanes are clear
        #
        qty = len(self.lanes)
        self.log.info("Waiting for {} lanes to be ready".format(qty))
        ready = 0
        self.gate.red()
        while ready < qty:
            ready = 0
            time.sleep(1)
            for lane in self.lanes:
                lane['op'].displayReady(lane['ip'])
                if(lane['ip'].isReady()):
                    self.log.debug("Lane {} ready".format(lane['ip'].getLaneNo()))
                    ready += 1
        self.gate.green()


        # Await starting gate
        self.log.info("Waiting starting gate to open.")
        self.gate.blockingStart()


        # Get the starting timestamp (as seconds)
        start = time.time()
        self.gate.yellow()

        # Start all threads.  This can happen after the starting gate because:
        # A - we don't want a false-positive before the start
        # B - spinning up the threads will easily happen in a few MS
        # C - spinup delay isn't critical to functionality
        self.log.info("Starting race at {}".format(start))
        for t in self.lanes:
            t['ip'].daemon = True
            t['ip'].start()
        

        # Wait until the timeout has lapsed or all threads are dead
        alive = True
        while (start + self.timeout > time.time() and alive):
            # Check if threads are still alive or not
            # We should do an `is_alive()`` on all threads in case a car DNF and `join()` doesn't return
            alive = False
            for t in self.lanes:
                if t['ip'].is_alive():
                    alive = True
                    break   # A thread is still running - we aren't finished yet
            sleep(0.5)  # We shouldn't hog CPU with checking if children have returned
        # All threads have terminated OR we are over the timeout

        self.log.info("Race completed")
        
        # In case we have a DNF, loop threads and kill
        for t in self.lanes:
            if t['ip'].is_alive():
                self.log.info("Lane {} DNF".format(t['ip'].getLaneNo()))
                t['ip'].stop()

        # Give the lanes the start time AFTER the race is over.
        # Doing this before could take away from processing to monitor the finish
        for t in self.lanes:
            t['ip'].setTimeStart(start)

        # Sort lanes by time
        self.lanes.sort(key = lambda x : x['ip'].totalTime())

        for index, t in enumerate(self.lanes):
            place = index + 1
            t['ip'].setPlace(place)
            place = t['ip'].getPlace()      # getPlace will take DNF into account
            self.log.info("Place: {}, Lane {}, Time: {}".format(place, t['ip'].getLaneNo(), t['ip'].totalTime()))
            t['op'].showPlace(place)
