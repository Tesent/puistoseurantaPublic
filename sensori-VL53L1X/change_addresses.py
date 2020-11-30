#!/usr/bin/env python

import VL53L1X
import RPi.GPIO as GPIO
import time

XSHUT1 = 16
XSHUT2 = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(XSHUT1, GPIO.OUT)
GPIO.output(XSHUT1, False)
GPIO.setup(XSHUT2, GPIO.OUT)
GPIO.output(XSHUT2, False)

GPIO.output(XSHUT1, True)

tof1 = VL53L1X.VL53L1X(i2c_bus=1,i2c_address=0x29)
tof1.open()
tof1.change_address(new_address = 0x28)

tof1.open()

GPIO.output(XSHUT2, True)

tof2 = VL53L1X.VL53L1X(i2c_bus=1,i2c_address=0x29)
tof2.open()
tof2.change_address(new_address = 0x2a)

tof2.open()

GPIO.setup(XSHUT1, GPIO.IN)
GPIO.setup(XSHUT2, GPIO.IN)