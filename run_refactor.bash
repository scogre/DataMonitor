#!/bin/bash --login
#module load intel/14.0.3
#module load hpss
#module load szip/2.1
#module load hdf5/1.8.9
#module load netcdf4


pattern='([[:digit:]])'

machine_path=${PWD}

streamyrs=(2003 2007 2011 2015)
allstreampath='/lustre/f1/Oar.Esrl.Nggps_psd/'
alloutpath='/lustre/f1/Scott.Gregory/'

numruns=${#streamyrs}
for i in `seq 1 $numruns`; do
    echo 'modelrun='${streamyrs[$i-1]}'stream'
    modelrun=${streamyrs[$i-1]}'stream'
    fullmodelpath=$allstreampath$modelrun'/'
    echo $fullmodelpath
    outputpath=$alloutpath'FV3s'${streamyrs[$i-1]}'/'
    echo $outputpath
    listfilename='latestlist_FV3s'${streamyrs[$i-1]}'.txt'


    rmlistofdir='rm '$listfilename
    $rmlistofdir
    rm dates10dig_FV3s${streamyrs[$i-1]}.txt
    rm mergedates10dig_FV3s${streamyrs[$i-1]}.txt


    ls -1 $fullmodelpath > $listfilename

    count=0
    while read -r line
    do
            name="$line"
            NUMBERzz=$(echo $name | tr -dc $pattern)
            lennum=${#NUMBERzz}
            if [ $lennum -gt 9 ]; then
               date10[$count]=${NUMBERzz:$lennum-10:10}
               date8[$count]=${date10[$count]:0:8}
               #echo ${date10[$count]}
               echo ${date10[$count]} >> 'dates10dig_FV3s'${streamyrs[$i-1]}'.txt'
               ((count++))
            fi
            unset NUMBERzz
            unset lennum
    done < "$listfilename"

    $rmlistofdir

    echo LASTONE= ${date10[$count-1]}

    count=0
    for x in `ls -1 -d "$outputpath"bufr2nc*`; do
          NUMBERzz=$(echo $x | tr -dc $pattern)
          lennum=${#NUMBERzz}
          date10B[$count]=${NUMBERzz:$lennum-10:10}
          date8B[$count]=${date10B[$count]:0:8}
          #echo ${date10B[$count]}
          echo ${date10B[$count]} >> 'mergedates10dig_FV3s'${streamyrs[$i-1]}'.txt'
          ((count++))
    done
    echo LASTONEMERGED= ${date10B[$count-1]}

    uniqcount=0
    for date in ${date10[*]}; do
            uniqdate=$date
            for dateB in ${date10B[*]}; do
                    if [ $date = $dateB ]
                    then
                            uniqdate=0
                            continue
                    fi
            done
            if [ $uniqdate -gt 0 ];
            then
                    #echo unique date= $uniqdate
                    uniqcount=$uniqcount+1
                    uniqindx=$uniqcount-1
                    date10dig[$uniqindx]=$date
            fi
    done
    #echo unique= ${date10dig[*]}
    echo num modeldates= ${#date10[*]}
    echo num to merge= ${#date10dig[*]}

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

################### ALL of the processing action is kicked off with the 'date10dig' list of dates

    unset date10dig
    unset date8
    unset date8B
    unset date10
    unset date10B
    unset uniqdate
    unset uniqcount
    unset dateB
    unset NUMBERzz

done






