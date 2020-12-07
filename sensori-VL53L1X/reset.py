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
GPIO.output(XSHUT2, True)
