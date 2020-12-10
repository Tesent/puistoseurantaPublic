#Created by Riku Laitinen



import matplotlib.pyplot as plt
import sqlite3 as sql
from dateutil import parser
import datetime

#Sqlite file with the visitor logs
#Need to change the path when uploading to the server
conn = sql.connect('app.sqlite')
#Selects all the date from the sqlite file
#Change to this "select * from [sensor_data] where [time] >= Datetime('now', '-1 day', 'localtime');" when
#we have more data in .sqlite file
cursor = conn.execute("select * from [sensor_data] where [laite_id] == 666 and [aika] >= Datetime('now', '-5 day');")
kaviat = 0
arrAika = []
arrKaviat = []
sysTime = datetime.datetime.now()
for row in cursor:

    date_time = parser.isoparse(row[3])
    hour = date_time.hour
    #Enable this when the visitor tracking device goes online
    if(sysTime.year != date_time.year or sysTime.month != date_time.month or hour < 6 or hour > 18):
        print("No new visitors within this month!")
        print("Last visitors were : %d" %date_time.year + ":%d" %date_time.month)
        pass
    else:

        if hour not in arrAika:
            arrAika.append(hour)
            arrKaviat.append(kaviat)

        if (row[2] == 1):
            kaviat += 1
        else:
            kaviat -= 1

   # print("Aika = ", row[3], "\n")


#def get_aika_maara():
#    laske = conn.execute("SELECT ")


#print("Kaviat : ", kaviat)

#aika = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
#kaviaMaara = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#for tunti in arrAika:
#    if tunti in aika:
#        kaviaMaara[aika.index(tunti)] = arrKaviat[aika.index(tunti)]




img = plt.bar(arrAika, arrKaviat, align='center', alpha=0.5)

plt.xlabel('Aika')
plt.ylabel('Käviämäärä')
#When on server insert path to '/var/www/html/maija.png'
plt.savefig('maija.png')
plt.show()