#!/usr/bin/python3

import os                                               # Used for OS interaction (os.system('clear'))
from time import sleep                                  # Used for sleep()
import time                                             # Used for timestamps


import board                                            # Used to reference pins by name on the Pi
import digitalio                                        # Used to control I/Os on the Pi
import busio                                            # Used for SPI

from gpiozero import LED, RGBLED                        # Used for LEDs and RGB LEDs
from gpiozero import Button, DigitalInputDevice         # Used for button and break-beam

import laneInput                                        # Used to time a lane
import laneOutput                                       # Used to display lane status

from log import *


#led = RGBLED(17, 18, 19)



##
# Class to store/run the pinewood races
#
#
# Right now this isn't a class but a function.  Will need to be refactored
class pinewood:

    startBtn = None
    lanes = []                  # Lanes
    log = None

    timeout = 15


    ##
    # Constructor
    #
    def __init__(self, lanes, startBtn, log):
        self.log = log
        self.startBtn = Button(startBtn, True)

        # Construct lane objects
        for lane in lanes:
            ipop = {}
            ipop['op'] = laneInput.laneOutput(lane = ip, rLED = t['rLED'], gLED = t['gLED'])
            ipop['ip'] = laneInput.laneInput(lane['no'], lane['input'], ipop['op'], log = self.log)
            self.log.trace("ipop={}".format(ipop))
            self.lanes.append(ipop)

        self.log.debug(self.lanes)
    

    ##
    #
    #
    def setTimeout(self, timeout):
        self.timeout = timeout
    

    ##
    # Main program to run
    # This is messy and will likely require cleanup/refactor
    #
    def race(self):

        #
        # Ensure all lanes are clear
        #
        # TODO: Implement me!
        for lane in self.lanes:
            lane['op'].displayReady()

        
        # Await starting gate
        self.log.info("Awaiting starting gate.")
        while self.startBtn == False:
            pass

        # Get the starting timestamp (as seconds)
        start = time.time()

        # Start all threads.  This can happen after the starting gate because:
        # A - we don't want a false-positive before the start
        # B - spinning up the threads will easily happen in a few MS
        # C - spinup delay isn't critical to functionality
        self.log.info("Starting race at {}".format(start))
        for t in self.lanes:
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
                self.log.info("Lane {} DNF".format(t.getLaneNo()))
                t['ip'].stop()

        # Give the lanes the start time AFTER the race is over.
        # Doing this before could take away from processing to monitor the finish
        for t in self.lanes:
            t['ip'].setTimeStart(start)

        # Sort lanes by time
        self.lanes.sort(key = lambda x : x['ip'].totalTime())

        for index, t in enumerate(self.lanes):
            self.log.info("Place: {}, Lane {}, Time: {}".format(index + 1, t['ip'].getLaneNo(), t['ip'].totalTime()))



# General flow
#
# 1. Instantiate race loop
# 2. Start Loop
# 3. Check start button = ready
# 4. Check lanes = empty
# 5. Green light
# 6. Wait for start button = go
# 7. Take starting timestamp
# 8. Start threads to watch lanes
# 9. On lane occupied, take ending timestamp, flag finished, calculate time, return
# 10. Sort by times, return times & winner
# 11. Return to step 2
#

