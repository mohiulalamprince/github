#!/usr/bin/env python

import serial

s = serial.Serial("COM3")
s.write("AT\r")
print s.read()
        