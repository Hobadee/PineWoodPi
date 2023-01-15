#!/usr/bin/python3

import os                                               # Used for OS interaction (os.system('clear'))
from time import sleep                                  # Used for sleep()
import time                                             # Used for timestamps

import threading                                        # Lets us multithread

import board                                            # Used to reference pins by name on the Pi
import digitalio                                        # Used to control I/Os on the Pi
import busio                                            # Used for SPI

from gpiozero import LED, RGBLED                        # Used for LEDs and RGB LEDs
from gpiozero import Button, DigitalInputDevice         # Used for button and break-beam

from log import *

lanes = [{'no':1,'input':20},
        {'no':2,'input':21},
        {'no':3,'input':22},
        {'no':4,'input':23}]

led = RGBLED(17, 18, 19)

##
# Class to init/store lane info
#
# Right now we are definitely violating the principle of single-responsibility
#
class lane(threading.Thread):

    laneNo = None
    laneInput = None
    log = None

    timeStart = 0
    timeStop = 0
    timeTotal = 0

    run = False

    ##
    # Constructor
    #
    def __init__(self, laneNo, laneInput, log, *args, **kwargs):
        super(lane,self).__init__(*args, **kwargs)
        self.laneNo = laneNo
        self.laneInput = laneInput
        self.DID = DigitalInputDevice(self.laneInput, True)
        self.log = log
    
    ##
    # Return the status of the lane sensor
    # False - beam broken
    # True - beam active
    #
    def broken(self):
        if self.DID.value == 1:
            return False
        else:
            return True
    
    ##
    #
    #
    def run(self):
        # Flip "run" flag True
        self.run = True
        self.log.debug("Running lane {}".format(self.laneNo))
        while(self.getSensor and self.run):
            # Poll the sensor super-fast
            pass
        # As soon as the sensor trips, log the time and return
        if(self.run == True):
            self.timeStop = time.time()
            self.log.debug("Lane {} finished at {}".format(self.laneNo, self.timeStop))
    

    ##
    # Mechanism to stop the thread
    #
    def stop(self):
        self.run = False
    

    ##
    # Return the lane number
    #
    def getLaneNo(self):
        return self.laneNo
    

    ##
    # Returns if a car is sensed by the sensor or not
    #
    # True if a car is there, False otherwise
    #
    def getSensor(self):
        if(self.DID.value == 0):
            return True
        return False


    ##
    #
    #
    def setTimeStart(self, time):
        self.timeStart = time
    

    ##
    #
    #
    def totalTime(self):
        if self.timeStart == 0 or self.timeStop == 0:
            # Start or Stop haven't been set yet - puke
            return 0
        return self.timeStop - self.timeStart
        


##
# Class to store/run the pinewood races
#
#
# Right now this isn't a class but a function.  Will need to be refactored
class pinewood:

    lanes = []
    log = None

    timeout = None


    ##
    # Constructor
    #
    def __init__(self, lanes):
        self.log = log()
        # DEBUG:
        self.log.setDisplayLevel('TRACE')
        self.lanes = lanes

        self.timeout = 15
    

    ##
    # Main program to run
    # This is messy and will likely require cleanup/refactor
    #
    def race(self):

        # Construct threads from lanes
        threads = []
        for i in self.lanes:
            t = lane(i['no'], i['input'])
            threads.append(t)

        # Await starting gate
        # TODO: Implement me!
        # while startingGate == False:
        #     pass

        # Get the starting timestamp (as seconds)
        start = time.time()

        # Start all threads.  This can happen after the starting gate because:
        # A - we don't want a false-positive before the start
        # B - spinning up the threads will easily happen in a few MS
        # C - spinup delay isn't critical to functionality
        self.log.info("Starting race at {}".format(start))
        for t in threads:
            t.start()
        

        # Wait until the timeout has lapsed or all threads are dead
        alive = True
        while (start + self.timeout > time.time() and alive):
            # Check if threads are still alive or not
            # We should do an `is_alive()`` on all threads in case a car DNF and `join()` doesn't return
            alive = False
            for t in threads:
                if t.is_alive():
                    alive = True
                    break   # A thread is still running - we aren't finished yet
            sleep(0.5)  # We shouldn't hog CPU with checking if children have returned
        # All threads have terminated OR we are over the timeout

        self.log.info("Race completed")

        # In case we have a DNF, loop threads and kill
        for t in threads:
            if t.is_alive():
                self.log.info("Lane {} DNF".format(t.getLaneNo()))
                t.stop()

        # Give the lanes the start time AFTER the race is over.
        # Doing this before could take away from processing to monitor the finish
        for t in threads:
            t.setTimeStart(start)

        # Sort lanes by time
        threads.sort(key = lambda x : x.totalTime())

        for index, t in enumerate(threads):
            self.log.info("Place: {}, Lane {}".format(index, t.getLaneNo()))



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

