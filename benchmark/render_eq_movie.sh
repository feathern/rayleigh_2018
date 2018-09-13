#!/bin/bash
#SBATCH --job-name eqmovie
#SBATCH --qos normal
#SBATCH --account=tutorial1
#SBATCH --partition=shas
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 24
#SBATCH --time 00:30:00
#SBATCH --mail-type=all
#SBATCH --export=NONE
#SBATCH --threads-per-core=1
#SBATCH --reservation=rc-tutorial

mkdir eq_pngs
rm eq_pngs/*
rm eq_movie.mp4

ml purge
ml intel impi
ml python/3.5.1


###################################
# Various movie control parameters

export QINDEX=501 #Render temperature
export DPI=300 # dots-per-inch (use in tandem with xypix)
export XYPIX=1024 # x-y dimensions of the movie (pixels; square aspect ratio)
export TITLE='T-$\overline{\mathrm{T}}$'
export VMIN=-0.2
export VMAX=0.2
export CBAR='(nondimensional)'

mpirun -np 24 python -u equatorial_movie.py $QINDEX $DPI $XYPIX $TITLE $VMIN $VMAX $CBAR


export PATH=/projects/feathern/software/ffmpeg/:$PATH
ffmpeg -y -framerate 30 -i './eq_pngs/%*.png' -s:v 1536:512 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p  eq_movie.mp4
