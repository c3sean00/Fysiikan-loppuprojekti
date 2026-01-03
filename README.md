# Fysiikan loppuprojekti

Tämä Streamlit-sovellus analysoi kävelyn kiihtyvyys- ja GPS-dataa, joka on mitattu Phyphox-sovelluksella. Sovellus laskee ja visualisoi seuraavat asiat:

- Askelmäärä suodatetusta kiihtyvyysdatasta (nollanylitykset)
- Askelmäärä Fourier-analyysilla (PSD)
- Kuljettu matka ja keskinopeus GPS-datasta
- Askelpituus (matka / askelmäärä)
- Suodatettu kiihtyvyysdatakäyrä
- Tehospektritiheys (PSD)
- Reitti kartalla

## Tiedostorakenne

```
Fysiikan-loppuprojekti/
├── analyysi_streamlit.py         # Streamlit-pääsovellus
├── README.md                    # Tämä ohjetiedosto
├── mittaukset/
│   ├── Linear Acceleration.csv  # Kiihtyvyysdata (Phyphox)
│   └── Location.csv             # GPS-data (Phyphox)
```

## Käytetyt komponentit ja kirjastot

- Python 3
- [Streamlit](https://streamlit.io/) – web-sovelluksen rakentamiseen
- [pandas](https://pandas.pydata.org/) – datan käsittelyyn
- [numpy](https://numpy.org/) – numeerisiin laskuihin
- [matplotlib](https://matplotlib.org/) – kuvaajien piirtämiseen
- [scipy](https://scipy.org/) – signaalinkäsittelyyn (filtterit, FFT)
- [folium](https://python-visualization.github.io/folium/) – karttavisualisointiin
- [streamlit-folium](https://github.com/randyzwitch/streamlit-folium) – Folium-karttojen näyttö Streamlitissä
- [geopy](https://geopy.readthedocs.io/) – etäisyyksien laskemiseen GPS-koordinaateista

## Datan käyttö

**Muista:** Koodin ajaminen suoraan GitHubista edellyttää, että datatiedostojen polut on määritelty viittaamaan GitHubin raw-linkkeihin (esim. `https://raw.githubusercontent.com/...`).

Koodissa käytetään seuraavia linkkejä:
- [Linear Acceleration.csv](https://raw.githubusercontent.com/c3sean00/Fysiikan-loppuprojekti/main/mittaukset/Linear%20Acceleration.csv)
- [Location.csv](https://raw.githubusercontent.com/c3sean00/Fysiikan-loppuprojekti/main/mittaukset/Location.csv)

Tällöin data haetaan suoraan GitHubista, eikä paikallisia tiedostoja tarvita.

## Sovelluksen käynnistys

1. Asenna riippuvuudet (esim. `pip install -r requirements.txt`).
2. Käynnistä sovellus:
   ```
   streamlit run analyysi_streamlit.py
   ```
3. Avaa selain ja siirry osoitteeseen [http://localhost:8501](http://localhost:8501).

## Testaus

- Sovellus hakee datan automaattisesti GitHubista.
- Jos haluat käyttää omaa dataa, muuta koodissa raw-linkit omiin tiedostoihisi tai käytä paikallisia polkuja.

