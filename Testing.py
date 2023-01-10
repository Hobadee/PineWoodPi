#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import board
from gpiozero import Button

GPIO.setmode(GPIO.BCM)

LANE_1_SENSE=0
LANE_2_SENSE=0
LANE_3_SENSE=12
LANE_4_SENSE=23

LANE_3 = Button(board.D12.id, False)
LANE_4 = Button(board.D23.id, False)

#LANE_1_LIGHT=

#GPIO.setup(LANE_1_SENSE, GPIO.IN)
#GPIO.setup(LANE_2_SENSE, GPIO.IN)
GPIO.setup(LANE_3_SENSE, GPIO.IN)
GPIO.setup(LANE_4_SENSE, GPIO.IN)

#GPIO.setup(LANE_1_LIGHT, GPIO.OUT)


while True:
  #if GPIO.input(LANE_3_SENSE) == 1:
  if LANE_3.value == 1:
    #GPIO.output(LANE_1_LIGHT, GPIO.LOW)
    print("Lane 3: False")
  else:
    #GPIO.output(LANE_1_LIGHT, GPIO.HIGH)
    print("Lane 3: True")
    
  #if GPIO.input(LANE_4_SENSE) == 1:
  if LANE_4.value == 1:
    print("Lane 4: False")
  else:
    print("Lane 4: True")
  time.sleep(0.2)
  