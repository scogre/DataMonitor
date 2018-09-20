#!/bin/tcsh
source /ncrc/home1/Scott.Gregory/.tcshrc
source /etc/profile.d/moab.csh 
module load PythonEnv-noaa
module load cray-hdf5
module load cray-netcdf
module load gcp
module load hpcrpt
module load alcrpt
module load moab
module use -a /ncrc/home2/fms/local/modulefiles


startdir=${PWD}
cd /lustre/f1/unswept/Scott.Gregory/transferDIR/
tar -czvpf RADannuals.tar.gz RAD_*nc
gcp -v RADannuals.tar.gz jet:/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/.
tar -czvpf CONVannuals.tar.gz CONV_*nc
gcp -v CONVannuals.tar.gz jet:/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/.
cd $startdir


