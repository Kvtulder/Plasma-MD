# Plasma-MD

Molecular dynamics (MD) simulation scripts for partially ionized, weakly coupled argon and xenon plasmas, developed as part of an MSc thesis on transport properties of partially ionized argon plasma. LAMMPS is used to compute self-diffusion, viscosity, and thermal conductivity via Green-Kubo/Einstein relations (through the OCTP plugin), which are compared against predictions from Chapman-Enskog kinetic theory.

## Background

In a partially ionized plasma, transport properties (viscosity, diffusion, thermal conductivity) can be predicted from Chapman-Enskog kinetic theory using pairwise interaction potentials and their associated collision integrals. This project verifies those kinetic-theory predictions with equilibrium MD simulations of explicit ions and neutrals, using implicit electrons through Debye screening of the ion-ion interaction.

Two elements are simulated (argon and xenon), each in two conditions:
- **nonionized** — a neutral, non-ionized gas, used as a baseline case
- **ionized** — a partially ionized gas with explicit ions and neutrals

The two workflows in this repository correspond to the two theoretical approaches:
- `chapmanenskog.py` — analytical/numerical route (kinetic theory, collision integrals)
- `Argon/`, `xenon/` — numerical route (LAMMPS MD simulations)

## Repository structure

```
Plasma-MD/
├── chapmanenskog.py           # Collision integral / kinetic theory solver
├── Argon/
│   ├── ionized/                # Partially ionized argon (Ar, Ar+)
│   │   ├── simulation.lammps   # LAMMPS input script
│   │   ├── forcefield.data     # Pair potentials (Yukawa + Morse)
│   │   ├── data.lmp            # Initial configuration / topology
│   │   └── job.sh              # SLURM batch script
│   └── nonionized/             # Neutral argon baseline
│       ├── simulation.lammps
│       ├── forcefield.data     # Morse potential only
│       ├── data.lmp
│       └── job.sh
└── xenon/
    ├── ionized/                 # Partially ionized xenon (Xe, Xe+)
    │   ├── simulation.lammps
    │   ├── forcefield.data      # Yukawa + Buckingham
    │   ├── data.lmp
    │   └── job.sh
    └── nonionized/              # Neutral xenon baseline
        ├── simulation.lammps
        ├── forcefield.data      # Buckingham potential only
        ├── data.lmp
        └── job.sh
```

## Chapman-Enskog collision integral solver (`chapmanenskog.py`)

Computes reduced collision integrals Ω^(l,s) from a chosen interaction potential by numerically solving the classical scattering deflection angle, following Laricchiuta et al. (equations 1, 2, and 3) and the Chapman-Enskog transport expressions from Kee, Coltrin & Glarborg (*Chemically Reacting Flow: Theory and Practice*).

- Supported reduced potentials: Lennard-Jones, Morse, Yukawa (screened Coulomb), inverse power law, exponential repulsive, and hard sphere (sanity check).
- Numerically solves for the distance of closest approach, then integrates the deflection angle, the Q(l) integral, and the Ω(l,s) collision integral over a Maxwellian velocity distribution.
- Provides `Viscosity()` and `Diffusion()` functions to convert collision integrals into transport coefficients.
- Some integrals produce convergence warnings near their bounds; this is expected and does not noticeably affect the resulting values relative to literature.

Set the `Potential` variable to select the interaction model, then run the script directly; results (Ω(1,1) as a function of reduced temperature) are appended to `outputMors.txt`.

## LAMMPS MD simulations (`Argon/`, `xenon/`)

Each `simulation.lammps` script runs the same staged equilibration/production pipeline:

1. **Minimization** — conjugate-gradient energy minimization of the initial configuration
2. **NPT initialization & equilibration** — ramped timesteps to relax the system, then equilibrate at target temperature and pressure (1 atm)
3. **NPT production** — average system volume is recorded and used to rescale the simulation box
4. **NVT initialization & equilibration** — the volume-rescaled system is equilibrated at fixed volume
5. **NVT production** — the average kinetic energy is used to rescale velocities to the target temperature
6. **NVE initialization & equilibration** — microcanonical equilibration
7. **NVE production** — self-diffusion, shear/bulk viscosity, and thermal conductivity are computed on the fly using the [OCTP plugin](https://github.com/omoultosEthTuDelft/OCTP) (order-n algorithm), and trajectories are dumped for post-processing

The ionized cases use `atom_style full` with two atom types (neutral and singly ionized), integrated with `comm_modify mode multi` for the mixed-mass system.

### Interaction potentials

| System | Neutral–neutral / Ion–neutral | Ion–ion |
|---|---|---|
| Argon | Morse | Yukawa (screened Coulomb) |
| Xenon | Buckingham | Yukawa (screened Coulomb) |

The ion-ion interaction is modeled as a screened Coulomb (Yukawa) potential to implicitly account for electron screening (Debye shielding) without simulating electrons explicitly. Neutral-neutral and ion-neutral interactions use element-specific empirical potentials (Morse for argon, Buckingham for xenon).

### Running a simulation

Each case directory is self-contained. From within e.g. `Argon/ionized/`:

```bash
lmp -in simulation.lammps
```

`job.sh` is a SLURM submission script (configured for the TU Delft DelftBlue cluster) that stages files to node-local scratch, runs LAMMPS, and syncs results back on completion or interruption.

### Simulation conditions

| System | Case | Temperature (K) | Atoms |
|---|---|---|---|
| Argon | nonionized | 1000 | 2000 |
| Argon | ionized | 13500 | 150 |
| Xenon | nonionized | 3000 | 2000 |
| Xenon | ionized | 13000 | 150 |
