# Sovelluksen toteutus
Sovellus on toteutettu ilman laajojen kielimallien käyttöä.

### Sovelluksen rakenne ja toiminta
Sovellus on graafisen käyttöliittymän (GUI) omaava tieteellinen laskin, jolle voidaan antaa syötteitä myös tietokoneen näppäimistön avulla. Käyttäjän infix-notaatiossa antama laskutoimitus annetaan käyttöliittymästä merkkijonona laskutoimituksista vastaavalle luokalle, joka hyödyntää validointi-luokkaa syötteen validoinnissa. Syötteen mukana annetaan käyttäjän GUI:ssa määrittelemä laskennan tarkkuus (desimaalien lukumäärä tuloksessa). Validointi suoritetaan kahdessa osassa. Ensin syöte validoidaan sen suhteen onko siinä oikeat tokenit oikeassa järjestyksessä (esim. että funktioille annetaan oikea määrä argumentteja) ja evaluoinnin jälkeen validoidaan onko evaluointi onnistunut. Tämä siksi, että esim. nollalla jakamisesta johtuvaa virhettä ei voida mielekkäästi tunnistaa ennen evaluointia, koska jakajana saattaa olla monimutkainen laskutoimitus. Jos validoinnissa huomataan virhe, laskin-luokka saa validointi-luokalta virheilmoituksen sisältävän merkkijonon, jonka laskin-luokka antaa eteenpäin GUI-luokalle. Jos validoinnissa ei löydetä virheitä, validointi-luokka antaa tyhjän merkkijonon laskin-luokalle, joka sitten palauttaa GUI-luokalle merkkijonomuotoisen syötteen, johon on lisätty " = X --> A", jossa X on saatu tulos ja A on muuttuja (--> A lisätään vain jos tulos talletetaan muuttujaan). Laskin-luokalla on results-muuttuja, johon saatu tulos talletetaan mahdollista muuttujaan tallettamista varten.

Sovellus hyödyntää validoinnissa ja laskutoimitusten evaluoinnissa sitä, että kullekin syötteen merkille on olemassa uniikki unicode-kokonaisluku. Tällöin on mahdollista tarkistaa että onko syötteen merkki esim. numero tai kirjain yksinkertaisilla vertailuoperaatioilla, sillä esim. numeroiden unicode-luvut ovat peräkkäisiä, eikä esim. tarvitse tarkistaa looppien avulla kuuluuko kyseinen syötteen merkki merkkijonoon "0123456789" tai tarkistaa isdigit() -funktiolla onko kyseessä kokonaisluku. Muunnokset merkkien ja unicode-lukujen välillä tosin monimutkaistaa merkittävästi sovelluksen rakennetta. Lisäksi tällä saatu hyöty algoritmien nopeudessa jää melko pieneksi, koska loopattavat merkkijonot olisivat olleet suhteellisen pieniä. Saatuaan merkkijonomuotoisen syötteen, laskin-luokka muuttaa sen listaksi syötteen merkkien unicode-lukuja. Sitten laskin-luokka käy läpi kyseisen listan ja tekee sen avulla listan listoja, joissa kukin lista sisältää tokenin merkkien unicode-luvut. Laskimen shunting yard -algoritmi tekee tämän listojen listan avulla dequen, joka sisältää tokenien kokonaislukulistat postfix-notaatiossa. Laskin muuttaa sitten tämän dequen listat merkkijonomuotoon tai Decimal-olioiksi (jos token on muuttuja, vakio tai luku). Laskin evaluoi tämän dequen, muuttaa tuloksen oikeaan tarkkuuteen käyttäjän antaman arvon mukaisesti. Kyseinen tulos tallennetaan laskimen results-muuttujaan, josta tämä deque myöhemmin (jos käyttäjä on niin määrittänyt GUI:ssa) tallennetaan muuttujat ja niiden arvot sisältävään dictionaryyn.

### Suorituskyky
Sovelluksen algoritmeilla on seuraavat aikavaativuudet:

Calculator-luokasta testatiin funktiot seuraavasti:
- chars_to_ints
    - Koska funktiossa rakennetaan uusi lista yksinkertaisen list comprehensionin avulla, on aikavaativuus O(n)
- ints_to_tokens
    - Funktiossa on yksi for loop, jossa on yksinkertaisia vertailuoperaatioita ja listan append()-funktiokutsuja (aikavaativuus O(1)), joten funktion aikavaativuus on O(n)
- shunting_yard
    - Shunting yard -algoritmin aikavaativuus on O(n) ([viite] (https://en.wikipedia.org/wiki/Shunting_yard_algorithm))
- ints_to_values
    - Funktiossa on for loop, jossa yhdistetään merkkijonoja ja lisätään alkio dequeen, joten aikavaativuus on O(n)
- evaluate_input_in_postfix_notation
    - Funktiossa on while loop, jossa popataan alkioita dequesta tai lisätään alkioita dequeen (kummankin aikavaativuus O(1)), joten aikavaativuus on O(n)

Validator-luokasta testattiin funktiot seuraavasti:
- get_calling_function_name
    - Palauttaa kutsuvan funktion nimen isolla alkukirjaimella ja huutomerkillä, eikä tehokkuus riipu sovelluksen saamasta syötteestä
- does_not_compute, numbers_too_large_to_be_computed, division_by_zero_is_undefined
    - Funktiot yhdistävät tyhjään merkkijonoon totuusarvolla kerrotun get_calling_function_name -funktion paluuarvon, joten niiden aikavaativuus on O(1)
- unassigned_variables_used
    - Funktio sisältää for loopin, missä suoritetaan yksinkertainen vertailuoperaatio jokaisen alkion kohdalla, joten aikavaativuus on O(n)
- invalid_use_of_operators
    - Funktio sisältää for loopin, missä suoritetaan yksi tai kaksi yksinkertaista vertailuoperaatiota jokaisen alkion kohdalla, joten aikavaativuus on O(n)
- missing_operator
    - Funktio käy läpi syötteen yhdellä for loopilla, joten aikavaativuus on O(n)
- unknown_function_used
    - Funktiossa käydään syötteen tokenit läpi yhdellä for loopilla, joten aikavaativuus on O(n)
- invalid_use_of_dot
    - Funktiossa etsitään löytyykö syötelistasta tiettyä alkiota ja kerrotaan paluuarvo get_calling_function_name:n paluuarvolla, joten aikavaativuus on O(n)
- invalid_use_of_functions
    - Funktiossa on kaksi sisäkkäistä for looppia syötteen läpikäymiselle, joten aikavaativuus on O(n^2)
- missing_function
    - Funktiossa suoritetaan jokaisen syötteen tokenin kohdalla kuusi vertailuoperaatiota, joten aikavaativuus on O(n)
- missing_function_argument
    - Funktio tekee neljä vertailuoperaatiota jokaiselle syötteen tokenille, joten aikavaativuus on O(n)
- mismatched_parentheses
    - Funktio palauttaa nimensä isolla alkukirjaimella ja huutomerkillä, jos sen saama argumentti on tyhjä lista, joten sen aikavaatimus on O(1)

### Puutteet

Sovelluksen rakenteen kannalta suurin puute on, että Calculator-luokka on riippuvainen Validator-luokasta, mikä hankaloittaa sovelluksen testaamista. Syötteen validointi merkkien unicode-lukujen avulla monimutkaistaa sovelluksen rakennetta ja tekee myös testaamisesta hankalampaa. Shunting yard -algoritmi on melko pitkä ja monimutkainen. Jos sitä pystyisi mielekkäästi yksinkertaistamaan tai muuten selkeyttämään, sen ymmärtäminen helpottuisi.