#!/bin/bash
#SBATCH --job-name benchmark
#SBATCH --qos normal
#SBATCH --account=tutorial1
#SBATCH --nodes 3
#SBATCH --ntasks-per-node 24
#SBATCH --time 00:15:00
#SBATCH --mail-type=all
#SBATCH --export=NONE
#SBATCH --threads-per-core=1
#SBATCH --reservation=rc-tutorial

# This job will make some movies -- clean out data
# to avoid partial/interrupted movies
rm Shell_Avgs/*
rm Shell_Slices/*

ml purge


#Submit the movie-making job
#That job depends on the current job (SLURM_JOBID) having completed

#ml slurm/blanca
sbatch --dependency=afterany:$SLURM_JOBID render_eq_movie.sh
sbatch --dependency=afterany:$SLURM_JOBID render_shell_movie.sh

ml intel impi mkl
export OMP_NUM_THREADS=1
mpirun -np 64 ./rayleigh.opt -nprow 8 -npcol 8
