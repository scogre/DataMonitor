#!/bin/sh
#PBS -l partition=sjet:vjet
#PBS -l procs=1
#PBS -l walltime=6:00:00
#PBS -A gfsenkf
#PBS -N fillreanl

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
else
  analdate_end=$3
fi

echo 'Processing dates from ' $analdate_start ' to ' $analdate_end ' in stream ' $streamyr

#python /lustre/f1/unswept/Anna.V.Shlyaeva/DataMonitor/RAD/fillin_year_reanl.py ${streamyr} ${analdate_start} ${analdate_end}
