#!/bin/bash
module load PythonEnv-noaa
module load cray-hdf5
module load cray-netcdf
module load gcp
module load hpcrpt
module load alcrpt
#module load moab/stub
#module use -a /ncrc/home2/fms/local/modulefiles
#source /etc/profile.d/moab.csh 

years=('1999' '2003' '2007' '2011' '2015')
#datayrs1=('1999' '2003' '2007' '2011' '2015')
datayrs2=('2000' '2004' '2008' '2012' '2016')


startdir=${PWD}
run_store_dir='/lustre/f2/dev/Scott.Gregory/'
cd $run_store_dir
count=0
for yearrun in ${years[*]}; do
   datayr=${datayrs2[$count]}
   echo datayr=$datayr
   QSUB='/opt/moab/bin/msub -A nggps_psd -q ldtn -l partition=es -vyearrun='$yearrun',datayr='$datayr' /ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/find_and_put_PICKYEAR.bash'
   echo $QSUB
   $QSUB


   ((count++))
done
cd $startdir



