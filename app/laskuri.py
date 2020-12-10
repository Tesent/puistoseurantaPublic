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
    cur = yhteys.cursor()
    komento="SELECT COUNT(aika) FROM sensor_data WHERE sisaan == 1 AND Datetime(aika)>=Datetime('now','+2 hours', '-5 minutes')"
    # print(komento)
    cur.execute(komento)
    tulos = cur.fetchone()
    return tulos                                                 


def main():           
    tk = "../instance/app.sqlite"
    yhteys = yhdista(tk)
    with yhteys:
        hetkellinen=select_rivit(yhteys)
#        print(hetkellinen[0]) 
    return hetkellinen[0]
   

if __name__ == '__main__':
    main()





