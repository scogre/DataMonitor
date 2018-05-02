#!/bin/bash


ANNFILE='/lustre/f1/Scott.Gregory/FV3s2015/FV3s2015_2015_amsua_metop-a_GLOBL.nc'



###################################################################
YEARRUN=2015
STARTMODAHR=032000
startdate10dig=$YEARRUN$STARTMODAHR
windowlen_days=20
hourincremnt=6

diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/'$YEARRUN'stream/'
outputpath='/lustre/f1/Scott.Gregory/FV3s'$YEARRUN'/'
if [ -d $outputpath/ ] #if directory exists
then
    echo 'out directory '$outputpath' exists'
else
    echo 'making out directory '$outputpath
    mkdir -p $outputpath
fi
###################################################################
listfilename='latestlist_FV3s'$YEARRUN'.txt'
dates_in_ann_fname='date_in_ann'$YEARRUN'.txt'
rm $listfilename
rm $dates_in_ann_fname
###################################################################
###################################################################
## listing the completed model dates

ls -1d $diagpath$YEARRUN* | xargs -n 1 basename  > $listfilename

modeldates=$(ls -1d $diagpath$YEARRUN* | xargs -n 1 basename)
echo modeldates=$modeldates
#echo lenmoddates=${#modeldates}
##################################################################
###########################
fusestring=''
XX=''
for lines in `seq 1 50`; do
   language="/Full_Dates =/ {nextline=NR+$lines}{if(NR==nextline){print}}"
   XX=$(ncdump -v Full_Dates $ANNFILE |awk "$language")
   fusestring=$fusestring' '$XX
done
lenFUSE=${#fusestring}
#######
fs2=$(echo $fusestring |awk -F ',' '{for(i=1; i <= NF; ++i) print $i}')   #eliminates commas
fs3=$(echo $fs2 |awk -F ';' '{for(i=1; i <= NF; ++i) print $i}') #eliminates semicolon
fs4=$(echo $fs3 |awk -F '{' '{for(i=1; i <= NF; ++i) print $i}') #eliminates {
fs5=$(echo $fs4 |awk -F '_' '{for(i=1; i <= NF; ++i) print $i}') #eliminates _
dates_in_ann=$(echo $fs5 |awk -F '}' '{for(i=1; i <= NF; ++i) print $i}') #eliminates }
echo dates_in_ann=$dates_in_ann
printf '%s\n' $dates_in_ann > $dates_in_ann_fname
#echo lenanndates=${#dates_in_ann}






uniqcount=-1
for date in ${modeldates[*]}; do
   uniqdate=$date
   for dateB in ${dates_in_ann[*]}; do
      if [ $dateB = $date ]
      then
         echo $date not unique
         uniqdate=0
         continue
      fi
   done
   if [ $uniqdate -gt 0 ];
   then
      echo unique date= $uniqdate
      uniqcount=$uniqcount+1
      date10dig[$uniqcount]=$date
   fi
done
echo unique= ${date10dig[*]}
echo num unique= ${#date10dig[*]}



