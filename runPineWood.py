#!/usr/bin/python3


from PineWood import pinewood
from gpiozero import Button, PWMLED
from log import *
import gate
import rgLED


###################################
#          Configuration          #
###################################


# Configure the starting equipment
# NO = 12
# NO = 19
start = {'input':19,'rLED':16,'gLED':13}

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

startBtn = Button(start['input'], False)
startRgLED = rgLED.rgLED(start['rLED'], start['gLED'])

startGate = gate.gate(startBtn, startRgLED)

pinewood = pinewood(lanes, startGate, log)
pinewood.setTimeout(5)

while True:
    pinewood.race()


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

