#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --account=pi-lgagliardi
#SBATCH --cpus-per-task=24
#SBATCH --time=96:00:00
#SBATCH --mem=96G
#SBATCH --partition=lgagliardi-amd
#SBATCH --error=fe3_m500_s4.e
#SBATCH --output=fe3_m500_s4.o
#SBATCH --qos=lgagliardi

#MODULES
module use /software/modulefiles-amd
module load python

#PATHING
cd $SLURM_SUBMIT_DIR

#EXECUTION
block2main fe3_m500_s4.conf > fe3_m500_s4.out
