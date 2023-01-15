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

    timeStart = 0
    timeStop = 0
    timeTotal = 0

    ##
    # Constructor
    #
    def __init__(self, laneNo, laneInput, *args, **kwargs):
        super(lane,self).__init__(*args, **kwargs)
        self.laneNo = laneNo
        self.laneInput = laneInput
        self.DID = DigitalInputDevice(self.laneInput, True)
    
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
    
    def run(self):
        while(self.DID.value == 1):
            # Poll the sensor super-fast
            pass
        # As soon as the sensor trips, log the time and return
        self.timeStop = time.time()
    
    def setTimeStart(self, time):
        self.timeStart = time
    
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


    ##
    # Constructor
    #
    def __init__(self, lanes):
        self.log = log()
        # DEBUG:
        self.log.setDisplayLevel('TRACE')
        self.lanes = lanes
    

    ##
    # Main program to run
    # This is messy and will likely require cleanup/refactor
    #
    def run(self):

        # Get the starting timestamp (as seconds)
        start = time.time()
        timeout = 15

        # Construct threads from lanes
        threads = []

        for i in self.lanes:
            t = lane(i['no'], i['input'])
            threads.append(t)

        # Start all threads
        for t in threads:
            t.start()
        
        while start + timeout > time.time():
            alive = 0
            # Check if threads are still alive or not
            # We should do an `is_alive()`` on all threads in case a car DNF and `join()` doesn't return
            for t in threads:
                if t.is_alive():
                    break   # A thread is still running - we aren't finished yet
            sleep(0.5)  # We shouldn't hog CPU with checking if children have returned
        # All threads have terminated OR we are over the timeout

        for t in threads:
            if t.is_alive():
                t.kill()

        # Give the lanes the start time AFTER the race is over.
        # Doing this before could take away from processing to monitor the finish
        for t in threads:
            t.setTimeStart(start)

        # Sort lanes by time
        threads.sort(key = lambda x : x.totalTime())



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

