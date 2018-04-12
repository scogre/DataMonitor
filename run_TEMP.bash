#!/bin/bash

###################################################################
#startdate10dig=2015010100
startdate10dig=2015010100
windowlen_days=31
hourincremnt=6

#STREAM 1... 1999->
#diagpath='/3year/NCEPDEV/GEFSRR/Sherrie.Fredrick/C96_fv3reanl/'
#outputpath='/lfs3/projects/gfsenkf/Scott.Gregory/FV3s1999/'
#CFSRpath='/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
#listfilename=latestlist_FV3s1999.txt

##STREAM 2... 2000->
#diagpath='/3year/NCEPDEV/GEFSRR/Gary.Bates/C96_fv3reanl/'
#outputpath='/lfs3/projects/gfsenkf/Scott.Gregory/FV3s2000/'
#CFSRpath='/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
#listfilename=latestlist_FV3s2000.txt

#2001: /3year/NCEPDEV/GEFSRR/Sherrie.Fredrick/2001_C96_fv3reanl/ /lfs3/projects/gfsenkf/Scott.Gregory/FV3s2001
#diagpath='/3year/NCEPDEV/GEFSRR/Sherrie.Fredrick/2001_C96_fv3reanl/'
#outputpath='/lfs3/projects/gfsenkf/Scott.Gregory/FV3s2001/'
#CFSRpath='/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
#listfilename=latestlist_FV3s2001.txt

##2005:
diagpath='/3year/NCEPDEV/GEFSRR/Gary.Bates/2005_C96_fv3reanl/'
outputpath='/lfs3/projects/gfsenkf/Scott.Gregory/FV3s2005/'
CFSRpath='/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
listfilename=latestlist_FV3s2005.txt

##2010: /3year/NCEPDEV/GEFSRR/Gary.Bates/2010_C96_fv3reanl/ /lfs3/projects/gfsenkf/Scott.Gregory/FV3s2010
#diagpath='/3year/NCEPDEV/GEFSRR/Gary.Bates/2010_C96_fv3reanl/'
#outputpath='/lfs3/projects/gfsenkf/Scott.Gregory/FV3s2010/'
#CFSRpath='/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
#listfilename=latestlist_FV3s2010.txt

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
while [ $datesec -le $endseconds ]; do
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

#######################################################################################################
count=0
###################################################################
startdir=${PWD}
echo starting place $startdir
#cd $outputpath
cd $CFSRpath
echo working place${PWD}

for date in ${date10dig[*]}; do
        hr=${hour[$count]}        
#        if [ -d $CFSRpath$date/ ] #if directory exists
#         then
#          echo "have CFSR diag, no htar"
#        else
#          echo directory $date doesnot exist
#          bash /misc/whome/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/CFSRextract_single.bash $date $CFSRpath
#        fi


	echo HOUR IS $hr
	if [ "$hr" -eq "00" ];

	then
                QSUB='qsub -A gfsenkf -lpartition=xjet -lwalltime=8:00:00 -lvmem=16G -lnodes=1 -venddate10dig='$date',outpath='$CFSRpath' /misc/whome/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/makeALL_plotdata_CFSR_NEWnobufr.bash'
                echo $QSUB
                $QSUB
	fi
        ((count++))
done
cd $startdir

