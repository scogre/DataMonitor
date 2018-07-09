#!/bin/bash

pattern='([[:digit:]])'

rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_OVERLAP.txt

models=$@
echo make_OVERLAP_datelist_amsu models=${models[*]}
#models[0]=FV3s1999
#models[1]=FV3s2000
#models[2]=FV3s2001
#models[3]=FV3s2005
#models[4]=FV3s2010

echo 'nummodels='${#models[@]}
modct=0
yrcount=0
countyear=0
for model in ${models[*]}; do
        echo model=$model
	count=0
	countuniq=0
        modelnumz=$(echo $model | tr -dc $pattern)
        lenmodelnum=${#modelnumz}
        modelyears[$modct]=${modelnumz:$lenmodelnum-4:4}
        echo modelyears= ${modelyears[$modct]}
        for x in `ls -1 /Projects/gefsrr/prep_plotdata_$model/prep_plotdata*00_GLOBL.nc`; do
        #for x in `ls -1 /Projects/gefsrr/prep_plotdata_$model/prep_plotdata${modelyears[$modct]}*`; do
                #NUMBERzz[$count]=$(echo $x | tr -dc $pattern)
                NUMBERzz=$(echo $x | tr -dc $pattern)
                #echo NUMBERzz=$NUMBERzz
                lennum=${#NUMBERzz}
                date10_dummy[$count]=${NUMBERzz:$lennum-10:10}
                date8_dummy[$count]=${date10_dummy[$count]:0:8}
                year[$count]=${date10_dummy[$count]:0:4}

                if [ $count -eq 0 ]
                then
                        uniquedate[$countuniq]=${date8_dummy[$count]}
			echo 'found first'$model
                        echo ${uniquedate[$count]} >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_'$model'.txt'
                elif [ ${date8_dummy[$count]} -ne ${date8_dummy[$count-1]} ]
                then
                        ((countuniq++))
                        uniquedate[$countuniq]=${date8_dummy[$count]}
                        echo ${uniquedate[$count]} >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_'$model'.txt'
                        #echo 'found another '$countuniq ${uniquedate[$countuniq]}
                fi


                if [ $count -eq 0 ]
                then
                        unique_year[$countyear]=${year[$count]}
                elif [ ${year[$count]} -ne ${unique_year[$countyear]} ]
                then
                        ((countyear++))
                        unique_year[$countyear]=${year[$count]}
                fi

                ((count++))

        done
        echo countyears = $countyear
        echo unique years= ${unique_year[*]}

	#echo ${uniquedate[*]}
	b=( "${uniquedate[*]}" )
	#echo $b
	declare "date8_$model=$b" 
        #echo ${date8_{$model}}
        unset uniquedate
        unset date10_dummy
        unset date8_dummy
	((modct++))
done





for model in ${models[*]}; do
    tempvarb='date8_'$model
    echo tempvarb=$tempvarb
    listemp2=$(eval echo "$"${tempvarb}"") 
    echo L2= $listemp2
    for modelB in ${models[*]}; do
        tempvarbB='date8_'$modelB
        listemp3=$(eval echo "$"${tempvarbB}"")
        if [ "$modelB" != "$model" ]
        then
           rmold='rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_OVERLAP_'$model'_'$modelB'.txt'
           $rmold
           for item in ${listemp3[@]}; do
              echo item=$item
              if [[ $listemp2 =~ " $item " ]] ; then
                result+=($item)
                echo $item >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_OVERLAP_'$model'_'$modelB'.txt'
              fi
           done
        else
           rmold='rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_OVERLAP_'$model'_CFSR.txt'
           $rmold
           rmold2='rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_OVERLAP_CFSR_'$model'.txt'
           $rmold2
           for item in ${listemp3[@]}; do
              echo item=$item
              if [[ $listemp2 =~ " $item " ]] ; then
                result+=($item)
                echo $item >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_OVERLAP_'$model'_CFSR.txt'
                echo $item >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_conv_OVERLAP_CFSR_'$model'.txt'
              fi
           done

        fi
        echo  ${result[@]}
    done
done










