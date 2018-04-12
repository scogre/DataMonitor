#!/bin/bash
#ulimit -s 2048000
#ulimit -s unlimited
ulimit -f unlimited






###################################################################
enddate10dig=2002021718
outputpath='/lustre/f1/Scott.Gregory/TESTER/'
#enddate10dig=2016010106
#outputpath='/lustre/f1/Scott.Gregory/sample_binaryNC/'
###################################################################
#echo enddate is $enddate10dig
#outputpath=$outpath
#echo output path is $outputpath
#windowlen_cycles=3
windowlen_cycles=3
hourincremnt=6

###################################################################


enddate_nohour=${enddate10dig:0:8}
enddate_nohour_seconds=$(date -d $enddate_nohour "+%s")
echo $enddate_nohour_seconds
enddate_hour=${enddate10dig:8:2}
enddate_hour_seconds=$((enddate_hour*60*60))
echo $enddate_hour_seconds
enddate_seconds=$((enddate_nohour_seconds + enddate_hour_seconds))
echo $enddate_seconds


enddate_check=$(date +%Y%m%d%H -d "1970-01-01 $enddate_seconds sec GMT")
echo endcheck= $enddate_check

startseconds=$((enddate_seconds-(windowlen_cycles*hourincremnt*60*60)))

startdate_yrmodahr=$(date +%Y%m%d%H -d "1970-01-01 $startseconds sec GMT")
echo startdate_yrmodahr= $startdate_yrmodahr


datesec=$startseconds
count=0
while [ $datesec -le $enddate_seconds ]; do
        date10dig[$count]=$(date +%Y%m%d%H -d "1970-01-01 $datesec sec GMT")
        hour[$count]=${date10dig[$count]:8:2}
        #echo hour= ${hour[$count]}
        datesec=$((datesec+hourincremnt*60*60))
        ((count++))
done
echo ${hour[*]}
echo BACKWARD ${date10dig[*]}

########################################################################################################
########################################################################################################



machine_path='/ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/'
diagpath='/lustre/f1/Gary.Bates/C128_C384_nsst/'


mergevarbs=$machine_path'PREP/merge_diag_convvarbs.py'
prep_plotdatacode=$machine_path'PREP/make_NSTGplotdata.py'

pythonpath='python'
#pythonpath='/ncrc/home2/Jeffrey.S.Whitaker/anaconda2/bin/python'

temppath=$outputpath
normq_exec='/misc/whome/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/PREP/norm_q/norm_q'

#######################################################################################################
###################################################################
#######################################################################################################
count=0
###################################################################
startdir=${PWD}
echo starting place $startdir
cd $outputpath
echo working place${PWD}

for date in ${date10dig[*]}; do
        hr=${hour[$count]}
        ncoutdir[$count]=$outputpath'bufr2nc'$date'/'

#prep2nc
        convpath[$count]=$diagpath$date'/'
        prepncname[$count]=${ncoutdir[$count]}'prep'$date'.nc'

        prep_plotdataname[$count]=${ncoutdir[$count]}'prep_plotdata'$date'.nc'


        mkdir -p ${ncoutdir[$count]}

        echo $pythonpath $mergevarbs $date ${convpath[$count]} ${prepncname[$count]}
        $pythonpath $mergevarbs  $date ${convpath[$count]} ${prepncname[$count]}

        echo $pythonpath $prep_plotdatacode ${prepncname[$count]} ${prep_plotdataname[$count]}
        $pythonpath $prep_plotdatacode ${prepncname[$count]} ${prep_plotdataname[$count]}


        ((count++))
done
cd $startdir



