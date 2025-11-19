# ============================================================
# LINEARIZZAZIONE DEL LASER TRAMITE INTERFEROMETRO DI MICHELSON
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
from scipy.interpolate import PchipInterpolator
from scipy.signal import find_peaks

# ========================
# === PARAMETRI ==========
# ========================

file_I1  = "L1_2.csv"     # braccio 1 bloccato → resta I2
file_I2  = "L2_2.csv"     # braccio 2 bloccato → resta I1
file_I12 = "ADD1.csv"     # entrambi aperti → interferenza Michelson

DeltaL_m = 0.32           # ΔL dell'interferometro [m]
c = 3e8                   # velocità della luce [m/s]

# ========================
# === LETTURA FILE =======
# ========================

def read_siglent_csv(path, ch_index=1, preview=True):
    """
    Legge un file .csv Siglent SDS1204X-E e restituisce tempo + canale.
    """
    with open(path, "r", encoding="latin-1") as f:
        lines = f.readlines()

    # Trova riga header dati
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("second"):
            header_idx = i
            break

    if header_idx is None:
        raise RuntimeError(f"Intestazione 'Second,...' non trovata in {path}")

    if preview:
        print(f"\n🔹 File: {path}")
        print(f"   → Riga dati trovata a linea {header_idx+1}")
        print("   Prime righe header prima dei dati:")
        for l in lines[:header_idx]:
            print("     ", l.strip())

    df = pd.read_csv(path, skiprows=header_idx)

    if preview:
        print("   Prime 5 righe dati:")
        print(df.head(), "\n")

    t = df.iloc[:, 0].to_numpy()
    y = df.iloc[:, ch_index].to_numpy()
    return t, y


# === Leggiamo i tre file ===
t1, I1_raw = read_siglent_csv(file_I1)
t2, I2_raw = read_siglent_csv(file_I2)
t12, I12_raw = read_siglent_csv(file_I12)

# =============================
# === ALLINEAMENTO TEMPORALE ==
# =============================

tmin = max(t1.min(), t2.min(), t12.min())
tmax = min(t1.max(), t2.max(), t12.max())

mask12 = (t12 >= tmin) & (t12 <= tmax)
t = t12[mask12]

I1_interp  = np.interp(t, t1, I1_raw)
I2_interp  = np.interp(t, t2, I2_raw)
I12_interp = I12_raw[mask12]




plt.figure(figsize=(9,3))
plt.plot(t, I12_interp)
plt.title("Interferenza grezza interpolata(t)")
plt.xlabel("Tempo [s]")
plt.ylabel("I_int [a.u.]")
plt.tight_layout()
plt.show()


# ============================================
#   COSTRUZIONE DELL'INTERFERENZA NORMALIZZATA
#   (formula corretta della slide!!)
# ============================================

# Segnali interpolati: I1_interp, I2_interp, I12_interp

eps = 1e-12
den = 2.0 * np.sqrt(np.clip(I1_interp, eps, None) * np.clip(I2_interp, eps, None))

I_int = (I12_interp - I1_interp - I2_interp) / den

plt.figure(figsize=(9,3))
plt.plot(t, I_int)
plt.title("Interferenza normalizzata I_int(t)")
plt.xlabel("Tempo [s]")
plt.ylabel("I_int [a.u.]")
plt.tight_layout()
plt.show()



# =============================
# === TROVA I PICCHI ==========
# =============================

# Tentativo: trovare i picchi sul segnale normalizzato I_int
I_int_smooth = savgol_filter(I_int, 51, 3)

idx_int, props = find_peaks(I_int_smooth, prominence=0.05, distance=50)

t_int_peaks = t[idx_int]
y_int_peaks = I_int_smooth[idx_int]


# soglia per rimuovere picchi artefatti (ad esempio il 50% dell'altezza max)
threshold = 0.25 * np.max(y_int_peaks)

mask_valid = y_int_peaks > threshold

# teniamo solo quelli veri
t_peaks_clean = t_int_peaks[mask_valid]
y_peaks_clean = y_int_peaks[mask_valid]

plt.figure(figsize=(12,4))
plt.plot(t, I_int_smooth, label="Interferenza normalizzata")
plt.plot(t_peaks_clean, y_peaks_clean, "ro", label="Picchi trovati")
plt.title("Picchi trovati sulla normalizzazione")
plt.legend()
plt.grid(True)
plt.show()

