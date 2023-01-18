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
import lane                                             # Used to time a lane
import laneOutput                                       # Used to display lane status

lanes = [{'no':1,'input':20,'rLED':0,'gLED':0},
        {'no':2,'input':21,'rLED':0,'gLED':0},
        {'no':3,'input':22,'rLED':0,'gLED':0},
        {'no':4,'input':23,'rLED':0,'gLED':0}]

#led = RGBLED(17, 18, 19)



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
            op = laneOutput(rLED = t['rLED'], gLED = t['gLED'])
            t = lane(i['no'], i['input'], op, self.log)
            threads.append(t)


        #
        # Ensure all lanes are clear
        #
        # TODO: Implement me!

        
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
                t.setDNF(True)

        # Give the lanes the start time AFTER the race is over.
        # Doing this before could take away from processing to monitor the finish
        for t in threads:
            t.setTimeStart(start)

        # Sort lanes by time
        threads.sort(key = lambda x : x.totalTime())

        for index, t in enumerate(threads):
            self.log.info("Place: {}, Lane {}, Time: {}".format(index + 1, t.getLaneNo(), t.totalTime()))



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

