#!/bin/bash

### need to sort out the variable inputs
yearruns=('2003' '2007' '2011' '2015')
count=0
for Y in "${yearruns[@]}"
do
   YEARRUN=$Y
   echo YRRUN=$YEARRUN
   echo $count
   echo "$Y"
   ((count++))
   ANNFILES=$(ls -1d /lustre/f1/Scott.Gregory/FV3s$YEARRUN/FV3s$YEARRUN*nc)
   #echo $ANNFILES
   echo numfile=${#ANNFILES}
   for file in ${ANNFILES[*]}; do
      echo file=$file
   done
done


