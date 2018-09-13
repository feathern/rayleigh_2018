#!/bin/bash
#SBATCH --job-name shellmovie
#SBATCH --qos normal    
#SBATCH --account=tutorial1 
#SBATCH --partition=shas      
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 24
#SBATCH --time 00:30:00
#SBATCH --mail-type=all
#SBATCH --export=NONE
#SBATCH --threads-per-core=1
#SBATCH	--reservation=rc-tutorial

export PATH="/projects/feathern/software/miniconda/bin:$PATH"
source activate myenv2
export OMP_NUM_THREADS=1

mkdir shell_pngs
rm shell_pngs/*
rm shell_movie.mp4

ml intel impi
which mpirun
echo $SLURM_NTASKS
export QINDEX=501 #Render temperature
export NBATCH=3

for i in `seq 1 ${NBATCH}`
do
xvfb-run --server-args="-screen 0 1536x768x24" mpirun -np 24 python -u shell_slice_movie.py $i $NBATCH $QINDEX
done

export PATH=/projects/feathern/software/ffmpeg/:$PATH
ffmpeg -y -framerate 30 -i './shell_pngs/%*.png' -s:v 1536x512 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p  shell_movie.mp4
