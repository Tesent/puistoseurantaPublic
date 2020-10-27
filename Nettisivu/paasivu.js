"use strict"

//let url = 'https://www.semma.fi/modules/json/json/Index?costNumber=1408&language=en'
// 
//async function getData(url) {
//  const response = await fetch(url);
//
//  return response.json();
//}
//
//const data = getData(url);

let url = [['Piato.json','divPiato'],['Maija.json', 'divMaija'], ['Lozzi.json', 'divLozzi']];
let urlI = 0;
//Luodaan ruokalistalle viikonpäivän mukaan id
let paivat = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai"];


async function getJson(urlI){
  //Haetaan .json tiedosto ja annetaan se addContex funktiolle
    try{
     await fetch(url[urlI][0])
      .then(res => res.json())
      .then(data => addContex(data, urlI));
      }
      catch (e){
        console.error(e.message);
      }
      //Käytetään rekursiota jolla käydään kaikki .json tiedostot läpi
      if(urlI < url.length){
        urlI++;
      getJson(urlI);
      }
      
}


//Luodaan dynaamisesti ravintolan nimi, pvm, aika ja ruokalista
function addContex(json, urlI){
  let paivatI = 0;
  //Luodaan ravintolan nimi ja laitetaan se runkoon
  var nimi = document.createElement("p");
  var ravintola = document.getElementById(url[urlI][1]);
  var nimiText = document.createTextNode(json.RestaurantName);
  nimi.appendChild(nimiText);
  ravintola.appendChild(nimi);

  for(let k of json.MenusForDays){
    //Luodaan div päivämäärää varten 
    var divAika = document.createElement("div");
    //Asetetaan jokaiselle div:lle oma id
    divAika.setAttribute("id", paivat[paivatI]);
    paivatI++;
    ravintola.appendChild(divAika);

    //Luodaan päivämäärä (Muutetaan myöhemmin muotoon dd//mm//yy)
    var pvm = document.createElement("label");
    var pvmText = document.createTextNode(k.Date);
    pvm.appendChild(pvmText);
    divAika.appendChild(pvm);

    //Luodaan kellonaika monelta ruokailu tapahtuu (Muotoa hh//mm//ss)
    var aika = document.createElement("label");
    var aikaText = document.createTextNode(k.LunchTime);
    aika.appendChild(aikaText)
    divAika.appendChild(aika)

    for(let j of k.SetMenus){
      //Luodaan Lounaan nimi (Muotoa VEGETARIAN LUNCH / LUNCH / DESSERT)
      var lunch = document.createElement("label");
      var lunchText = document.createTextNode(j.Name);
      lunch.appendChild(lunchText);
      
      var lunchDiv = document.createElement("div");
      lunchDiv.appendChild(lunch);
      divAika.appendChild(lunchDiv);

      for(let l of j.Components){
        //Luodaan lounaalla tarjottavan ruuan div nimiä varten
        var foodDiv = document.createElement("div");

        //Ruuan nimi
        var food = document.createElement("label");
        var foodText = document.createTextNode(l)
        food.appendChild(foodText);

        foodDiv.appendChild(food);
        lunchDiv.appendChild(foodDiv);
        


      }

    }
  }
}
getJson(urlI).then(() => {console.log('done')})
//addContex(data);