#!/bin/bash
module load PythonEnv-noaa
module load cray-hdf5
module load cray-netcdf
module load gcp
module load hpcrpt
module load alcrpt


/bin/bash /ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/find_and_put.bash
/bin/bash /ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/find_and_put_Yplus1.bash


startdir=${PWD}
cd /lustre/f1/Scott.Gregory/transferDIR/
tar -czvpf RADannuals.tar.gz RAD_*nc
gcp -v RADannuals.tar.gz jet:/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/.
tar -czvpf CONVannuals.tar.gz CONV_*nc
gcp -v CONVannuals.tar.gz jet:/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/.
cd $startdir


