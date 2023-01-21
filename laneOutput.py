#!/usr/bin/python3


import laneOutputDisplayReady
from gpiozero import PWMLED

##
# Class to display lane status
# We *JUST* display a status here - other classes check the status and request we display
#
class laneOutput:

    redLED = None
    greenLED = None


    ##
    # Constructor
    #
    # We should change r/g LEDs to rgLED object
    #
    def __init__(self, rLED, gLED):
        self.redLED = PWMLED(rLED)
        self.greenLED = PWMLED(gLED)
    

    ##
    # What to show prior to the race
    #
    def showClear():
        # Red LED off
        # Green LED on
        pass
    

    ##
    # What to show when we have finished the race
    #
    def showFinish():
        # Red LED on
        # Green LED off
        pass
    

    ##
    # What to show when the race is finished and we are displaying standings
    #
    def showPlace(place = None, lane = None):
        # First = Green
        # Second = Yellow (Green/Red)
        # Third = Red
        # Fourth = Off
        if (place == None and lane == None):
            # Throw an error or some shit
            pass
        
        # If we are passed a lane, get it's place
        if (lane):
            place = lane.getPlace()
        
        # Display based off place
        if(place == 1):
            self.green()
        elif(place == 2):
            self.yellow()
        elif(place == 3):
            self.red()
        else:
            self.off()



    ##
    # Displays whether the lane is ready to race or not.
    #
    def displayReady(self, lane):
        if (lane.isReady()):
            self.green()
            return
        self.red()
    

    ##
    # Methods to set static colors
    #
    def off(self):
        self.redLED.value = 0.0
        self.greenLED.value = 0.0

    def red(self):
        self.redLED.value = 1.0
        self.greenLED.value = 0.0
    
    def yellow(self):
        # Yellow = Red=100, Green=40
        self.redLED.value = 1.0
        self.greenLED.value = 0.4
    
    def green(self):
        self.redLED.value = 0.0
        self.greenLED.value = 0.4
