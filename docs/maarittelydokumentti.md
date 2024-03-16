# Sovellusten vaatimusten määrittely

Tämä dokumentti määrittelee vaatimukset kurssin 'Aineopintojen harjoitustyö: Algoritmit ja tekoäly' harjoitustyösovellukselle. Kurssi tehdään osana Helsingin yliopiston Tietojenkäsittelytieteen kandidaatin tutkintoa. Harjoitustyö tehdään Pythonilla, mutta voin tarvittaessa vertaisarvioida myös sovelluksia, jotka on tehty Javalla. Projekti on dokumentoitu suomeksi ja koodi on kirjoitettu englanniksi.

Harjoitustyönä tehtävä sovellus on tieteellinen laskin. Laskimella on graafinen käyttöliittymä, minkä avulla käyttäjä voi syöttää laskutoimituksen tekstikenttään. Tämä tekstikenttä on muokattavissa myös näppäimistön avulla, jotta käyttäjä voisi kätevämmin korjata syöttämiään laskutoimituksia. Käyttäjä antaa laskutoimitukset laskimelle infix-notaatiossa (esim. 1 + 2), sillä se on tuttu suurimmalle osalle käyttäjistä. Sovellus muuttaa annetun syötteen Shunting yard -algoritmin avulla postfix-notaatioon (esim. 1 2 +), jonka avulla laskutoimitusten tekeminen sovelluksen toimesta on huomattavasti helpompaa. Laskutoimitusten arvot voidaan tallentaa muuttujiin, joita voidaan hyödyntää myöhemmissä laskutoimituksissa. Jos käyttäjä antaa virheellisen syötteen, sovellus ilmoittaa tästä käyttäjälle, eikä kyseisen syötteen mahdollisesti sisältämiä laskutoimituksia lasketa.

Syötteen infix-notaatiosta postfix-notaatioon muuttava algoritmin tulee toimia aikavaatimuksella O(n). Shunting yard perustuu pino-tietorakenteiden hyödyntämiseen. Pythonilla pino voidaan toteuttaa list- tai deque-tietorakenteilla. Aion kokeilla kumpi näistä olisi tehokkaampi edellämainitun algoritmin toteuttamiseen.

## Viitteet

[Shunting yard -algoritmi Wikipediassa](https://en.wikipedia.org/wiki/Shunting_yard_algorithm)
[Postfix-notaatio (Reverse Polish notation) Wikipediassa](https://en.wikipedia.org/wiki/Reverse_Polish_notation)