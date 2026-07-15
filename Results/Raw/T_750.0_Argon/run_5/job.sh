#!/bin/bash

#SBATCH --job-name="T_750.0_run_5"
#SBATCH --partition=compute
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --account=research-me-pe


start2=$(date +%s)
# check if avx512 is available
EXECUTABLE="/home/kvantulder/lammpsbig/src/lmp_mpi"

# Copy everything over
echo "Starting to copy"
cp -r $SLURM_SUBMIT_DIR /$TMPDIR/$SLURM_JOBID  # copy files over to tmp drive located at the node
cd /$TMPDIR/$SLURM_JOBID
rm "slurm-${SLURM_JOBID}.out"  # make sure to not have a slurm output file in the tmp drive as that write back to submit folder

srun $EXECUTABLE -in simulation.lammps # run your main executable

echo "Finished running, starting to copy back"
rsync -a "$(pwd -P)/" ${SLURM_SUBMIT_DIR}  # when writing back to submit directory, rsync is the smarter solution
rm -rf /$TMPDIR/$SLURM_JOBID  # remove file to clean up after yourself
# End copying

