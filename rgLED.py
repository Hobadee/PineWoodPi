#!/usr/bin/python3


from gpiozero import PWMLED


class rgLED:

    # Yellow = Red=100, Green=40

    def __init__(self, rLED, gLED):
        self.rLED = PWMLED(rLED)
        self.gLED = PWMLED(gLED)

    
    ##
    # Methods to set static colors
    #
    def off(self):
        self.rLED.value = 0.0
        self.gLED.value = 0.0

    def red(self):
        self.rLED.value = 1.0
        self.gLED.value = 0.0
    
    def yellow(self):
        # Yellow = Red=100, Green=40
        self.rLED.value = 1.0
        self.gLED.value = 0.4
    
    def green(self):
        self.rLED.value = 0.0
        self.gLED.value = 0.4
