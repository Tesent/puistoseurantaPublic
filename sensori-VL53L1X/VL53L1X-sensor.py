import VL53L1X
import time
import signal
import sys

INTER_MEASUREMENT_PERIOD_MILLIS = 70
UPDATE_TIME_MICORS = 66000

tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x28)
tof1.open()
tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x2a)
tof2.open()

#Alustetaan ja asetetaan roi
roi = VL53L1X.VL53L1xUserRoi(6,9,9,6)
tof1.set_user_roi(roi)
tof2.set_user_roi(roi)

#Asetetaan mittauksen vali
tof1.set_timing(UPDATE_TIME_MICORS, INTER_MEASUREMENT_PERIOD_MILLIS)
tof2.set_timing(UPDATE_TIME_MICORS, INTER_MEASUREMENT_PERIOD_MILLIS)

#Aloitetaan mittaaminen
tof1.start_ranging(3)
tof2.start_ranging(3)

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
verrokki = int(((tof1.get_distance()+tof2.get_distance())/2)*0.9)

#Apumuuttujat, joiden avulla tarkastellaan kuljettua jarjestysta
eka = False
toka = False

ensimmainen = (False, False)
viimeisin = (False, False)

palautus = ((False, False),(False,False))

eka_tallessa = False

print(verrokki)
time.sleep(0.1)

while running:
    d1 = tof1.get_distance()
    d2 = tof2.get_distance()
    if verrokki > d1:
        eka = True
    else:
        eka = False
    if verrokki > d2:
        toka = True
    else:
        toka = False
    
    if (eka, toka) != (False, False) and  not eka_tallessa:
        ensimmainen = (eka, toka)
        viimeisin = (eka, toka)
        eka_tallessa = True
    
    if (eka, toka) == (False, False) and eka_tallessa:
        if ensimmainen == (True, False) and viimeisin == (False, True):
            print("Out")
        if ensimmainen == (False, True) and viimeisin == (True, False):
            print("In")
        ensimmainen = (False, False)
        viimeisin = (False, False)
        eka_tallessa = False
    
    if (eka, toka) != (False, False):
        viimeisin = (eka, toka)
    
    #print("1: {}, 2: {}".format(d1,d2))
    
        
    time.sleep(INTER_MEASUREMENT_PERIOD_MILLIS/1000)