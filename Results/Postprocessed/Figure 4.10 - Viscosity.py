# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:49:28 2026

@author: kvtul
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 13:36:19 2026
@author: kvtul
"""
import matplotlib.pyplot as plt
import numpy as np

with open('argonviscosity.npy', 'rb') as f:
    temps = np.load(f)
    mean = np.load(f)
    std = np.load(f)
    success = np.load(f)
    
with open('chapmanenskog-viscosity.npy', 'rb') as f:
    LJtemps_vis = np.load(f)
    LJCE_vis = np.load(f)
    Morsetemps_vis = np.load(f)
    MorseCE_vis = np.load(f)
    
plt.figure(figsize=(6,4), dpi=300)
plt.xlabel("Temperature (K)")
plt.ylabel("Viscosity (cP)")
plt.yticks([.05,.1,.15,.2,.25,.3])
error = 1.96 * std / np.sqrt(success)

LJmask = temps < 3000
Morsemask = temps <= 10000

plt.errorbar(temps, 1000*mean, yerr=1000*error, fmt='o', capsize=4,
                color='tab:orange', label='Morse + Yukawa MD')
plt.errorbar(temps[Morsemask], 1000*mean[Morsemask], yerr=1000*error[Morsemask], fmt='o', capsize=4,
                color='tab:green', label='Morse MD')
plt.errorbar(temps[LJmask], 1000*mean[LJmask], yerr=1000*error[LJmask], fmt='o', capsize=4,
                color='tab:blue', label='LJ MD')

plt.plot(LJtemps_vis, LJCE_vis, '--', color='tab:blue', label="LJ Kinetic Theory")
plt.plot(Morsetemps_vis, MorseCE_vis, '--', color='tab:green', label="Morse Kinetic Theory")


plt.ylim([0,.31])
with open('chen.npy', 'rb') as f:
    tempschen = np.load(f)
    vischen = np.load(f)

plt.plot(tempschen, vischen,'--',color='tab:red',label='Experimental (Chen $\it{et. al.})$')
#plt.title("Viscosity")

plt.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),  # push outside right side
    frameon=False
)
plt.grid()