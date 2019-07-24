#!/bin/sh
#PBS -l partition=sjet:vjet
#PBS -l procs=1
#PBS -l walltime=6:00:00
#PBS -A gfsenkf
#PBS -N fillcfsrconv

module load intel
module load mvapich2
module switch intel intel/14.0.3
module load hdf5
module load netcdf4

alias python="/contrib/anaconda/2.0.1/bin/python"
export PYTHONPATH="/home/Anna.V.Shlyaeva/.local/lib/python2.7/site-packages/"

python /lfs3/projects/gfsenkf/ashlyaeva/DataMonitor/CONV/fillin_year_CFSR_obscount.py $1
