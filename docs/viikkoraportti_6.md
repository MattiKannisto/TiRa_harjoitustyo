Olen tällä viikolla tehnyt pääasiassa lisää automaattisia testejä sovellukselleni ja sainkin nostettua testikattavuuden sataan prosenttiin. Testejä tehdessäni huomasin että en saa joitakin algoritmien haaraumia testattua millään syötteellä. Lopulta totesin että kyseiset koodirivit olivat itse asiassa tarpeettomia sovellukseni toiminnan kannalta, vaikka ne tuntuivatkin algoritmien toteutushetkellä tarpeellisilta. Mm. tämän syyn vuoksi totesin että olisi ollut järkevää tehdä enemmän ja kattavampia testejä sovellukselle heti projekti alussa, sillä ne olisivat todennäköisesti helpottaneet algoritmien toteuttamista.

Opin että automaattisia testejä kehittäessä on hyvä tehdä lyhyiden yhtä asiaa testaavien testien lisäksi monimutkaisia ja pitkiä syötteitä sisältäviä testejä. Tämä siksi, että pitkillä ja monimutkaisilla syötteillä on mahdollista löytää sovelluksesta virheitä, joiden olemassaoloa voi olla hankala ennakoida ja joille siten ei välttämättä osaa tehdä testejä. Olin esim. testannut aiemmin, että 'min()' -funktio palauttaa oikein pienemmän argumentit, mutta kun tein monimutkaisemman testin, missä se on ennen kertolaskua (esim. 'min(3,4)*32'), saadaan virheellinen tulos johtuen siitä, että funktioiden ja kertolaskujen laskujärjestys oli määritetty väärin. En olisi välttämättä löytänyt tätä virhettä ellen olisi generoinut sattumanvaraisesti pitkää monimutkaista syötettä, jossa kyseinen asia testattiin.

Lisäsin GUI:iin ominaisuuden, mikä estää muuttujaan tallentamisen, jos kaikki muuttujat A - Z ovat käytössä.

Tein toisen vertaisarvioinnin ja hyödynsin ensimmäisessä vertaisarvioinnissa saamaani palautetta mm. sovellukseni testien kehittämisessä. Sain vertaisarvioinnissa hyvää palautetta myös sovelluksen rakenteeseen liittyen, mutta en valitettavasti enää tässä vaiheessa ehdi tehdä näitä muutoksia sovellukseeni.

Sovellus on nyt valmis, mutta sen dokumentaatiota tarvitsee parantaa. Lisäksi, jos aikaa jää yli, aion refaktoroida koodia siistimmäksi pylintin ehdottamalla tavalla ja vertaisarvoinnissa saamani palautteen perusteella.

Tällä viikolla käytetyt työtunnit: 20
