#!/bin/sh
#PBS -A nggps_psd
#PBS -l partition=c4
#PBS -l walltime=15:00
#PBS -l nodes=1
#PBS -N fillreanlconv
#PBS -S /bin/sh

module load PythonEnv-noaa/1.4.0
module load cray-hdf5
module load cray-netcdf

echo 'fillin_reanl.sh <stream> <startdate> <enddate>'
echo 'if <enddate> is not provided, its taken from analdate in the stream'
echo 'if <startdate> is also not provided, its assumed to be the first date of the stream'

if [ $# -eq 0 ]; then
    exit
fi

streamyr=$1

if [ -z "$2" ];  then
  analdate_start=${streamyr}010100
else
  analdate_start=$2
fi

if [ -z "$3" ]; then
  datapath=/lustre/f1/Oar.Esrl.Nggps_psd/${streamyr}stream/
  analdate_end=`cat "${datapath}/analdate.csh" | awk 'NR==1{print $3}'`
  analdate_end=`/lustre/f1/unswept/Anna.V.Shlyaeva/DataMonitor/incdate.sh $analdate_end -6`
else
  analdate_end=$3
fi

echo 'Processing dates from ' $analdate_start ' to ' $analdate_end ' in stream ' $streamyr

python /lustre/f1/unswept/Anna.V.Shlyaeva/DataMonitor/CONV/fillin_stream_reanl.py ${streamyr} ${analdate_start} ${analdate_end}
