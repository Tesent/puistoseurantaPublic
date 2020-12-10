import sqlite3
from sqlite3 import Error


def yhdista(data):
    yhteys = None
    try:
        yhteys = sqlite3.connect(data)
    except Error as e:
        print(e)
    return yhteys


def select_rivit(yhteys):
    cur = yhteys.cursor()
    cur.execute("SELECT COUNT(time) FROM sensor_data WHERE time LIKE '2020-11-13 14:%' AND sisaan == 1")
    
    tulos = cur.fetchone()
    return tulos

def main():
    tk = "./testi.db"

    yhteys = yhdista(tk)
    with yhteys:
        hetkellinen=select_rivit(yhteys)
   return hetkellinen
#    return int(42)

if __name__ == '__main__':
        main()

