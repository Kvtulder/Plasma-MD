# Details on saved numpy arrays

Be a bit carefull when using these files. I've tried to check everything but I'm not one hunder percent sure if everything is correct. Please double check data with the plots used in my thesis to be sure.

## argondiffusion.npy
Contains 4 arrays. The first array is the temperatures, the second the mean diffusion of neutral argon in m^2/s. Std contains the standard deviation of the values and success the number of successful simulations: simulations where a powerlaw slope of 1 was found with a maximum deviation of 5%.

Note: this file concatenates results from three different potentials at different index ranges, used by slicing in the plotting scripts rather than a separate flag array:
- `[:4]` — Lennard-Jones potential
- `[4:11]` — Morse potential
- `[11:]` — Morse + Yukawa potential (includes ion-neutral resonant charge exchange correction)

### Example script
```python
with open('argondiffusion.npy', 'rb') as f:
    temps = np.load(f)
    mean = np.load(f)
    std = np.load(f)
    success = np.load(f)
```

## argonplusdiffusion.npy
Same as argondiffusion but for the positively charged Ar+ ion.

### Example script
```python
with open('argonplusdiffusion.npy', 'rb') as f:
    tempsion = np.load(f)
    meanion = np.load(f)
    stdion = np.load(f)
    succession = np.load(f)
```

## chapmanenskog-diffusion.npy
Contains the diffusion values calculated with Chapman-Enskog theory for the Lennard-Jones and Morse potentials.

### Example script
```python
with open('chapmanenskog-diffusion.npy', 'rb') as f:
    LJtemps = np.load(f)
    LJCE = np.load(f)
    Morsetemps = np.load(f)
    MorseCE = np.load(f)
```

## argonplusLJdiffusion.npy *(recommend renaming to argonLJdiffusion.npy)*
Same 4-array structure as argondiffusion, but for **neutral** argon simulated with the Lennard-Jones potential specifically (contrast with argondiffusion.npy, which mixes LJ, Morse, and Morse+Yukawa results in one file by index range). Confirmed as neutral Ar, not Ar+, from the plot legend (`'Ar LJ MD'`).

### Example script
```python
with open('argonplusLJdiffusion.npy', 'rb') as f:
    temps = np.load(f)
    mean = np.load(f)
    std = np.load(f)
    success = np.load(f)
```

## argonplusLJviscosity.npy *(recommend renaming to argonLJviscosity.npy)*
Same as argonplusLJdiffusion, but containing viscosity values instead of diffusion. Also confirmed as neutral Ar via the plot legend.

### Example script
```python
with open('argonplusLJviscosity.npy', 'rb') as f:
    tempsvis = np.load(f)
    meanvis = np.load(f)
    stdvis = np.load(f)
    successvis = np.load(f)
```

## argonviscosity.npy
Same 4-array structure and index/threshold-slicing convention as argondiffusion.npy, but for neutral argon viscosity in Pa·s. Sliced in the plotting scripts as:
- `temps < 3000` — Lennard-Jones potential
- `temps <= 10000` — Morse potential
- full array — Morse + Yukawa potential

### Example script
```python
with open('argonviscosity.npy', 'rb') as f:
    temps = np.load(f)
    mean = np.load(f)
    std = np.load(f)
    success = np.load(f)
```

## chapmanenskog-viscosity.npy
Same as chapmanenskog-diffusion, but containing the Chapman-Enskog viscosity values for the Lennard-Jones and Morse potentials.

### Example script
```python
with open('chapmanenskog-viscosity.npy', 'rb') as f:
    LJtemps_vis = np.load(f)
    LJCE_vis = np.load(f)
    Morsetemps_vis = np.load(f)
    MorseCE_vis = np.load(f)
```

## argondensity.npy
Contains 2 arrays: temperatures and the corresponding MD-simulated argon mass density in kg/m^3. Used to check deviation from ideal gas behaviour and, in diffusionplotwithcorrections.py, to correct the Morse-potential Chapman-Enskog diffusion curve for non-ideal density effects.

### Example script
```python
with open('argondensity.npy', 'rb') as f:
    temps = np.load(f)
    density = np.load(f)
```

## debyelength.npy
Contains 3 arrays: Ar+ temperature, the corresponding Debye length (screening length) in meters, and the Ar+ number density in m^-3. Used to compute ion partial pressure and as the screening-length parameter (sigma) for the Yukawa-potential Chapman-Enskog ion transport calculations.

### Example script
```python
with open('debyelength.npy', 'rb') as f:
    ArPlus_T = np.load(f)
    Debye = np.load(f)
    ArPlus_n = np.load(f)
```

## chen.npy
Contains 2 arrays: temperatures and viscosity values, digitized from experimental reference data (Chen et al.) used as a literature comparison point on the viscosity plots.

### Example script
```python
with open('chen.npy', 'rb') as f:
    tempschen = np.load(f)
    vischen = np.load(f)
```