print("Numero di picchi trovati =", len(idx_int))

t_pk= t_peaks_clean
y_pl= y_peaks_clean


#################################
#picchi non normalizzati
#############################
# try:
    # I_smooth = savgol_filter(I12_interp, 31, 3)
# except Exception as e:
    # print("Problema con savgol_filter, uso direttamente I_mich:", e)
    # I_smooth = I_mich


# idx_pk, _ = find_peaks(I_smooth, height=3.0, distance=80)
# t_pk = t[idx_pk]
# y_pk = I_smooth[idx_pk]

# plt.figure(figsize=(9,4))
# plt.plot(t, I_smooth, label="Michelson")
# plt.plot(t_pk, y_pk, "ro", label="Picchi")
# plt.title("Picchi del Michelson")
# plt.legend()
# plt.tight_layout()
# plt.show()

# print("Numero di frange =", len(t_pk))



# =============================
# === CALCOLO FREQUENZE ======= Δν = c / (2ΔL)
# =============================

Delta_nu = c / (2 * DeltaL_m)
nu_pk = np.arange(len(t_pk)) * Delta_nu

plt.figure(figsize=(9,3))
plt.plot(t_pk, nu_pk, "o-")
plt.title("Scala di frequenza ai picchi")
plt.xlabel("Tempo [s]")
plt.ylabel("Frequenza (a.u.)")
plt.tight_layout()
plt.show()


# =============================
# === INTERPOLAZIONE ν(t) =====
# =============================

nu_of_t = PchipInterpolator(t_pk, nu_pk)(t)

plt.figure(figsize=(9,3))
plt.plot(t, nu_of_t)
plt.title("Laser linearizzato: ν(t)")
plt.xlabel("Tempo [s]")
plt.ylabel("Frequenza (a.u.)")
plt.tight_layout()
plt.show()


# =========================================
#   GRAFICO FRINGEPOSITION vs RAMP VOLTAGE
# =========================================

# 1) Leggiamo il canale CH3 = rampa dal file doppler
file_dopp = "003.csv"   # usa il primo doppler che hai acquisito
t_ramp, ramp_raw = read_siglent_csv(file_dopp, ch_index=1, preview=False)



# ============================================
#     SELEZIONE DELLA SOLA SALITA DELLA RAMPA
# ============================================

# 1) rampa raw
t_ramp, ramp_raw = read_siglent_csv(file_dopp, ch_index=1, preview=False)

# 2) rampa ai tempi dei picchi
ramp_at_peaks = np.interp(t_pk, t_ramp, ramp_raw)

# 3) maschera: dove la rampa CRESCE
mask_up_peaks = np.concatenate(([False], np.diff(ramp_at_peaks) > 0))

# 4) punti solo nella salita
V_salita = ramp_at_peaks[mask_up_peaks]
t_salita = t_pk[mask_up_peaks]

# 5) grafico
plt.figure(figsize=(7,5))
plt.plot(V_salita, t_salita, "o-", markersize=5)
plt.xlabel("Ramp Voltage [V]")
plt.ylabel("Fringe position [s]")
plt.title("Fringe position vs Ramp Voltage (solo salita della rampa)")
plt.grid(True)
plt.show()

# ===============================
# FIT POLINOMIALE DELLA NON-LINEARITÀ
# ===============================

# polinomio di secondo ordine
coeffs = np.polyfit(V_salita, t_salita, deg=2)  
p = np.poly1d(coeffs)

print("\nCoefficients (t = a*V^2 + b*V + c) =")
print(coeffs)

# plot confronto dati vs fit
V_fit = np.linspace(V_salita.min(), V_salita.max(), 500)
t_fit = p(V_fit)

plt.figure(figsize=(7,5))
plt.plot(V_salita, t_salita, "o", label="Dati")
plt.plot(V_fit, t_fit, "-", label="Fit polinomiale")
plt.xlabel("Ramp Voltage [V]")
plt.ylabel("Fringe position t [s]")
plt.title("Fit della non-linearità della risposta laser")
plt.grid(True)
plt.legend()
plt.show()




# =============================
# === SALVATAGGIO RISULTATI ===
# =============================

df_out = pd.DataFrame({
    "t": t,
    "nu": nu_of_t,
    "I12": I_int
})

df_out.to_csv("laser_linearized.csv", index=False)
print("\n✅ Creato file: laser_linearized.csv")


