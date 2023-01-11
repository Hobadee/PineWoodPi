#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import board
from gpiozero import Button, DigitalInputDevice

GPIO.setmode(GPIO.BCM)

LANE_1_SENSE=22
LANE_2_SENSE=23
LANE_3_SENSE=21
LANE_4_SENSE=20

LANE_3 = DigitalInputDevice(LANE_3_SENSE, True)
#LANE_4 = Button(board.D23.id, True)
LANE_4 = DigitalInputDevice(LANE_4_SENSE, True)

#LANE_1_LIGHT=

#GPIO.setup(LANE_1_SENSE, GPIO.IN)
#GPIO.setup(LANE_2_SENSE, GPIO.IN)
GPIO.setup(LANE_3_SENSE, GPIO.IN)
GPIO.setup(LANE_4_SENSE, GPIO.IN)

#GPIO.setup(LANE_1_LIGHT, GPIO.OUT)

L3STS="False"
L4STS="False"

while True:
  #if GPIO.input(LANE_3_SENSE) == 1:
  if LANE_3.value == 1:
    #GPIO.output(LANE_1_LIGHT, GPIO.LOW)
    L3STS="False"
  else:
    #GPIO.output(LANE_1_LIGHT, GPIO.HIGH)
    L3STS="True"
    
  #if GPIO.input(LANE_4_SENSE) == 1:
  if LANE_4.value == 1:
    L4STS="False"
  else:
    L4STS="True"
  print("Lane 3: " + L3STS + ", Lane 4: " + L4STS)
  time.sleep(0.2)
  
