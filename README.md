# Fysiikan loppuprojekti: Liikkeen analyysi matkapuhelimen sensoreilla

## Tausta
Matkapuhelimen sensoreilla voidaan tutkia käyttäjän liikettä monin eri tavoin. Kiihtyvyyssensori ja gyroskooppi mittaavat liiketilaa, GPS taas kertoo sijainnin. Monet yksinkertaiset hyvinvointisovellukset käyttävät kiihtyvyyden havaintoja, koska sensorin virrankulutus on maltillista ja sen käyttöön ei vaadita erillistä suostumusta. Pelkästään kiihtyvyyshavaintojen perusteella on kuitenkin vaikeaa mitata tarkasti matkaa tai arvioida energiankulutusta.

## Projektin kuvaus
Projektissa analysoidaan samanaikaisesti mitattuja GPS- ja kiihtyvyyshavaintoja ja tuotetaan niistä visualisointi Streamlit-sovelluksella. Tuloksena syntyy urheilusovelluksen prototyyppi, jonka avulla voi analysoida mitattua liikettä harjoittelun ajalta.

## Mittaukset
- Kävele ulkona usean minuutin ajan ja mittaa samalla kiihtyvyyttä ja sijaintia Phyphox-sovelluksella.
- Pidä puhelin samassa asennossa lähellä ylävartaloa.
- Kävele ensin hitaasti, sitten nopeammin ja lopuksi juokse.
- Mittaus tuottaa kaksi csv-tiedostoa: `Accelerometer.csv` ja `Location.csv`.

## Analyysi ja visualisointi
Sovellus analysoi ja visualisoi seuraavat asiat:
- Askelmäärä suodatetusta kiihtyvyysdatasta
- Askelmäärä Fourier-analyysin perusteella
- Keskinopeus (GPS-datasta)
- Kuljettu matka (GPS-datasta)
- Askelpituus (matkan ja askelmäärän perusteella)

Visualisoinnit:
- Suodatettu kiihtyvyysdata
- Kiihtyvyysdatan tehospektritiheys
- Reitti kartalla

## Käyttöohje
1. Lataa mittausdata Phyphox-sovelluksesta (Accelerometer.csv ja Location.csv).
2. Käynnistä sovellus komennolla:
   ```
   streamlit run analyysi_streamlit.py
   ```
3. Lataa csv-tiedostot sovelluksen sivupalkista.
4. Tutki visualisointeja ja analyysituloksia.

