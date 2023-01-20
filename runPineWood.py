#!/usr/bin/python3


from PineWood import pinewood
from log import *


###################################
#          Configuration          #
###################################


# Configure start button sensor
startBtn = 1

# Configure lanes and sensors
lanes = [{'no':1,'input':4,'rLED':20,'gLED':21},
        {'no':2,'input':17,'rLED':5,'gLED':6},
        {'no':3,'input':18,'rLED':24,'gLED':25},
        {'no':4,'input':27,'rLED':22,'gLED':23}]


# Hold long should the race last before cars get a DNF?
timeout = 5


#################################################
#          Create race object and race          #
#################################################


log = log()
# DEBUG:
log.setDisplayLevel('TRACE')

pinewood = pinewood(lanes, startBtn, log)
pinewood.setTimeout(5)

pinewood.race()
