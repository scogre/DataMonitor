#!/bin/csh
#PBS -A nggps_psd
#PBS -l partition=c4
#PBS -l walltime=16:00:00
#PBS -l nodes=1
#PBS -N fillreanl
#PBS -S /bin/csh

module load PythonEnv-noaa/1.4.0
module load cray-hdf5
module load cray-netcdf
module load gcp

set scriptdir=/lustre/f1/unswept/Anna.V.Shlyaeva/DataMonitor/

foreach streamyr (1999 2003 2007 2011 2015)
  set analdate_start=${streamyr}010100
  set datapath=/lustre/f1/Oar.Esrl.Nggps_psd/${streamyr}stream/
  set analdate_end=`cat "${datapath}/analdate.csh" | awk 'NR==1{print $3}'`

  echo 'Processing dates from ' $analdate_start ' to ' $analdate_end ' in stream ' $streamyr

  python ${scriptdir}/CONV/fillin_stream_reanl_obscount.py ${streamyr} ${analdate_start} ${analdate_end}
  python ${scriptdir}/call_plot_conv_obscount.py           ${streamyr} ${analdate_start} ${analdate_end}
end
#gcp -v gaea:/lustre/f1/unswept/Anna.V.Shlyaeva/images/obscounts/*png   theia:/scratch3/BMC/gsienkf/ashlyaeva/reanalysis/obscounts/

