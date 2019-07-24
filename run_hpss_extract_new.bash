#!/bin/bash
#################20070311002015030807##################################################
YEARRUN=2007
#STARTMODAHR=021800
STARTYR=2008
STARTMODAHR=080400
startdate10dig=$STARTYR$STARTMODAHR
windowlen_days=1
hourincremnt=6
#hourincremnt=24

exptname=$YEARRUN'stream'

#diagpath='/lustre/f2/scratch/Oar.Esrl.Nggps_psd/'$YEARRUN'stream/'
#mydatapath='/lustre/f1/Scott.Gregory/'${exptname}'_B'
mydatapath='/lustre/f2/dev/Scott.Gregory/'${exptname}
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
        hr=${hour[$count]}
        if [ "$hr" -eq "07" ] || [ "$hr" -eq "13" ];
           then
           datesec=$((datesec-1*60*60))
           date10dig[$count]=$(date +%Y%m%d%H -d "1970-01-01 $datesec sec GMT")
           hour[$count]=${date10dig[$count]:8:2}
        elif [ "$hr" -eq "19" ] || [ "$hr" -eq "01" ]
           then
           datesec=$((datesec-1*60*60))
           date10dig[$count]=$(date +%Y%m%d%H -d "1970-01-01 $datesec sec GMT")
           hour[$count]=${date10dig[$count]:8:2}
        elif [ "$hr" -eq "05" ] || [ "$hr" -eq "11" ]
           then
           datesec=$((datesec+1*60*60))
           date10dig[$count]=$(date +%Y%m%d%H -d "1970-01-01 $datesec sec GMT")
           hour[$count]=${date10dig[$count]:8:2}
        elif [ "$hr" -eq "17" ] || [ "$hr" -eq "23" ]
           then
           datesec=$((datesec+1*60*60))
           date10dig[$count]=$(date +%Y%m%d%H -d "1970-01-01 $datesec sec GMT")
           hour[$count]=${date10dig[$count]:8:2}
        fi 

        #echo hour= ${hour[$count]}
        datesec=$((datesec+hourincremnt*60*60))
        ((count++))
done
echo ${hour[*]}
echo FORWARD ${date10dig[*]}


########################################################################################################
#######################################################################################################
count=0
###################################################################
startdir=${PWD}
echo starting place $startdir

if [ -d $mydatapath/ ] #if directory exists
then
    echo 'out directory '$mydatapath' exists'
else
    echo 'making out directory '$mydatapath
    mkdir -p $mydatapath
fi



cd $mydatapath
echo working place${PWD}


for date in ${date10dig[*]}; do
   hr=${hour[$count]}        
   echo date IS $date
   echo HOUR IS $hr
#   MSUB='msub -A nggps_psd -q urgent -lpartition=c4 -lwalltime=5:00:00 -N untar -e sgextract_'$date'.err -o sgextract_'$date'.out -S /bin/csh -venddate10dig='$date',exptname='$exptname',mydatapath='$mydatapath' /ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/get_sgextract.sh'
   MSUB='msub -venddate10dig='$date',exptname='$exptname',mydatapath='$mydatapath' /ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/get_sgextract_new.sh'
   echo $MSUB
   $MSUB
done

cd $startdir

