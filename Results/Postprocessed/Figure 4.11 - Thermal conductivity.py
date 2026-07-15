# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:32:52 2026

@author: kvtul
"""

import matplotlib.pyplot as plt
import numpy as np

with open('argonthermal.npy', 'rb') as f:
    temps = np.load(f)
    mean = np.load(f)
    std = np.load(f)
    success = np.load(f)

plt.figure(figsize=(6,4), dpi=300)
error = 1.96*std/np.sqrt(success)

LJmask = temps < 3000
Morsemask = (temps <= 10000) & ~LJmask

plt.errorbar(temps,mean,yerr=error,fmt='o',capsize=4, color='tab:orange', label='Thermal cond.\nMD Morse + Yukawa')
plt.errorbar(temps[LJmask],mean[LJmask],yerr=error[LJmask],fmt='o',capsize=4, color='tab:blue', label='Thermal cond.\nMD LJ')
plt.errorbar(temps[Morsemask],mean[Morsemask],yerr=error[Morsemask],fmt='o',capsize=4, color='tab:green', label='Thermal cond.\nMD Morse')

# Plot digitized data from Murhpy
x = np.array([952.3809908258751, 5492.063471559533, 3523.8091816497154, 9492.063148622186, 10380.953042205047, 11301.588484409413, 12031.74579082452, 12698.41199999661, 13460.317277063328, 14031.746840370899, 14857.143214680636, 15460.318326609713, 16095.238987160294, 16634.920579816247, 17238.095691745322, 17873.01635229591, 18444.44591560348, 19111.112124775565, 19809.523882569167, 7301.586385316654, 8095.23721100488, 8793.651390828587])
y = np.array([0.06711307446187162, 0.1342278557235312, 0.11185683090290732, 0.5369114228941247, 0.8053688411409752, 1.0961955774086614, 1.4093950452967594, 1.7449655380054814, 2.0805360307142036, 2.304249692520018, 2.3713644737816777, 2.326620717340642, 2.2818786676993943, 2.2371366180581465, 2.2371366180581465, 2.2818786676993943, 2.326620717340642, 2.483221304684585, 2.63982018522874, 0.22371366180581465, 0.2684557114470624, 0.3803125423499697])

# sort by x
idx = np.argsort(x)

x_sorted = x[idx]
y_sorted = y[idx]

plt.plot(x_sorted, y_sorted,'--', color='tab:red', label='Thermal cond.\nby Murphy $\mathit{et. al.}$')
plt.xlabel("Temperature (K)")
plt.ylabel("Thermal conductivity (W m$^{-1}$ K$^{-1}$)")
leg = plt.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    frameon=False
)
plt.xticks([5000, 10000, 15000, 20000])
for txt in leg.get_texts():
    txt.set_multialignment('left')
plt.grid()