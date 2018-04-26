#!/bin/bash

###################################################################
YEARRUN=2007
STARTMODAHR=032000
startdate10dig=$YEARRUN$STARTMODAHR
windowlen_days=10
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

startdate_nohour=${startdate10dig:0:8}
startdate_nohour_seconds=$(date -d $startdate_nohour "+%s")
echo $startdate_nohour_seconds
startdate_hour=${startdate10dig:8:2}
startdate_hour_seconds=$((startdate_hour*60*60))
echo $startdate_hour_seconds
startdate_seconds=$((startdate_nohour_seconds + startdate_hour_seconds))
echo $startdate_seconds


startdate_check=$(date +%Y%m%d%H -d "1970-01-01 $startdate_seconds sec GMT")
echo startcheck= $startdate_check

endseconds=$((startdate_seconds+windowlen_days*60*60*24))

enddate_yrmodahr=$(date +%Y%m%d%H -d "1970-01-01 $endseconds sec GMT")
echo enddate_yrmodahr= $enddate_yrmodahr


datesec=$startdate_seconds
count=0
while [ $datesec -lt $endseconds ]; do
        date10dig[$count]=$(date +%Y%m%d%H -d "1970-01-01 $datesec sec GMT")
        hour[$count]=${date10dig[$count]:8:2}
        #echo hour= ${hour[$count]}
        datesec=$((datesec+hourincremnt*60*60))
        ((count++))
done
echo ${hour[*]}
echo FORWARD ${date10dig[*]}


########################################################################################################
putcode='/ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/RAD/put_all.py'

for date in ${date10dig[*]}; do
   echo python $putcode $YEARRUN $date
   python $putcode $YEARRUN $date
done



