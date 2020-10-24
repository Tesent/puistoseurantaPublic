from datetime import datetime, timedelta
import time
import dataset
import adafruit_dht
import board
from timeloop import Timeloop

#muuttujia
sensor_id = None #Vaihda tämä joksikin 500-15000 välillä
db_name = 'testi'
table_name = 'sensor_data'

#dht11 sensor, pulseio=False pakollinen raspilla?
dhtDevice = adafruit_dht.DHT11(board.D18, use_pulseio=False)

#sqlite database
db = dataset.connect('sqlite:///' + db_name)
table = db[table_name]

#tällä voitaisiin printata alkioita databasesta
for alkio in db[table_name]:
    print(alkio)

#Timeloop, 
t1 = Timeloop()

#Timeloop tehtävä, suoritetaan joka 60s
@t1.job(interval=timedelta(seconds=60))
def measure():
    temp = None
    humidity = None
    while temp is None or humidity is None:     #loopataan kunnes saadaan validi mittaus
        time.sleep(1)                           #nukutaan epäonnistuneiden mittausten välissä
        try:
            temp = dhtDevice.temperature        #kokeillaan mitata, jos onnistuu viedään tauluun
            humidity = dhtDevice.humidity
            if temp is not None and humidity is not None:
                #print("Temp: {:.1f} C    Humidity: {}% ".format(temp, humidity))
                aika = datetime.now()
                table.insert(dict(sId = sensor_id, h = humidity, t = temp, time = aika.strftime("%Y-%m-%d %H:%M:%S")))
                
        except RuntimeError as error:
            print(error.args[0])
    
        except Exception as error:
            dhtDevice.exit()
            raise error

#Aloitetaan timeloop
t1.start(block=True)
