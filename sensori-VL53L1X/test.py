from datetime import datetime
from datetime import timedelta
from random import randrange
import requests
import time
from requests.auth import HTTPBasicAuth

url = "http://128.199.32.80/post_data/testi"
salaus = "VahvaSalausOnVahva"

for x in range(0,500):
    sisaan = randrange(2)
    paiva = randrange(12)
    tunti = randrange(4,12)
    minuutti = randrange(0,60)
    sekunti = randrange(0,60)
    pvm = (datetime.now()-timedelta(days=paiva, hours=tunti, minutes=minuutti, seconds= sekunti)).strftime("%Y-%m-%d %H:%M:%S")
    myObj = {
        'laite_id' : 666,
        'sisaan' : sisaan,
        'aika' : pvm
        }
    x = requests.post(url, data=myObj, auth=HTTPBasicAuth('laite', salaus))
    print(x)
    time.sleep(1)