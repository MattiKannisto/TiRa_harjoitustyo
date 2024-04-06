Tällä viikolla olen totetuttanut suurimman osan sovelluksen ydintoimintaa tukevista metodeista. Sovellusta pystyy nyt kokeilemaan käytännössä, mutta en ole vielä tehnyt tarpeeksi kattavia testejä sen varmistamiseksi, että sovellus laskee oikein kaikki syötteet ja huomaa virheelliset syötteet. Esim.validointiluokka tunnistaa nyt suurimman osan virheellisistä syötteistä, mutta esim. operaattorin puuttuminen syötteestä "1(3)" jää tunnistamatta virheelliseksi. Seuraavan viikon aikana aion keskittyä parantamaan validointiluokkaa, jotta se tunnistaa kaikki virheelliset syötteet. Lisäksi aion toteuttaa riittävästi testejä, jotta voin varmistua laskutoimitusten tapahtumisesta oikeellisesti.

Testausdokumentin kirjoitus on myös nyt aloitettu, mutta siinä on tällä hetkellä ainoastaan kuva testikattavuudesta. Aion ensi viikolla panostaa enemmän testauksen dokumentointiin.

Sovelluksen graafinen käyttöliittymä on nyt lähes valmis. Toteutin siihen mahdollisuuden muokata syötettä näppäimistön avulla ja lisäsin myös mahdollisuuden valita kuinka monen desimaalin tarkkuudella tulos esitetään. Refaktoroin myös käyttöliittymän koodia, mihin kului ehkä hieman liikaa aikaa.

Koodin laatu on pylintillä testattuna kohtalaisella tasolla, mutta siinä on paljon liian pitkiä rivejä. Lisäksi jotkin loopit voisi pylintin mukaan toteuttaa paremmin enumerate():n avulla. Aion ensi viikolla refaktoroida toteuttamiani luokkia hieman, minkä jälkeen alan siistimään pylintin ilmoittamia asioita.

Tällä viikolla käytetyt työtunnit: 20