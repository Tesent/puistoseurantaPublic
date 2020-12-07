import VL53L1X
import time
import signal
import sys
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

#Requestin muuttujat
url = "http://128.199.32.80/post_data/testi"

INTER_MEASUREMENT_PERIOD_MILLIS = 24
TIMING_BUDGET = 20000

#Alustetaan ensimmainen sensori
tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x28)
tof1.open()

#Alustetaan ja asetetaan roi
#                             x,y,x,y
roi1 = VL53L1X.VL53L1xUserRoi(11,7,15,11)
tof1.set_user_roi(roi1)

#Asetetaan mittauksen vali
tof1.set_timing(TIMING_BUDGET, INTER_MEASUREMENT_PERIOD_MILLIS)

#Aloitetaan mittaaminen
tof1.start_ranging(0)

#Samat toiselle sensorille
tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x2a)
tof2.open()
roi2 = VL53L1X.VL53L1xUserRoi(0,7,4,11)
tof2.set_user_roi(roi2)
tof2.set_timing(TIMING_BUDGET, INTER_MEASUREMENT_PERIOD_MILLIS)
tof2.start_ranging(0)

#Apumuuttuja exit_handlerille ja while loopille
running = True

#Funktio ohjelman sammutusta varten
def exit_handler(signal, frame):
    global running
    running = False
    tof1.stop_ranging()
    tof2.stop_ranging()
    print("exit")
    sys.exit(0)
    
signal.signal(signal.SIGINT, exit_handler)

#Otetaan verrattava arvio talteen
verrokki = int(((tof1.get_distance()+tof2.get_distance())/2)*0.8)

#Apumuuttujat, joiden avulla tarkastellaan kuljettua jarjestysta
eka = False
toka = False

ensimmainen = (False, False)
viimeisin = (False, False)

palautus = ((False, False),(False,False))

eka_tallessa = False

edellinen_aika = datetime.now()

print(verrokki)

while running:
    d2 = tof2.get_distance()
    d1 = tof1.get_distance()
    if verrokki > d2:
        toka = True
    else:
        toka = False
    if verrokki > d1:
        eka = True
    else:
        eka = False
    
    if (eka, toka) != (False, False) and  not eka_tallessa:
        ensimmainen = (eka, toka)
        viimeisin = (eka, toka)
        eka_tallessa = True
    
    if (eka, toka) == (False, False) and eka_tallessa:
        if ensimmainen == (True, False) and viimeisin == (False, True):
            myObj = {
                'laite_id' : '123',
                'sisaan' : '0',
                'aika' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            x = requests.post(url, data=myObj, auth=HTTPBasicAuth('laite', 'VahvaSalausOnVahva'))
            print(x)
            print("Out")
        if (ensimmainen == (False, True) or ensimmainen == (True, True)) and (viimeisin == (True, False) or viimeisin == (True, True)):
            myObj = {
                'laite_id' : '123',
                'sisaan' : '1',
                'aika' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            x = requests.post(url, data=myObj, auth=HTTPBasicAuth('laite', 'VahvaSalausOnVahva'))
            print(x)
            print("In")
        ensimmainen = (False, False)
        viimeisin = (False, False)
        eka_tallessa = False
    
    if (eka, toka) != (False, False):
        viimeisin = (eka, toka)
        print(viimeisin)
    
    #uusi_aika = datetime.now()
    #print("\r 1: {}, 2: {}, aika:{}".format(d1,d2,uusi_aika-edellinen_aika))
    #print(uusi_aika-edellinen_aika)
    #edellinen_aika = uusi_aika
        
    time.sleep(INTER_MEASUREMENT_PERIOD_MILLIS/1000)