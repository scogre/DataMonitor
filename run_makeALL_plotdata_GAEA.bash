#!/bin/bash

###################################################################
YEARRUN=2015
STARTMODAHR=010100
startdate10dig=$YEARRUN$STARTMODAHR
windowlen_days=49
hourincremnt=6

diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/'$YEARRUN'stream/'
#diagpath='/lustre/f1/Gary.Bates/C128_C384_nsst/'
#diagpath='/3year/NCEPDEV/GEFSRR/Gary.Bates/2010_C96_fv3reanl/'
outputpath='/lustre/f1/Scott.Gregory/FV3s'$YEARRUN'/'
#CFSRpath='/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
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

temppath=$outputpath
normq_exec='/misc/whome/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/PREP/norm_q/norm_q'

#######################################################################################################
count=0
###################################################################
startdir=${PWD}
echo starting place $startdir
cd $outputpath
echo working place${PWD}

for date in ${date10dig[*]}; do
        hr=${hour[$count]}        

	echo HOUR IS $hr
	if [ "$hr" -eq "00" ];
#        if [ "$hr" -eq "00" ] || [ "$hr" -eq "12" ];
	then
		echo 'found one '$date 'attempting QSUB'
                MSUB='msub -A nggps_psd -q ldtn -lpartition=es -lwalltime=8:00:00 -lvmem=16G -lnodes=1 -venddate10dig='$date',outpath='$outputpath',diagpath='$diagpath' /ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/makeALL_plotdata_GAEA.bash'
		echo $MSUB
		$MSUB
	fi
        ((count++))
done
cd $startdir




