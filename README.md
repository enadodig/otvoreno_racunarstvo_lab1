# otvoreno_racunarstvo

# Lab1
## Skup podataka glazbenih žanrova i podžanrova

Ovaj skup podataka sadrži hijerarhijsku klasifikaciju glazbenih žanrova i podžanrova. Podatci su strukturirani u roditelj-dijete odnos koji omogućava pripadnost više podžanrova jednom glavnom žanru. Skup podataka može poslužiti za analizu glazbenih preferencija ili edukativne svrhe.

## Metapodatci
### Licencija:
Link: https://www.dbpedia.org/about/ | https://en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attribution-ShareAlike_4.0_International_License

Naziv: Creative Commons Attribution-ShareAlike 3.0 License 

Vrsta: CC BY-SA 4.0 GFDL

Opis: https://creativecommons.org/licenses/by-sa/4.0/deed.hr
    Slobodno možete:
    Dijelite dalje — možete umnažati i redistribuirati materijal u bilo kojem mediju ili formatu u bilo koju svrhu, pa i komercijalnu.
    Stvarajte prerade — možete remiksirati, mijenjati i prerađivati djelo u bilo koju svrhu, pa i komercijalnu.
    Davatelj licence ne može opozvati slobode korištenja koje Vam je ponudio dokle god se pridržavate uvjeta licence.
    Pod sljedećim uvjetima:
    Imenovanje — Morate adekvatno navesti autora , uvrstiti link na licencu i naznačiti eventualne izmjene . Možete to učiniti na bilo koji razuman način, ali ne smijete sugerirati da davatelj licence izravno podupire Vas ili Vaše korištenje djela.
    Dijeli pod istim uvjetima — Ako remiksirate, mijenjate ili prerađujete materijal, Vaše prerade morate distribuirati pod istom licencom pod kojom je bio izvornik.
    Bez daljnjih ograničenja — Ne smijete dodavati pravne uvjete ili tehnološke mjere zaštite koji će druge pravno ograničiti da čine ono što im licenca dopušta.
    Upozorenja:
    Ne morate se pridržavati licence kada je riječ o elementima djela koji su javno dobro ili gdje je Vaše iskorištavanje djela dopušteno zakonskim iznimkama i ograničenjima autorskog prava.
    Nema jamstava. Licenca Vam možda ne daje sva potrebna dopuštena za Vašu željeno korištenje djela. Primjerice, druga prava poput prava nad objavljivanjem osobne fotografije, pravo privatnosti ili moralno pravo može ograničiti kako smijete koristiti materija.
### Naziv autora
Ena Dodig
### Datum objavljivanja
26.10.2025.
### Verzija skupa podataka
1.0
### Jezik u kojemu se nalaze podaci
engleski
### Opis atributa koji se nalaze u skupu podataka
Skup podataka sadrži nazive žanrova (genre) i pripadajućih podžanrova (subgenre).
### Ključne riječi
glazba, žanr, podžanr, music, genre, subgenre
### Tema
glazbeni žanrovi
### Broj zapisa
20
### Format podataka
CSV, JSON

# Lab2
Web aplikacija koja prokazuje podatke u tabličnom obliku i omogućava navigaciju i filtriranje podataka te njihov izvoz u CSV i JSON fomratu.

# Lab3
REST API za upravljanje glazbenim žanrovima izrađen u Pythonu s OpenAPI specifikacijom API-ja.

Implementirani endpointi:

GET /api/genres - dohvati sve žanrove

GET /api/genres/{id} - dohvati žanr po ID-u

GET /api/genres/era/{era} - dohvati žanrove po eri

GET /api/genres/country/{country} - dohvati žanrove po državi

GET /api/genres/artist/{artist} - dohvati žanrove po izvođaču

POST /api/genres - kreiraj novi žanr

PUT /api/genres/{id} - ažuriraj žanr

DELETE /api/genres/{id} - obriši žanr

# Lab4
- web-aplikacija integrirana s uslugom auth0 za Single sign-on
- web sučelje mogućnošću prikaza elementarnog profila prijavljenog korisnika
- semantička dopuna za barem dva atributa resursa iz kolekcije po specifikaciji JSON-LD