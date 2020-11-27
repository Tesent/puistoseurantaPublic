import urllib.request, json

url = ["https://www.semma.fi/modules/json/json/Index?costNumber=1408&language=en",
       "https://www.semma.fi/modules/json/json/Index?costNumber=1402&language=en",
       "https://www.semma.fi/modules/json/json/Index?costNumber=1401&language=en"];

names = ['Piato.json', 'Maija.json', 'Lozzi.json']
i = 0;
for url in url:
    repsonse = urllib.request.urlopen(url)
    ruokala = json.load(repsonse)

    with open(names[i],'w') as jsonFile:
        json.dump(ruokala, jsonFile)
        i+=1;

#responseLozzi = urllib.request.urlopen(url[0]);
#lozzi = json.load(responseLozzi);

#with open('Lozzi.json', 'w') as jsonFile:
#    json.dump(lozzi, jsonFile);

#print(lozzi)