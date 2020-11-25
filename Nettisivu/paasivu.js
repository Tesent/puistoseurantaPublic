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
      if(j.Components.length > 0){
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
}
function naytaTilasto(ruokala, popup){
  console.log(ruokala.attributes[1].value);
  //var popupText = document.createElement("span");
  //var ruokalaNimi = document.createTextNode(ruokala.attributes[1].value)
  //popupText.appendChild(ruokalaNimi);
  //popup.appendChild(popupText);
  //popup.classList.toggle("show");

  //Luodaan div:t popUp ikkunalle, sen headerille ja otsikolle
  var popUp = document.createElement("div");
  var popUpHeader = document.createElement("div");
  var popUpTitle = document.createElement("div");
  var popUpBody = document.createElement("div");

  //Annetaan niille luokat ja id:t
  popUp.setAttribute("class", "popUp");
  popUp.setAttribute("id", "popUp");

  popUpHeader.setAttribute("class", "popUp-header");

  popUpTitle.setAttribute("class", "popUpTitle");

  //Luodaan popUp:n otsikon teksti (HUOM! se on ruokalan nimi) 
  var popUpTitleText = document.createTextNode(ruokala.attributes[1].value);
  popUpTitle.appendChild(popUpTitleText);

  //Luodaan popUp:n sulkemis nappi
  var popUpCloseButton = document.createElement("button");
 

  popUpCloseButton.setAttribute("class", "PopUpClose-button");
  //popUpCloseButton.setAttribute("textContent", "X")
  popUpCloseButton.textContent = 'x';

  //Bodylle väliaikainen teksti
  var placeHolderText = document.createTextNode("Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolores consequatur fugiat dignissimos optio impedit accusantium error id corrupti, consequuntur deleniti ipsa, atque, quibusdam recusandae mollitia quisquam eum hic odio voluptatum illum provident laborum explicabo voluptates beatae? Ullam voluptate doloribus amet iste dignissimos perferendis unde, fugit reprehenderit corporis recusandae, ab quod. Repellat adipisci eum non corporis debitis soluta impedit minus, aperiam beatae quae, odio maxime recusandae dicta ipsa explicabo magnam veniam sed? Assumenda minima neque nesciunt placeat animi consequatur error beatae!");
  popUpBody.appendChild(placeHolderText);

  //popUpOverlay tulee ponnahdusikkunan taakse harmaaksi taustaksi jolla korostetaan visuaalisesti ponnahdusikkunaa
  var popUpOverlay = document.createElement("div");
  popUpOverlay.setAttribute("id", "popUpOverlay");
  popUpOverlay.setAttribute("class", "active");

  //Laitetaan headeriin otissko ja nappi
  popUpHeader.appendChild(popUpTitle);
  popUpHeader.appendChild(popUpCloseButton);

  //Laitetaan header ensimmäisenä popUp:iin
  popUp.appendChild(popUpHeader);

  //Laitetaan ponnahdusikkunan body ponnahdusikkunaan
  popUp.appendChild(popUpBody);

  //Lisätään popUp ja popUpOverlay hmtl:n body:n
  document.body.appendChild(popUp);
  document.body.appendChild(popUpOverlay);

  //Luodaan kuuntelija popUpCloseButton:lle jolla poistetaan popUp ja popUpOverlay
  popUpCloseButton.addEventListener("click", function(){closePopUp()})


}

//Funktio poistaa html body:ä popUp ja popUpOverlay:n
function closePopUp(){
  document.body.removeChild(popUp)
  document.body.removeChild(popUpOverlay);  
}

function taustaNapit(){
var popup = document.createElement("div");

var piato = document.getElementById("layer1");
piato.appendChild(popup);
piato.addEventListener("click", function(){naytaTilasto(piato, popup)});

var maija = document.getElementById("layer3")
maija.addEventListener("click", function(){naytaTilasto(maija)});

var lozzi = document.getElementById("layer4")
lozzi.addEventListener("click", function(){naytaTilasto(lozzi)});

var ylistö = document.getElementById("layer5")
ylistö.addEventListener("click", function(){naytaTilasto(ylistö)});

var uno = document.getElementById("layer6")
uno.addEventListener("click", function(){naytaTilasto(uno)});

var tilia = document.getElementById("layer7")
tilia.addEventListener("click", function(){naytaTilasto(tilia)});

var ilokivi = document.getElementById("layer8")
ilokivi.addEventListener("click", function(){naytaTilasto(ilokivi)});

}

getJson(urlI).then(() => {console.log('done')})
window.onload = taustaNapit;
//addContex(data);