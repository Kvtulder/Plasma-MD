import matplotlib.pyplot as plt
import numpy as np

with open('argonLJdiffusion.npy', 'rb') as f:
    temps = np.load(f)
    mean = np.load(f)
    std = np.load(f)
    success = np.load(f)

with open('argonLJviscosity.npy', 'rb') as f:
    tempsvis = np.load(f)
    meanvis = np.load(f)
    stdvis = np.load(f)
    successvis = np.load(f)

with open('argondiffusion.npy', 'rb') as f:
    temps_morse = np.load(f)
    mean_morse = np.load(f)
    std_morse = np.load(f)
    success_morse = np.load(f)

with open('argonMorseViscosity.npy', 'rb') as f:
    tempsvis_morse = np.load(f)
    meanvis_morse = np.load(f)
    stdvis_morse = np.load(f)
    successvis_morse = np.load(f)

with open('chapmanenskog-viscosity.npy', 'rb') as f:
    LJtemps_vis = np.load(f)
    LJCE_vis = np.load(f)
    Morsetemps_vis = np.load(f)
    MorseCE_vis = np.load(f)

with open('chapmanenskog-diffusion.npy', 'rb') as f:
    LJtemps_diff = np.load(f)
    LJCE_diff = np.load(f)
    Morsetemps_diff = np.load(f)
    MorseCE_diff = np.load(f)

# Conversion factor: Pa·s -> cP (1 Pa·s = 1000 cP)
Pa_to_cP = 1000

fig, (ax_vis, ax_diff) = plt.subplots(1, 2, figsize=(12,4), dpi=300)
plt.rcParams.update({'font.size': 12})
fig.suptitle("Morse and LJ transport coefficients")


# --- Left: Viscosity ---
error_vis = 1.96 * stdvis / np.sqrt(successvis)
ax_vis.errorbar(tempsvis, meanvis * Pa_to_cP, yerr=error_vis * Pa_to_cP, fmt='o', capsize=4,
                color='tab:orange', label='Ar LJ MD')
error_vis_morse = 1.96 * stdvis_morse / np.sqrt(successvis_morse)
ax_vis.errorbar(tempsvis_morse, meanvis_morse * Pa_to_cP, yerr=error_vis_morse * Pa_to_cP, fmt='s', capsize=4,
                color='tab:red', label='Ar Morse MD')
ax_vis.plot(LJtemps_vis, LJCE_vis, '-', color='tab:orange', label='Ar LJ CE')
ax_vis.plot(Morsetemps_vis, MorseCE_vis, '-', color='tab:red', label='Ar Morse CE')
ax_vis.set_title("Viscosity")
ax_vis.set_xlabel("Temperature (K)")
ax_vis.set_ylabel("Viscosity (cP)")
ax_vis.set_xlim(right=10500)
ax_vis.set_ylim(top=0.3)

ax_vis.legend()
ax_vis.grid()

# --- Right: Diffusion ---
error_diff = 1.96 * std / np.sqrt(success)
ax_diff.errorbar(temps, mean, yerr=error_diff, fmt='o', capsize=4,
                 color='tab:blue', label='Ar LJ MD')
error_diff_morse = 1.96 * std_morse / np.sqrt(success_morse)
ax_diff.errorbar(temps_morse, mean_morse, yerr=error_diff_morse, fmt='s', capsize=4,
                 color='tab:green', label='Ar Morse MD')
ax_diff.plot(LJtemps_diff, LJCE_diff, '-', color='tab:blue', label='Ar LJ CE')
ax_diff.plot(Morsetemps_diff, MorseCE_diff, '-', color='tab:green', label='Ar Morse CE')
ax_diff.set_title("Diffusion")
ax_diff.set_xlabel("Temperature (K)")
ax_diff.set_ylabel("Diffusion coefficient (m²/s)")
ax_diff.set_xlim(right=10500)
ax_diff.set_ylim(top=0.01)

ax_diff.legend()
ax_diff.grid()

plt.tight_layout()
plt.savefig('transport_coefficients.png', dpi=300, bbox_inches='tight')
plt.show()