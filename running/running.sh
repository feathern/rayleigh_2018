#!/bin/bash
#SBATCH --job-name running
#SBATCH --qos normal
#SBATCH --account=tutorial1
#SBATCH --nodes 3
#SBATCH --ntasks-per-node 24
#SBATCH --time 00:15:00
#SBATCH --mail-type=all
#SBATCH --export=NONE
#SBATCH --threads-per-core=1
#SBATCH --reservation=rc-tutorial


ml purge


ml intel impi mkl
export OMP_NUM_THREADS=1
mpirun -np 64 ./rayleigh.opt
