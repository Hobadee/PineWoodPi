#!/usr/bin/python3


from PineWood import *
from log import *


###################################
#          Configuration          #
###################################


# Configure start button sensor
startBtn = None

# Configure lanes and sensors
lanes = [{'no':1,'input':20},
        {'no':2,'input':21},
        {'no':3,'input':22},
        {'no':4,'input':23}]

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
