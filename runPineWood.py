#!/usr/bin/python3

from PineWood import *

lanes = [{'no':1,'input':20},
        {'no':2,'input':21},
        {'no':3,'input':22},
        {'no':4,'input':23}]

pinewood = pinewood(lanes)
pinewood.race()
