# Indeksin-tehokkuus

Tehtävän anto:

Tee ohjelma, jonka avulla voidaan suorittaa tietokannan tehokkuustesti. Tehokkuustestin osat ovat:

    Ohjelma luo taulun Elokuvat, jossa on sarakkeet id, nimi ja vuosi.
    Ohjelma lisää tauluun miljoona riviä. Jokaisen rivin kohdalla nimeksi valitaan satunnainen merkkijono ja vuodeksi valitaan satunnainen kokonaisluku väliltä 1900–2000.
    Ohjelma suorittaa tuhat kertaa kyselyn, jossa haetaan elokuvien määrä vuonna x. Jokaisessa kyselyssä x valitaan satunnaisesti väliltä 1900–2000. 

Toteuta ohjelma niin, että kaikki rivit lisätään saman transaktion sisällä (esimerkiksi alussa komento BEGIN ja lopussa komento COMMIT), jotta rivien lisääminen ei vie liikaa aikaa.

Elokuvien määrän laskemisessa käytä kyselyä, jossa haetaan COUNT(*) ehtoon täsmäävistä riveistä.

Suorita ohjelman avulla kolme testiä seuraavasti:

    Tauluun ei lisätä kyselyitä tehostavaa indeksiä.
    Tauluun lisätään kyselyitä tehostava indeksi ennen rivien lisäämistä.
    Tauluun lisätään kyselyitä tehostava indeksi ennen kyselyiden suoritusta. 

Ilmoita jokaisesta testistä rivien lisäämiseen ja kyselyiden suoritukseen kuluva aika sekä tietokantatiedoston koko testin jälkeen. Miten voit selittää testin tulokset?

Varmista ennen varsinaisia testejä, että kyselysi antavat järkeviä tuloksia: indeksin tulisi nopeuttaa kyselyjä merkittävästi testeissä 2 ja 3. Älä kuitenkaan tulosta varsinaisissa testeissä mitään muuta kuin ajankäyttö, jotta tulostaminen ei vääristä testin tulosta. 
