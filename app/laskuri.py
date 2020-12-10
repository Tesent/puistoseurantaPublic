import sqlite3 
from sqlite3 import Error
from datetime import datetime, timedelta



def yhdista(data):
    yhteys = None
    try:
        yhteys = sqlite3.connect(data)
    except Error as e:
        print(e)
        return yhteys
    
def select_rivit(yhteys):
    nyt = datetime.now()
    viisi = timedelta(minutes=5)                                                    nyt = nyt-viisi
    stime = nyt.strftime("%Y-%m-%d %H:%M:%S")
    cur = yhteys.curso()
    komento="SELECT COUNT(aika) FROM sensor_data WHERE sisaan == 1 AND Datetime(aika)>=Datetime('now','+2 hours', '-5 minutes')"
    # print(komento)
    cur.execute(komento)
    tulos = cur.fetchone()
    return tulos[0]                                                                                         
def main():
           
    tk = "/home/humppa/puistoseuranta/instance/app.sqlite"
    yhteys = yhdista(tk)
    with yhteys:
        hetkellinen=select_rivit(yhteys)
        print(hetkellinen)                                                          return hetkellinen
        #    return int(42)
        
if __name__ == '__main__':
    main()

