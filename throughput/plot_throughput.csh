#!/bin/csh
cd /lustre/f2/dev/esrl/Anna.V.Shlyaeva/DataMonitor/throughput/

module load PythonEnv-noaa/1.4.0
module load cray-hdf5
module load cray-netcdf
module load gcp

sh plot_throughput.sh

python plot_throughput.py 30
