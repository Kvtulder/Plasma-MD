# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:20:18 2026

@author: kvtul
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const

# Ar+ data
ArPlus_n = np.array([

    288043945271607230., 1112291446650506100., 5585596305826863000,
    20006971821596970000, 69012828343233670000, 183057359042794950000,
    585716728316807540000, 2.3466958764015197e+21, 5.355480564772642e+21,
    1.2686050265638124e+22, 2.894081288416934e+22, 5.271185147439671e+22,
    7.95907774873497e+22, 1.294761894070182e+23, 1.6201814071382912e+23,
    1.8110314731394875e+23, 1.876910855234455e+23, 1.8044821847775017e+23,
    1.609358713422984e+23, 1.5477452533236716e+23
], dtype=np.float64)
ArPlus_T = np.array([
    4595.898673100121, 4957.780458383596, 5392.038600723764,
    5826.296743063934, 6369.119420989145, 6839.56574185766,
    7454.764776839566, 8359.469240048253, 9010.856453558506,
    9879.372738238842, 10820.265379975877, 11688.781664656213,
    12412.545235223162, 13570.56694813028, 14402.895054282268,
    15416.164053075998, 16863.691194209892, 18311.21833534379,
    19758.745476477685, 20952.95536791315
])

# Ar data
Ar_n = np.array([
    1.9402013542176133e+25, 8.490530156404655e+24, 4.8305425188803314e+24,
    3.0751883132710726e+24, 2.1096895182024139e+24, 1.5024189496334566e+24,
    1.197828407388515e+24, 9.912080940781734e+23, 8.516073849567104e+23,
    7.046449035960166e+23, 5.8320228440674126e+23, 4.1534729977673903e+23,
    2.9588406137572315e+23, 1.883381825543493e+23, 1.2450234512091742e+23,
    7.635327332804891e+22, 3.466298816269308e+22, 1.6962636890909004e+22,
    8.949692170112345e+21, 5.698526524344072e+21,
    4.060421244839714e+21, 2.489448893571606e+21, 1.4697133980858707e+21,
    971388907762456900000, 512261279433511100000, 302427283262638100000
], dtype=np.float64)
Ar_T = np.array([
    361.8817852834745, 759.9517490952958, 1447.5271411338972,
    2316.043425814233, 3437.8769601930044, 4704.463208685164,
    5753.920386007238, 7056.694813027746, 8359.469240048253,
    9734.620024125452, 10892.641737032573, 12123.039806996385,
    13136.308805790111, 14113.38962605549, 14873.341375150787,
    15597.104945717736, 16646.56212303981, 17732.207478890232,
    18673.100120627263, 19396.863691194216,
    20229.1917973462, 21170.084439083235, 22291.917973462005,
    23196.62243667069, 24535.585042219547, 25657.418576598313
])
epsilon0 = 8.854187817e-12
kB = 1.380649e-23
e = 1.60217663E-19
Debye = (epsilon0*kB*ArPlus_T/2/ArPlus_n/(e**2))**.5



def getArPlusn(T):
    """ Returns the number density for Ar+ for a given temp"""
    return np.interp(T,ArPlus_T,ArPlus_n)

def getArn(T):
    """ Returns the number density for Ar for a given temp"""
    return np.interp(T,Ar_T,Ar_n)

def getDebyeLength(T):
    return np.interp(T,ArPlus_T,1e10*Debye)
    
def plot():
    # --- Plot 1: Number densities ---
    plt.figure(dpi=300)
    plt.grid()

    plt.plot(ArPlus_T, ArPlus_n, label="Ar+")
    plt.plot(Ar_T, Ar_n, label="Ar")
    plt.xlim([0, 20000])
    plt.legend()
    plt.semilogy()
    plt.title("Argon Ion number density")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Number density (m⁻³)")
    plt.tight_layout()
    
    # --- Degree of ionization ---
    # Interpolate Ar neutral density onto the Ar+ temperature grid
    # Only interpolate within the overlapping temperature range to avoid extrapolation
    T_min = max(ArPlus_T.min(), Ar_T.min())
    T_max = min(ArPlus_T.max(), Ar_T.max())
    
    mask = (ArPlus_T >= T_min) & (ArPlus_T <= T_max)
    T_common   = ArPlus_T[mask]
    ArPlus_n_common = ArPlus_n[mask]
    
    Ar_n_interp = np.interp(T_common, Ar_T, Ar_n)
    
    # Degree of ionization: alpha = n_ion / (n_ion + n_neutral)
    # This gives the fraction of argon atoms that are ionized (0 to 1)
    degree_of_ionization = ArPlus_n_common / (ArPlus_n_common + Ar_n_interp)
    
    # --- Plot 2: Degree of ionization (linear scale) ---
    plt.figure()
    plt.grid()

    plt.plot(T_common, degree_of_ionization)
    plt.xscale('linear')
    plt.yscale('linear')
    
    plt.xlabel("Temperature (K)")
    plt.ylabel("Degree of ionization α (-)")
    plt.title("Degree of Ionization of Argon")
    plt.xlim([T_min, T_max])
    plt.ylim([0, 1])
    plt.show()
    
    # Print a summary table
    print(f"{'Temperature (K)':>18} {'α (degree of ionization)':>26}")
    print("-" * 46)
    for T, alpha in zip(T_common, degree_of_ionization):
        print(f"{T:>18.1f} {alpha:>26.6f}")
    

    
    plt.figure(dpi=300)
    plt.grid()
    plt.plot(ArPlus_T, 1e9*Debye)
    plt.semilogy()
    plt.grid(which='both')
    plt.ylabel("Debye length (nm)")
    plt.xlabel("Temperature (K)")
    plt.title("Debye Length Argon")
    
    print("n Ar+", np.interp(10000,ArPlus_T,ArPlus_n))
    print("n Ar",np.interp(10000,Ar_T,Ar_n))
    
    print(np.interp(10000,ArPlus_T,1e9*Debye))
    
    plt.figure(dpi=300)
    plt.grid()
    Gamma = const.e**2/4/np.pi/const.epsilon_0/const.k/ArPlus_T*(4*np.pi/3*ArPlus_n)**(1/3)
    plt.plot(ArPlus_T, Gamma)
    plt.title("Ion-Ion coupling in a partionally ionized argon")
    plt.ylabel(r"Coupling parameter $\Gamma$")
    plt.xlabel("Temperature (K)")
    print(Gamma)
        

plot()