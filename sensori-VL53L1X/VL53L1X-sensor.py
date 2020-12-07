import VL53L1X
import time
import signal
import sys
import requests
import subprocess
from requests.auth import HTTPBasicAuth
from datetime import datetime
from datetime import timedelta

#Requestin muuttujat
url = "http://128.199.32.80/post_data/testi"
url_testimittaus = "http://128.199.32.80/post_data/tarkkailu"
salaus = "VahvaSalausOnVahva"
laite_id = 123
ip = subprocess.check_output(['hostname', '-I']).split(" ")[0]

#Apumuuttujia tarkistusmittauksen lahettamisen ajastusta varten
edellinen_aika = datetime.now()
vertailu_aika = timedelta(seconds=10)

#Mittavali
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

#Samat toiselle anturille
tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x2a)
tof2.open()
roi2 = VL53L1X.VL53L1xUserRoi(0,7,4,11)
tof2.set_user_roi(roi2)
tof2.set_timing(TIMING_BUDGET, INTER_MEASUREMENT_PERIOD_MILLIS)
tof2.start_ranging(0)

#Apumuuttuja exit_handlerille ja while loopille
running = True

#Funktio ohjelman sammutusta varten, CTRL+C sulkee ohjelman
def exit_handler(signal, frame):
    global running
    running = False
    tof1.stop_ranging()
    tof2.stop_ranging()
    print("exit")
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

######                   ######
###### Ohjelman logiikka ######
######                   ######

#Luodaan verrattava arvo molempien antureiden keskiarvosta ja kertoimesta
#Kerroin kertoo sen, etta milloin ohjelma ajattelee jonkin olevan anturin edessa
#verrattuna maksimiarvoon
kerroin = 0.8
verrokki = int(((tof1.get_distance()+tof2.get_distance())/2)*kerroin)

#Apumuuttujat, joiden avulla tarkastellaan kuljettua jarjestysta
eka = False
toka = False

#Ensimmainen ja viimeinen arvopari, arvojen perusteella voidaan paatella kulkusuunta
#esim ensimmainen (False, True) ja viimeinen (True, False) -> kuljettu oikealta vasemmalle
ensimmainen = (False, False)
viimeisin = (False, False)

#Apumuuttuja, joka kertoo sen, etta onko ensimmaista mittausta (jokin on laitteen edessa) tapahtunut
#muuttuja resetoidaan, kun mitaan ei ole edessa
eka_tallessa = False

#Tehdaan tarkistuksia ja lahetetaan arvot palvelimelle
tarkistus_mittaus = {
    'laite_id' : laite_id,
    'etaisyys1' : -1,
    'etaisyys2' : verrokki,
    'ip' : ip
}

#x = requests.post(url_testimittaus, data=tarkistus_mittaus, auth=HTTPBasicAuth('laite', salaus))
#print(x)

#Tulostetaan verrattava arvo kalibrointia varten
print(verrokki)

#Silmukka mittaamista varten
while running:
    #Haetaan antureiden mittaama etaisyys
    d2 = tof2.get_distance()
    d1 = tof1.get_distance()
    
    #Jos aiemmin laskettu verrokki arvo on suurempi kuin mitattu tulos ->
    #anturin d2 edessa on jotakin
    if verrokki > d2:
        toka = True
    else:
        toka = False
    
    #Sama vertailu anturille d1
    if verrokki > d1:
        eka = True
    else:
        eka = False
    
    #Jos eka_tallessa ei ole tallessa (ensimmaista havaintoa ei ole tehty), niin viedaan
    #mittauksen tulokset apumuuttujiin
    if (eka, toka) != (False, False) and  not eka_tallessa:
        ensimmainen = (eka, toka)
        viimeisin = (eka, toka)
        eka_tallessa = True
    
    #Jos eka_tallessa ja uusin mittaus on (False, False) -> jotakin on kaynyt anturin edessa
    #ja se on siita poistunut, joten tarkistetaan ensimmaisen ja viimeisen mittauksen
    #arvoparit
    if (eka, toka) == (False, False) and eka_tallessa:
        #Jos nama ehdot toteutuvat -> joku on kulkenut d1 -> d2 suuntaisesti
        #viedaan mittatulos serverille
        if ensimmainen == (True, False) and viimeisin == (False, True):
            #myObj = {
            #    'laite_id' : laite_id,
            #    'sisaan' : '0',
            #    'aika' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #    }
            #x = requests.post(url, data=myObj, auth=HTTPBasicAuth('laite', salaus))
            #print(x)
            print("Out")
        #Jos nama ehdot toteutuvat -> joku on kulkenut painvastaiseen suuntaan
        #TODO: anturi toimii 'huonosti' d2 -> d1 suunnassa ja tasta syysta logiikka eri kuin aiemmin
        if (ensimmainen == (False, True) or ensimmainen == (True, True)) and (viimeisin == (True, False) or viimeisin == (True, True)):
            #myObj = {
            #    'laite_id' : laite_id,
            #    'sisaan' : '1',
            #    'aika' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #    }
            #x = requests.post(url, data=myObj, auth=HTTPBasicAuth('laite', salaus))
            #print(x)
            print("In")
        #lopuksi nollataan apumuuttujat uusia havaintoja varten
        ensimmainen = (False, False)
        viimeisin = (False, False)
        eka_tallessa = False
    
    #mittausta varten tarvitsemme vain ensimmaisen ja viimeisen havainnon
    #joten paivitetaan viimeisin jokaisella mittauskerralla, kunnes se on (False, False), eli
    #kohde on poistunut edesta
    if (eka, toka) != (False, False):
        viimeisin = (eka, toka)
        print(viimeisin)  

    #lahetetaan tarkistusarvoja serverille 10min valein
    if (vertailu_aika < (datetime.now() - edellinen_aika)):
        uusi_ip = subprocess.check_output(['hostname', '-I']).split(" ")[0]
        tarkistus_mittaus = {
            'laite_id' : laite_id,
            'etaisyys1' : d1,
            'etaisyys2' : d2,
            'ip' : uusi_ip
            }
        print(tarkistus_mittaus)
        edellinen_aika = datetime.now()
        
    #print("\r 1: {}, 2: {}".format(d1,d2))  
    
    #nukutaan mittausten valissa
    time.sleep(INTER_MEASUREMENT_PERIOD_MILLIS/1000)