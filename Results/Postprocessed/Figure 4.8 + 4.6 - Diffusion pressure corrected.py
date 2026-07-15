# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 04:50:21 2026

@author: kvtul
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
import csv
from debyelength import *

P_tot = 101325

# --- Load Debye data ---
with open('debyelength.npy', 'rb') as f:
    ArPlus_T = np.load(f)
    Debye    = np.load(f)
    ArPlus_n = np.load(f)

P_ion = ((ArPlus_n*const.k*ArPlus_T - (const.k*ArPlus_T)/(24*np.pi*Debye**3)))*.7


# --- Load density data (keep separate name to avoid overwrite) ---
with open('argondensity.npy', 'rb') as f:
    density_temps = np.load(f)
    density       = np.load(f)

k_B    = 1.380649e-23
m_atom = 6.6335e-26
rho_ideal = (P_tot * m_atom) / (k_B * density_temps)

n = getArn(density_temps) + getArPlusn(density_temps)
rho = n * 0.03995 / 6.022e23

# --- Load diffusion data ---
with open('argondiffusion.npy', 'rb') as f:
    temps   = np.load(f)
    mean    = np.load(f)
    std     = np.load(f)
    success = np.load(f)

with open('chapmanenskog-diffusion.npy', 'rb') as f:
    LJtemps    = np.load(f)
    LJCE       = np.load(f)
    Morsetemps = np.load(f)
    MorseCE    = np.load(f)

with open('argonplusdiffusion.npy', 'rb') as f:
    tempsion   = np.load(f)
    meanion    = np.load(f)
    stdion     = np.load(f)
    succession = np.load(f)

# --- Collision integral helpers ---
def load_collision_table(filename):
    Tlist, Omega11, Omega22 = [], [], []
    with open(filename) as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            Tlist.append(float(row[0]))
            Omega11.append(float(row[1]))
            Omega22.append(float(row[2]))
    return np.array(Tlist), np.array(Omega11), np.array(Omega22)

def getOmega11(Tstar, Tlist, Omega11):
    return np.interp(Tstar, Tlist, Omega11)

def getOmega22(Tstar, Tlist, Omega22):
    return np.interp(Tstar, Tlist, Omega22)

def Viscosity(M, T, sigma, Omega22):
    return 5*(np.pi*M*const.k*T)**.5/16/np.pi/sigma**2/Omega22

def Diffusion(M, T, p, sigma, Omega11):
    return 3*(2*const.k**3*T**3/M)**.5/16/p/np.pi**.5/sigma**2/Omega11

# --- Compute Yukawa CE diffusion ---
T     = np.linspace(8000, 20000)
debye = getDebyeLength(T)/10*1e-9
Tstar = 4*np.pi*const.epsilon_0*debye/(const.e**2/const.k/T)
Tstar = 4*np.pi*const.epsilon_0*const.k*T*debye / const.e**2

T_Yukawa, O11_Yukawa, O22_Yukawa = load_collision_table("outputYukawa.csv")
Omega11_arr = getOmega11(Tstar, T_Yukawa, O11_Yukawa)
Omega22_arr = getOmega22(Tstar, T_Yukawa, O22_Yukawa)

Na = 6.02214076e23
M  = 39.948e-3/Na

diff = np.zeros(T.shape)
visc = np.zeros(T.shape)
for i in range(len(T)):
    sigma      = getDebyeLength(T[i])/10*1e-9
    Om11       = getOmega11(Tstar[i], T_Yukawa, O11_Yukawa)
    Om22       = getOmega22(Tstar[i], T_Yukawa, O22_Yukawa)
    p_local    = np.interp(T[i], ArPlus_T, P_ion)
    diff[i]    = Diffusion(M, T[i], p_local, sigma, Om11)
    visc[i]    = Viscosity(M, T[i], sigma, Om22)

# --- Plot 1: Collision integrals + ion diffusion as subplots ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
plt.rcParams.update({'font.size': 12})

ax1.plot(T, Omega11_arr, label=r'$\Omega^\star_{11}$')
ax1.plot(T, Omega22_arr, label=r'$\Omega^\star_{22}$')
ax1.set_title("Reduced Collision Integrals")
ax1.set_xlabel("Temperature (K)")
ax1.set_ylabel(r"$\Omega^\star$")
ax1.legend()
ax1.grid()

ax2.plot(T, diff, color='tab:blue')
ax2.set_title("Ar$^+$ Self-Diffusion (Yukawa CE)")
ax2.set_xlabel("Temperature (K)")
ax2.set_ylabel("Self-diffusivity (m$^2$/s)")
ax2.grid()

fig.suptitle("Yukawa Collision Integrals and Ion Diffusion")
fig.tight_layout()
plt.show()
plt.figure(figsize=(6,3), dpi=300)
error = 1.96*std/np.sqrt(success)
plt.errorbar(temps[:4],mean[:4],yerr=error[:4],fmt='o',capsize=4, color='tab:blue', label='Ar LJ MD')
plt.errorbar(temps[4:11],mean[4:11],yerr=error[4:11],fmt='o',capsize=4, color='tab:green', label='Ar Morse MD')
plt.errorbar(temps[11:],mean[11:],yerr=error[11:],fmt='o',capsize=4, color='tab:orange', label='Ar Morse + Yukawa MD')
errorion = 1.96*stdion/np.sqrt(succession)

plt.errorbar(tempsion, meanion, yerr=errorion, fmt='s',capsize=4, color='tab:orange', label='Ar$^+$ Morse + Yukawa MD')
plt.plot(LJtemps, LJCE, color='tab:blue', label='LJ CE')
plt.plot(Morsetemps, MorseCE, color='tab:green', label='Morse CE')

mask = Morsetemps <= 15000
correction = np.interp(Morsetemps[mask], density_temps , rho_ideal/density)

plt.plot(Morsetemps[mask], MorseCE[mask]*correction, '--', color='tab:green', label='Morse CE correction')

mask = T >= 9000
plt.plot(T[mask], diff[mask], '--', color='tab:red', label='Yukawa CE')

#
plt.xlim([0,16000])

plt.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),  # push outside right side
    frameon=False
)
plt.title("Argon self-diffusivity")
plt.xlabel("Temperature (K)")
plt.ylabel("Self-diffusivity (m$^2$/s)")
plt.grid()


