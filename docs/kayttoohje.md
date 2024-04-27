# Käyttöohjeet
### Sovelluksen asennus ja käynnistäminen
1. Lataa sovelluksen viimeisin release
2. Asenna projektin riippuvuudet komennolla **poetry install**
3. Käynnistä sovellus komennolla **poetry run invoke start**

### Sovelluksen käyttäminen
Sovelluksen käynnistäminen avaa laskimen graafisen käyttöliittymän (GUI). Laskimelle voidaan antaa laskutoimituksia GUI:n nappien kautta sekä tietokoneen näppäimistön avulla. Laskimella voidaan suorittaa GUI:n nappien määrittämiä laskutoimituksia. Näppäimistön kautta laskutoimituksia syötettäessä '=' -nappia vastaava näppäin on 'Enter' ja muuttujaan tuloksen tallentavaa '--> X' nappia vastaava näppäin on oikea nuolinäppäin. Potenssiin korottavan '^' -napin näppäimenä käytetään '<' -merkkiä. Lisäksi ylös ja alas -nuolinäppäimillä on mahdollista selata aiemmin syötettyjä laskutoimituksia. Viimeisimmät kymmenen laskutoimitusta tuloksineen (ja mahdollisesti muuttujat joihin tulokset on talletettu) näkyvät syötteen yläpuolella olevalla alueella siten, että vanhin syöte on ylimpänä.

GUI:n oikeassa reunassa olevien pudotusvalikoiden kautta on mahdollista asettaa laskutoimituksen tuloksen tarkkuus (0 - 10 desimaalia) ja lisätä laskutoimitukseen muuttujia, joihin on talletettu aiempien laskutoimitusten arvoja. Sovellus nimeää muuttujat automaattisesti isoilla kirjaimilla aloittaen 'A':sta.

#### Sallitut syötteet
Laskimelle syötetään laskutoimitus infix notaatiossa (esim. 1 + 2). Desimaalit erotetaan pisteellä ('.') ja pilkku on varattu funktioiden argumenttien erottamiseksi toisistaan. Funktioiden nimen jälkeen on aina oltava kaarisulkeet ja kaarisulkeiden sisällä funktion argumentit (esim. 'max(1,2)'). Kaikkien lukujen, muuttujien ja funktioiden välissä on oltava jokin operaattori (esim. '+' tai '*'). Täten esim. syötteitä '2 + 5A' tai '3sin(3)' ei evaluoida, vaan niistä seuraa virheilmoitus. Syötteeseen ei voi lisätä välilyöntejä. Jos syöte syötekentässä tai syötehistoriassa on liian suuri mahtuakseen GUI:n ikkunaan, kyseisen syötteen klikkaaminen hiiren vasemmalla napilla mahdollistaa syötteen lukemisen kokonaisuudessaan erillisessä ponnahdusikkunassa.

### Sovelluksen testaaminen
Sovelluksen automaattiset testit voidaan ajaa komennolla **poetry run invoke test** ja testikattavuusraportti voidaan generoida komennolla **poetry run invoke coverage**. Sovelluksen pylint-tyylitarkistukset voidaan tehdä komennolla **poetry run invoke lint**.