#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import board
import os
from gpiozero import Button, DigitalInputDevice

GPIO.setmode(GPIO.BCM)

LANE_1_SENSE=20
LANE_2_SENSE=21
LANE_3_SENSE=22
LANE_4_SENSE=23

LANE_1 = DigitalInputDevice(LANE_1_SENSE, True)
LANE_2 = DigitalInputDevice(LANE_2_SENSE, True)
LANE_3 = DigitalInputDevice(LANE_3_SENSE, True)
#LANE_4 = Button(board.D23.id, True)
LANE_4 = DigitalInputDevice(LANE_4_SENSE, True)

#LANE_1_LIGHT=

#GPIO.setup(LANE_1_SENSE, GPIO.IN)
#GPIO.setup(LANE_2_SENSE, GPIO.IN)
#GPIO.setup(LANE_3_SENSE, GPIO.IN)
#GPIO.setup(LANE_4_SENSE, GPIO.IN)

#GPIO.setup(LANE_1_LIGHT, GPIO.OUT)

L1STS="False"
L2STS="False"
L3STS="False"
L4STS="False"

while True:
  if LANE_1.value == 1:
    L1STS="Car"
  else:
    L1STS="Clear"
  
  if LANE_2.value == 1:
    L2STS="Car"
  else:
    L2STS="Clear"
    
  if LANE_3.value == 1:
    L3STS="Car"
  else:
    L3STS="Clear"
    
  if LANE_4.value == 1:
    L4STS="Car"
  else:
    L4STS="Clear"

  os.system('clear')
  print("Lane 1: " + L1STS)
  print("Lane 2: " + L2STS)
  print("Lane 3: " + L3STS)
  print("Lane 4: " + L4STS)
  time.sleep(0.2)
  
