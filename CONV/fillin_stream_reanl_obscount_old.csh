#!/bin/csh
#PBS -A nggps_psd
#PBS -l partition=c4
#PBS -l walltime=16:00:00
#PBS -l nodes=1
#PBS -N fillreanlconv
#PBS -S /bin/csh

module load PythonEnv-noaa/1.4.0
module load cray-hdf5
module load cray-netcdf

echo 'fillin_reanl.csh <stream> <startdate> <enddate>'
echo 'if <enddate> is not provided, its taken from analdate in the stream'
echo 'if <startdate> is also not provided, its assumed to be the first date of the stream'

if ($#argv < 1) then
  exit
endif
set dir1=$1

set streamyr=$1

if ( "$2" == "" )  then
  set analdate_start=${streamyr}010100
else
  set analdate_start=$2
endif

if ( "$3" == "" ) then
  set  datapath=/lustre/f1/Oar.Esrl.Nggps_psd/${streamyr}stream/
  set  analdate_end=`cat "${datapath}/analdate.csh" | awk 'NR==1{print $3}'`
else
  set analdate_end=$3
endif

echo 'Processing dates from ' $analdate_start ' to ' $analdate_end ' in stream ' $streamyr

python /lustre/f1/unswept/Anna.V.Shlyaeva/DataMonitor/CONV/fillin_stream_reanl_obscount_old.py ${streamyr} ${analdate_start} ${analdate_end}
