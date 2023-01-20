#!/usr/bin/python3


import laneOutputDisplayReady


##
# Class to display lane status
# We *JUST* display a status here - other classes check the status and request we display
#
class laneOutput:

    lane = None
    redLED = None
    greenLED = None


    ##
    # Constructor
    #
    def __init__(self, lane, rLED, gLED):
        self.lane = lane
        self.redLED = rLED
        self.greenLED = gLED
    

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
    def showPlace(place = None):
        # First = Green
        # Second = Yellow (Green/Red)
        # Third = Red
        # Fourth = Off
        if (place):
            pass
        else:
            self.lane.getPlace()
        pass


    ##
    # Displays whether the lane is ready to race or not.
    #
    def displayReady(self):
        self.laneOPDisplayReady = laneOutputDisplayReady()

        pass
