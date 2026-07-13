# -*- coding: utf-8 -*-
"""
Author: Kasper van Tulder

A script that calculates the collision integrals based on the 
kinetic gas theory. Equations are based on equation 1,2,3 and 14 from [1].

Some of the integrals do not converge properly and produce warnings. This is
expected behaviour and does not seem to influence the outcome of the integrals
when compared to literature values.

[1] Laricchiuta: Classical transport collision integrals for a Lennard-Jones 
like phenomenological model potential
[2] Kee: Chemically Reacting Flow Theory and Practice
"""

import numpy as np
from math import factorial
from scipy.integrate import quad
from scipy.optimize import root_scalar
import scipy.constants as const

# Physical contants
kB = const.k   # [m^2 kg s^-2 K^-1]

# Simulation params
Potential = "Morse"  # Choose from EXP, LJ or HS

# Define Reduced potentials
def Exponential(rstar):
    """ Returns a Reduced Repulsive Exponential potential"""
    return np.exp(-rstar)

def HS(rstar):
    """ Sanity check: Reduced Collision integral of Hard Sphere should return 1"""
    return np.inf if rstar < 1 else 0

def LJ(rstar):
    """ Returns a Reduced Lennard-Jones potential """
    return 4*((1/rstar)**12 - (1/rstar)**6)

def INV_POW(rstar, s=8.33):
    """ Inverse powerlaw potential"""
    return rstar**-s
#beta=
def Morse(rstar, beta=6.2993855242836351):
    """ Morse potential"""
    return (1 - np.exp(beta*(1 - (1 - np.log(2)/beta)*rstar)))**2 - 1

def Yukawa(rstar):
    return np.exp(-rstar)/rstar

match Potential:
    case "EXP":
        V = Exponential
    case "Yukawa":
        V = Yukawa
        int_limit = 25      # Quad limit on subdomains 
        near_zero = 1e-32   # Small number but not zero. Used to prevent zero division.
        b_max = 4          # Upper bound of Q integral (eq 2) of [1]
    case "HS":
        V = HS
        int_limit = 25      # Quad limit on subdomains 
        near_zero = 1e-32   # Small number but not zero. Used to prevent zero division.
        upper_limit = 3  # Upper domain limit in Brenth root finder
        b_max = 15          # Upper bound of Q integral (eq 2) of [1]
        lower_limit = near_zero

    case "LJ":
        V = LJ
        int_limit = 25      # Quad limit on subdomains 
        near_zero = 1e-32   # Small number but not zero. Used to prevent zero division.
        upper_limit = 3  # Upper domain limit in Brenth root finder
        b_max = 15          # Upper bound of Q integral (eq 2) of [1]
    
    case "INV_POW":
        V = INV_POW
    case "Morse":
        V = Morse
        int_limit = 25      # Quad limit on subdomains 
        near_zero = 1e-32   # Small number but not zero. Used to prevent zero division.
        lower_limit = near_zero
        upper_limit = 5e3  # Upper domain limit in Brenth root finder
        b_max = 5          # Upper bound of Q integral (eq 2) of [1]
    case _:
        print("""No valid potential defined. Choose from EXP (exponential repulsive),
              HS (Hard-Sphere), Yukawa (Screened Coulomb) or LJ (Lennard-Jones).
              """)

# Integral functions
def chi(Estar, bstar):
    """ Calculates the scattering deflection angle for a given:
        Energy E: float
        Impact parameter b: float
        molecular interaction potential V: function with rstar as argument.
        Make sure all three are reduced variables to ensure numerical stability.
    """
    def f(x):
        """ Function to solve to find upper bound of integral (rho_max)"""
        return 1.0 - (bstar**2*x**2) - V(1/x)/Estar  
    
    def int_func(rho):
        """ Integrand of equation 1 of [1] with rho = 1/r."""
        func = 1.0 - (bstar**2*rho**2) - V(1/rho)/Estar
        func = max(near_zero, func)
        return func**-.5
    
    if Potential == "EXP" or Potential == "Yukawa":
        rho_max = root_scalar(f, bracket=[near_zero, 1/bstar], method='brenth')
    else:
        rho_max = root_scalar(f, bracket=[lower_limit, upper_limit], method='brenth')
    integral, _ = quad(int_func, 0, rho_max.root, limit=int_limit)
    return np.pi - 2 * bstar * integral

def Q(Estar, l=1):
    """ Calculates the Q integral with parameter l: int (eq 2) of [1]"""
    def int_func(bstar):
        return bstar * (1 - np.cos(chi(Estar, bstar))**l)
    
    integral, _ = quad(int_func, 0, b_max, limit=int_limit)
    return 2 * np.pi * integral

def Omega(Tstar, l=1, s=1):
    """ Returns the collision integral omega(l:int,s:int) of dimensionless 
        temperature Tstar: float"""
    def int_func(gamma):
        Estar = gamma**2 * Tstar
        return gamma**(2*s+3) * Q(Estar, l) * np.exp(-gamma**2)
    
    integral, _ = quad(int_func, 0, np.inf, limit=int_limit)
    factor = 4 * (l+1)/((factorial(s+1)*(2*l+1-(-1)**l)*np.pi))
    return factor * integral

# Transport properties
def Viscosity(M, T, sigma, Omega22):
    """ Calculates the viscosity from the mass M [], Temperature T [K] and
        reduced collision integral Omega(2,2) [-]. Based on eq 12.100 from [2].
    """
    return 5*(np.pi*M*kB*T)**.5/16/np.pi/sigma**2/Omega22

def Diffusion(M, T, p, sigma, Omega11):
    """ Calculates the Binary Diffusion constant.
    """
    return 3*(2*kB**3*T**3/M)**.5/16/p/np.pi**.5/sigma**2/Omega11

Tlist = [1,2,4,6,8]
with open("outputMors.txt", "a") as f:
    for Tstar in Tlist:
        Omega11 = Omega(Tstar, l=1, s=1)
        #Omega11=0
        #Omega22 = Omega(Tstar, l=2, s=2)
        f.write("{},{},{}\n".format(Tstar, Omega11, 0))
        f.flush()
        print("{},{},{}\n".format(Tstar, Omega11, 0))
        #print("{},{},{}\n".format(Tstar, Omega11*Tstar**2, Omega22*Tstar**2))