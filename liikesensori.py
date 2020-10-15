import RPi.GPIO as GPIO
from datetime import datetime
import time

lID = 42                            #laite id
pin = 5                             #mones pinni piirilevyllä OUT (keltainen johto)


GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

try:
    while True:
        i = GPIO.input(pin)
        aika = datetime.now()
        if i==0:                    #sensorilta ei tule mitään
          #  print ("Ei liiku"),i
            time.sleep(1)
        else:                       #selsori on havainnut liikkeen
            print (str(lID) + "|" + aika.strftime("%y-%m-%d %H:%M:%S") + ";"),i
            time.sleep(3)
except:
    pass

GPIO.cleanup()

#TODO: tuloste tulee tuplana ~Maiju 15.10.
