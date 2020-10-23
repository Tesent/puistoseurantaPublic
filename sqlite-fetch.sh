sqlite3 testi ".headers on" ".mode csv" ".output data.csv" "select * from [sensor_data] where [time] >= Datetime('now', '-5 minutes', 'localtime');"
mv data.csv ./kansio/id$(date +"%Y%m%dT%H%M%S").csv

#tällä skriptille pitäisi keksiä paremmat muuttujat: id, kansio jne.