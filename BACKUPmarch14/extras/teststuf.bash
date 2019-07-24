#!/bin/bash
### need to sort out the variable inputs

yearruns=('1999' '2003' '2007' '2011' '2015')
datayrs=('1999' '2003' '2007' '2011' '2015')

count=0
outpath='/lustre/f1/Scott.Gregory/'
for Y in "${yearruns[@]}"
do
   modelname=FV3s$Y
   YEARRUN=$Y
   echo YRRUN=$YEARRUN
   echo $count
   echo "$Y"

   ###################################################################
   diagpath='/lustre/f2/scratch/Oar.Esrl.Nggps_psd/'$YEARRUN'stream/'
   #diagpath=$outpath$YEARRUN'stream/' ### when I download from the hpss
   echo diagpath is $diagpath
   ###################################################################

   ###################################################################
   outputpath=$outpath$modelname'/'
   ###################################################################
   if [ -d $outputpath/ ] #if directory exists
   then
      echo 'out directory '$outputpath' exists'
   else
      echo 'making out directory '$outputpath
#      mkdir -p $outputpath
   fi
   ###################################################################


   RAD_ANNFILES=$(ls -1d $outputpath/RAD*$modelname*${datayrs[$count]}*nc)
   echo $RAD_ANNFILES
   numfile=${#RAD_ANNFILES}
   echo numfile=${#RAD_ANNFILES}
   unset RAD_ANNFILES
   ((count++))
done
