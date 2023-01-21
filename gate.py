#!/usr/bin/python3


class gate:

    ##
    #
    # @var sBtn Expects Button object
    # @var rgLED Expects rgLED object
    def __init__(self, sBtn, rgLED):
        self.start = sBtn
        self.rgLED = rgLED


    ##
    # Block until the start gate is OPEN/RACING
    #
    def blockingStart(self):
        self.start.wait_for_release()

    ##
    # Block until the start gate is CLOSED
    #
    def blockingReady(self):
        self.start.wait_for_press()

    ##
    # Return the status of the starting gate
    #
    # @return Boolean True if the gate is closed/blocking, False if the gate is open
    def gateStatus(self):
        return self.start.is_pressed()
    

    ##
    # Set colors on the starting LED
    # This is poor design - refactor
    #
    def off(self):
        self.rgLED.off()

    def red(self):
        self.rgLED.red()

    def yellow(self):
        self.rgLED.yellow()

    def green(self):
        self.rgLED.green()
