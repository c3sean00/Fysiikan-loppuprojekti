import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks, welch
from geopy.distance import geodesic

# Streamlit app title
st.title("Liikkeen analyysi: Kiihtyvyys ja GPS")

# Data file upload
st.sidebar.header("Lataa mittaustiedostot")
acc_file = st.sidebar.file_uploader("Accelerometer.csv", type=["csv"])
loc_file = st.sidebar.file_uploader("Location.csv", type=["csv"])

if acc_file and loc_file:
    # Read accelerometer data
    acc_df = pd.read_csv(acc_file)
    # Read location data
    loc_df = pd.read_csv(loc_file)

    st.subheader("Kiihtyvyysdatan esikatselu")
    st.write(acc_df.head())
    st.subheader("GPS-datan esikatselu")
    st.write(loc_df.head())

    # Valitse analyysiin kiihtyvyyskomponentti
    acc_columns = [col for col in acc_df.columns if "X" in col or "Y" in col or "Z" in col]
    component = st.selectbox("Valitse kiihtyvyyskomponentti analyysiin", acc_columns)
    acc = acc_df[component].values
    time = acc_df[acc_df.columns[0]].values  # Oletetaan ensimmäinen sarake on aika

    # Suodatus (Butterworth bandpass)
    fs = 1 / np.mean(np.diff(time))  # Näytteenottotaajuus
    lowcut = 0.7  # Hz
    highcut = 3.0  # Hz
    b, a = butter(2, [lowcut/(0.5*fs), highcut/(0.5*fs)], btype='band')
    acc_filt = filtfilt(b, a, acc)

    st.subheader("Suodatettu kiihtyvyysdata")
    fig1, ax1 = plt.subplots()
    ax1.plot(time, acc_filt)
    ax1.set_xlabel("Aika (s)")
    ax1.set_ylabel(f"Kiihtyvyys ({component}) [m/s²]")
    st.pyplot(fig1)

    # Askelmäärä suodatetusta datasta
    peaks, _ = find_peaks(acc_filt, distance=int(fs*0.4), prominence=0.2)
    steps_filtered = len(peaks)
    st.metric("Askelmäärä (suodatettu)", steps_filtered)

    # Fourier-analyysi ja PSD
    f, Pxx = welch(acc, fs, nperseg=1024)
    st.subheader("Tehospektritiheys (PSD)")
    fig2, ax2 = plt.subplots()
    ax2.semilogy(f, Pxx)
    ax2.set_xlabel("Taajuus (Hz)")
    ax2.set_ylabel("PSD [m²/s⁴/Hz]")
    st.pyplot(fig2)

    # Askelmäärä PSD:n perusteella
    # Etsitään askeltaajuus (huippu 0.7-3 Hz välillä)
    mask = (f > 0.7) & (f < 3.0)
    step_freq = f[mask][np.argmax(Pxx[mask])] if np.any(mask) else 0
    duration = time[-1] - time[0]
    steps_psd = int(step_freq * duration)
    st.metric("Askelmäärä (PSD)", steps_psd)

    # GPS: matka ja keskinopeus
    st.subheader("Reitti kartalla")
    lat = loc_df[loc_df.columns[1]].values  # Oletetaan 2. sarake on lat
    lon = loc_df[loc_df.columns[2]].values  # Oletetaan 3. sarake on lon
    route = pd.DataFrame({"lat": lat, "lon": lon})
    st.map(route)

    # Matka
    distance = sum(geodesic((lat[i], lon[i]), (lat[i+1], lon[i+1])).meters for i in range(len(lat)-1))
    st.metric("Kuljettu matka (m)", f"{distance:.1f}")

    # Keskinopeus
    gps_time = loc_df[loc_df.columns[0]].values  # Oletetaan 1. sarake on aika
    gps_duration = gps_time[-1] - gps_time[0]
    avg_speed = distance / gps_duration if gps_duration > 0 else 0
    st.metric("Keskinopeus (m/s)", f"{avg_speed:.2f}")

    # Askelpituus
    step_count = st.radio("Valitse askelmäärä askelpituuden laskuun:", ["Suodatettu", "PSD"])
    steps = steps_filtered if step_count == "Suodatettu" else steps_psd
    step_length = distance / steps if steps > 0 else 0
    st.metric("Askelpituus (m)", f"{step_length:.2f}")

else:
    st.info("Lataa sekä kiihtyvyys- että GPS-tiedosto analyysiä varten.")
