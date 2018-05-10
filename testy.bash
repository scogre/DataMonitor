#!/bin/bash
### need to sort out the variable inputs

yearruns=('2003' '2007' '2011' '2015')
count=0
outpath='/lustre/f1/Scott.Gregory/'
for Y in "${yearruns[@]}"
do
   YEARRUN=$Y
   echo YRRUN=$YEARRUN
   echo $count
   echo "$Y"
   ((count++))

   RAD_ANNFILES=$(ls -1d /lustre/f1/Scott.Gregory/FV3s$YEARRUN/RAD*FV3s$YEARRUN*nc)
   #echo $RAD_ANNFILES
   numfile=${#RAD_ANNFILES}
   echo numfile=${#RAD_ANNFILES}
   if [ "$numfile" == "0" ]
   then
      echo 'making blanks for '$streamyr
      makeblanks='python RAD/make_rad_annual_all.py '$YEARRUN' '$YEARRUN' '$outpath
      $makeblanks
      RAD_ANNFILES=$(ls -1d /lustre/f1/Scott.Gregory/FV3s$YEARRUN/RAD*FV3s$YEARRUN*nc)
      #echo $RAD_ANNFILES
      numfile=${#RAD_ANNFILES}
      echo numfile=${#RAD_ANNFILES}
   fi
   echo first is ${RAD_ANNFILES:0:22}
done



