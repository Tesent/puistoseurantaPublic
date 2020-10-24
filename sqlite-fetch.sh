sqlite3 ~/Tiea207/puistoseuranta-main/testi ".headers on" ".mode csv" ".output ./Tiea207/puistoseuranta-main/data.csv" "select * from [sensor_data] where [time] >= Datetime('now', '-15 minutes', 'localtime');"
mv ~/Tiea207/puistoseuranta-main/data.csv ~/Tiea207/puistoseuranta-main/kansio/id$(date +"%Y%m%dT%H%M%S").csv
#scp ~/Tiea207/puistoseuranta-main/kansio/id$(date +"%Y%m%dT%H%M%S").csv raspit@128.199.32.80:

#tällä skriptille pitäisi keksiä paremmat muuttujat: id, kansio jne.