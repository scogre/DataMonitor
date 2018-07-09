#!/bin/bash

pattern='([[:digit:]])'

#rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_amsu_OVERLAP.txt

models=$@
echo make_OVERLAP_datelist_amsu models=${models[*]}



echo 'nummodels='${#models[@]}
modct=0
for model in ${models[*]}; do
        count=0
        countuniq=0
        countuniq_chanlist=0
        countuniq_yrmochanlist=0
        echo model working=$model
#TESTER        for x in `ls -1 /Projects/gefsrr/amsu_plotdata_$model/amsu_plotdata199901*`; do
        for x in `ls -1 /Projects/gefsrr/amsu_plotdata_$model/amsu_plotdata*00_GLOBL.nc`; do
                #ech $x
                lenx=${#x}
                lenmodelname=${#model}

                pldtstrndx=$(echo $x | grep -b -o $model | awk 'BEGIN {FS=":"}{print $1}')
                filenamestrtindx=$pldtstrndx+$lenmodelname+1
                endstring=${x:$filenamestrtindx:$lenx}

                NUMBERzz=$(echo $endstring | tr -dc $pattern)
                lennum=${#NUMBERzz}

                date10_dummy[$count]=${NUMBERzz:0:10}
                date8_dummy[$count]=${date10_dummy[$count]:0:8}
                date6_dummy[$count]=${date10_dummy[$count]:0:6}

                a=$(ncdump $x |awk '/CHANnum =/ {nextline=NR+1}{if(NR==nextline){print}}')
                lenchan=${#a}
                aa=$(echo $a |awk -F ',' '{for(i=1; i <= NF; ++i) print $i}')   #eliminates commas
                aaa=$(echo $aa |awk -F ';' '{for(i=1; i <= NF; ++i) print $i}') #eliminates semicolon
                aaaa=$(echo $aaa |awk -F '{' '{for(i=1; i <= NF; ++i) print $i}') #eliminates squigly{
                channelnumberz=$(echo $aaaa |awk -F '}' '{for(i=1; i <= NF; ++i) print $i}') #eliminates squigly}

###########################
                yrmo_and_chanz=${date6_dummy[$count]}' '$channelnumberz
                yrmoda_and_chanz=${date8_dummy[$count]}' '$channelnumberz
                lenyrmochan=${#yrmo_and_chanz}
###########################
                if [ $count -eq 0 ]
                then
                        uniquedate[$countuniq]=${date8_dummy[$count]}
                        uniq_date_chanz[$countuniq]=${date8_dummy[$count]}' '$channelnumberz
######### MARCH6               elif [ ${date8_dummy[count]} -ne ${date8_dummy[count-1]} ]
                elif [ ${date8_dummy[$count]} -ne ${date8_dummy[$count-1]} ]
                then
                        ((countuniq++))
                        uniquedate[$countuniq]=${date8_dummy[$count]}
                        uniq_date_chanz[$countuniq]=${date8_dummy[$count]}' '$channelnumberz
                fi
##########################
                if [ $count -eq 0 ]
                then
                        uniquechanlist[$countuniq_chanlist]=$channelnumberz
                elif [ "$channelnumberz" != "${uniquechanlist[$countuniq_chanlist]}" ]
                then
                        ((countuniq_chanlist++))
                        uniquechanlist[$countuniq_chanlist]=$channelnumberz
                fi
##########################
##########################
                if [ $count -eq 0 ]
                then
                        uniqueyrmochanlist[$countuniq_yrmochanlist]=$yrmo_and_chanz
                        lenyrmochanbase[$countuniq_yrmochanlist]=$lenyrmochan
                        yrmotmp=${date6_dummy[$count]}
                        chantmp=$channelnumberz
                elif [ "$yrmo_and_chanz" != "${uniqueyrmochanlist[$countuniq_yrmochanlist]}" ]
                then
############# MARCH6                       if [ $lenyrmochan -gt $lenyrmochanbase ] && [ ${date6_dummy[count]} -eq $yrmotmp ] #finds more channels for the same month
                        if [ $lenyrmochan -gt $lenyrmochanbase ] && [ ${date6_dummy[$count]} -eq $yrmotmp ] #finds more channels for the same month
                        then
                             uniqueyrmochanlist[$countuniq_yrmochanlist]=$yrmo_and_chanz #not advancing the index when month same but longer list... one list per month
                             lenyrmochanbase[$countuniq_yrmochanlist]=$lenyrmochan
                             chantmp=$channelnumberz
                             echo 'found a longer yrmochanlist'$countuniq_yrmochanlist ${uniqueyrmochanlist[$countuniq_yrmochanlist]}
#############  MARCH6                      elif [ ${date6_dummy[count]} -ne $yrmotmp ] #finds where month stays same but chanlist changes
                        elif [ ${date6_dummy[$count]} -ne $yrmotmp ] #finds where month stays same but chanlist changes
                        then
                             ((countuniq_yrmochanlist++))   #advancing the index
                             yrmotmp=${date6_dummy[$count]}
                             uniqueyrmochanlist[$countuniq_yrmochanlist]=$yrmo_and_chanz
                             lenyrmochanbase[$countuniq_yrmochanlist]=$lenyrmochan
                             echo 'found monthchange yrmochanlist'$countuniq_yrmochanlist ${uniqueyrmochanlist[$countuniq_yrmochanlist]}
                        fi
                fi
###############################
                if [ $count -eq 0 ]
                then
                        rmdatelist='rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_amsu_'$model'.txt'
                        $rmdatelist 
                        echo ${date8_dummy[$count]} >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_amsu_'$model'.txt'
                elif [ ${date8_dummy[count]} -ne ${date8_dummy[count-1]} ]
                then
                        echo ${date8_dummy[$count]} >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_amsu_'$model'.txt'
                fi
###############################
                ((count++))
        done

##########################
        len_uniqueyrmochanlist=${#uniqueyrmochanlist[*]}
        for i in `seq 0 $(($len_uniqueyrmochanlist-1))`;
        do
                echo List of yrmochan# $i ${uniqueyrmochanlist[$i]}
        done
###########
        lenALLdatechanz=${#uniq_date_chanz[*]}
        rmoldlist='rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/date8_w_chanz_'$model'.txt'
        $rmoldlist
        for i in `seq 0 $(($lenALLdatechanz-1))`;
        do
                echo ${uniq_date_chanz[$i]} >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/date8_w_chanz_'$model'.txt'
        done
##########
        b=( "${uniquedate[*]}" )
        bb=( "${uniq_date_chanz[*]}" )
        declare "date8_$model=$b" 
        declare "date8_chanz_$model=$bb" 
        unset uniquedate
        unset uniq_date_chanz
        unset date10_dummy
        unset date8_dummy
        unset date6_dummy
        unset yrmo_and_chanz
        unset yrmoda_and_chanz
        unset uniquechanlist
        unset uniqueyrmochanlist
        unset len_uniqueyrmochanlist
        unset lenALLdatechanz
        ((modct++))
done
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################




for model in ${models[*]}; do
    datesNchanz='/httpd-test/psd/forecast-modeling/gefsrr/data_assim/date8_w_chanz_'$model'.txt'
    listindx=0
    while read -r line
    do
      templist[$listindx]="$line"
      ((listindx++))
    done < "$datesNchanz"
    echo templist0=${templist[0]}
    echo templist1=${templist[1]}
    echo templist2=${templist[2]}
    echo templist3=${templist[3]}
    echo templist4=${templist[4]}
    modelA_datesname='date8_'$model
    echo  modelA_datesname=$modelA_datesname
    modelA_dates=$(eval echo "$"${modelA_datesname}"")
    echo modelA_dates= $modelA_dates
    len_modelA_dates=${#modelA_dates}
    echo len_modelA_dates=$len_modelA_dates


    for modelB in ${models[*]}; do
        modelB_datesname='date8_'$modelB
        modelB_dates=$(eval echo "$"${modelB_datesname}"")
        modelB_datesCHANZname='date8_chanz_'$modelB
        modelB_datesCHANZ=$(eval echo "$"${modelB_datesCHANZname}"")
        if [ "$modelB" != "$model" ]
        then
           rmold='rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_amsu_OVERLAP_'$model'_'$modelB'.txt'
           $rmold
           rmold2='rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_CHANZ_OVERLAP_'$model'_'$modelB'.txt'
           $rmold2
           echo modelB_dates= $modelB_dates


           dateB_indx=0
           datesNchanzB='/httpd-test/psd/forecast-modeling/gefsrr/data_assim/date8_w_chanz_'$modelB'.txt'
           while read -r line
           do
              dateB_w_chanz="$line"
              lendateBchanz=${#dateB_w_chanz}
              dateB=${dateB_w_chanz:0:8}
              echo dateBwchanz=$dateB_w_chanz
              echo dateB=$dateB
              lendateB=${#dateB}
              #echo quotespacedateBspacequote=" $dateB "
              if [[ $modelA_dates =~ "$dateB" ]] ; then
#########################
                 modelAindx=$(echo $modelA_dates | grep -b -o $dateB | awk 'BEGIN {FS=":"}{print $1}')
                 echo modelAindx=$modelAindx
                 echo dateA=${modelA_dates:$modelAindx:8}
                 chanzAindx=$modelAindx/9
                 dateA_w_chanz=${templist[$chanzAindx]}
                 echo dateAwchanz=$dateA_w_chanz
                 lendateAchanz=${#dateA_w_chanz}
##########################
                 result+=($dateB)
                 echo found overlapping
                 echo $dateB >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_amsu_OVERLAP_'$model'_'$modelB'.txt'
                 if [ $lendateBchanz -eq $lendateAchanz ] || [ $lendateBchanz -lt $lendateAchanz ] ; then
                    echo satisfied OR
                    echo dateBwchanz=$dateB_w_chanz
                    echo $dateB_w_chanz >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_CHANZ_OVERLAP_'$model'_'$modelB'.txt'
                 else
                    echo dateAwchanz=$dateA_w_chanz
                    echo OR NOT satisfied
                    echo $dateA_w_chanz >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_CHANZ_OVERLAP_'$model'_'$modelB'.txt'
                 fi
              fi
              ((dateB_indx++))
           done < "$datesNchanzB"
        fi
        #echo  ${result[@]}
    done
done







