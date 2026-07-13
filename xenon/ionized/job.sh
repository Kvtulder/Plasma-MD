#!/bin/bash

#SBATCH --job-name="t_13000.0_run_1"
#SBATCH --partition="rome"
#SBATCH --nodes=1
#SBATCH --time=36:00:00
#SBATCH --cpus-per-task=16

start2=$(date +%s)
# check if avx512 is available
EXECUTABLE="/home/kvtulder/lammps/src/lmp_serial"

DIR1="$SLURM_SUBMIT_DIR"
DIR2="$TMPDIR/$SLURM_JOBID"

cleanup() {
    echo "[$(date)] Cleaning up: copying results back..."

    # prevent partial overwrite issues
    rsync -a "$DIR2/" "$DIR1/" || true
}

trap cleanup SIGTERM SIGINT

# Copy everything over
echo "Starting to copy"
cp -r $SLURM_SUBMIT_DIR /$TMPDIR/$SLURM_JOBID  # copy files over to tmp drive located at the node
cd /$TMPDIR/$SLURM_JOBID
rm "slurm-${SLURM_JOBID}.out"  # make sure to not have a slurm output file in the tmp drive as that write back to submit folder

srun $EXECUTABLE -in simulation.lammps # run your main executable

echo "Finished running, starting to copy back"
rsync -a "$(pwd -P)/" ${SLURM_SUBMIT_DIR}  # when writing back to submit directory, rsync is the smarter solution
rm -rf /$TMPDIR/$SLURM_JOBID  # remove file to clean up after yourself
