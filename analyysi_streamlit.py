import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch
from scipy.fft import fft, fftfreq
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

st.title('Kävelyanalyysi GPS- ja kiihtyvyysdatasta')

# --- 1. Lue data ---
df_gps = pd.read_csv("mittaukset/Location.csv")
df_acc = pd.read_csv("mittaukset/Linear Acceleration.csv")

# --- 2. GPS-analyysi ---
coords = list(zip(df_gps['Latitude (°)'], df_gps['Longitude (°)']))
distance = sum(geodesic(coords[i], coords[i+1]).meters for i in range(len(coords)-1))
duration = df_gps['Time (s)'].max() - df_gps['Time (s)'].min()
avg_speed = distance / duration if duration > 0 else np.nan

# --- 3. Kiihtyvyysdatan analyysi ---
time = df_acc['Time (s)'].values
fs = 1 / np.mean(np.diff(time))
# Etsi z-komponentti, muuten käytä parasta
z_candidates = [col for col in df_acc.columns if 'z' in col.lower()]
component_cols = [col for col in df_acc.columns if 'Linear Acceleration' in col]
best_col = None
best_peak = 0
for col in component_cols:
	acc = df_acc[col].values
	f_test, Pxx_test = welch(acc, fs, nperseg=1024)
	mask = (f_test > 0.7) & (f_test < 3.0)
	peak = np.max(Pxx_test[mask]) if np.any(mask) else 0
	if peak > best_peak:
		best_peak = peak
		best_col = col
z_col = z_candidates[0] if z_candidates else best_col
z_data = df_acc[z_col].values
z_data_centered = z_data - np.mean(z_data)

# Suodatus
def butter_lowpass_filter(data, cutoff, fs, order=3):
	nyq = 0.5 * fs
	normal_cutoff = cutoff / nyq
	b, a = butter(order, normal_cutoff, btype='low', analog=False)
	y = filtfilt(b, a, data)
	return y
z_filt = butter_lowpass_filter(z_data_centered, cutoff=5.0, fs=fs, order=3)

# Askelmäärä nollanylityksistä
zero_crossings = np.where(np.diff(np.sign(z_filt)))[0]
askeleet_nolla = int(np.round(len(zero_crossings) / 2))

# Askelmäärä Fourier-analyysilla
N = len(z_filt)
dt = np.mean(np.diff(time))
fourier = fft(z_filt)
psd = np.abs(fourier)**2 / N
freqs = fftfreq(N, dt)
mask = (freqs > 0.8) & (freqs < 4.0)
if np.any(mask):
	dom_freq = freqs[mask][np.argmax(psd[mask])]
else:
	dom_freq = 0
thr = np.std(z_filt) * 0.2
active = np.abs(z_filt) > thr
T_active = active.sum() / fs
askeleet_fft = int(np.round(dom_freq * T_active)) if dom_freq > 0 else 0

# Askelpituus
askelpituus = distance / askeleet_nolla if askeleet_nolla > 0 else np.nan

# --- 4. Tulokset ---
st.header("Tulokset")
st.write(f"**Askelmäärä suodatetusta kiihtyvyysdatasta (nollanylitykset):** {askeleet_nolla}")
st.write(f"**Askelmäärä Fourier-analyysilla:** {askeleet_fft}")
st.write(f"**Kuljettu matka (GPS):** {distance/1000:.2f} km")
st.write(f"**Keskinopeus (GPS):** {avg_speed*3.6:.2f} km/h" if np.isfinite(avg_speed) else "**Keskinopeus (GPS):** —")
st.write(f"**Askelpituus:** {askelpituus:.2f} m" if np.isfinite(askelpituus) else "**Askelpituus:** —")

# --- 5. Visualisoinnit ---
st.header("Visualisoinnit")
st.subheader("Suodatettu kiihtyvyysdata (z-komponentti)")
fig0, ax0 = plt.subplots(figsize=(10, 4))
ax0.plot(time, z_filt, color='red')
ax0.set_xlabel("Aika (s)")
ax0.set_ylabel("a_z (m/s²), keskitetty")
ax0.set_title("Suodatettu kiihtyvyys (lowpass)")
ax0.grid()
st.pyplot(fig0)

st.subheader("Tehospektritiheys (PSD)")
f, Pxx = welch(df_acc[best_col].values, fs, nperseg=1024)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(f, Pxx, color='#1976d2', linewidth=2)
ax.set_xlabel("Taajuus [Hz]", fontsize=14)
ax.set_ylabel("Teho", fontsize=14)
ax.tick_params(axis='both', labelsize=12)
fig.subplots_adjust(left=0.08, right=0.98, top=0.85, bottom=0.15)
fig.text(0.01, 0.97, "Tehospektri", fontsize=28, fontweight='bold', va='top', ha='left')
st.pyplot(fig)

st.subheader("Reitti kartalla")
start_lat = df_gps['Latitude (°)'].mean()
start_long = df_gps['Longitude (°)'].mean()
my_map = folium.Map(location=[start_lat, start_long], zoom_start=14)
folium.PolyLine(coords, color='blue', weight=3.5, opacity=1).add_to(my_map)
st_folium(my_map, width=900, height=650)