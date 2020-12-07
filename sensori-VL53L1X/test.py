import subprocess
import time
import threading
from datetime import datetime
from datetime import timedelta

edellinen_aika = datetime.now()
vertailu_aika = timedelta(seconds=1)

output = subprocess.check_output(['hostname', '-I'])

print(subprocess.check_output(['hostname', '-I']).split(" ")[0])

while 1:
    if (vertailu_aika < (datetime.now() - edellinen_aika)):
        print(datetime.now())
        edellinen_aika = datetime.now()
    
    time.sleep(1)