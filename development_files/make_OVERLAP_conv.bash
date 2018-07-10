#!/bin/bash

pattern='([[:digit:]])'

#rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/datelist_amsu_OVERLAP.txt

models=$@
echo make_OVERLAP_datelist_conv=${models[*]}

#ls /Projects/gefsrr/ANNUAL/CONV_t_FV3s1999_*GLOBL.nc
#RAD_FV3s2003_2003_amsua_n15_GLOBL.nc
datapath='/Projects/gefsrr/ANNUAL/'
lendatapath=${#datapath}
echo 'nummodels='${#models[@]}
modct=0
for model in ${models[*]}; do
   fileprefix=CONV_t_$model   
   lenprefix=${#fileprefix}
   
   count=0
   maxyeardummy=0
   for x in `ls -1 $datapath$fileprefix*GLOBL.nc`; do
      #echo $x
      fullname[$count]=$x      
      lenx=${#x}
      lenmodelname=${#model}
      len2yr=$lendatapath+$lenprefix
      datayr[$count]=${x:$len2yr+1:4}
      echo ${datayr[$count]}
      if [ ${datayr[$count]} -gt $maxyeardummy ]
      then
         maxyeardummy=${datayr[$count]}
         echo MAXYR=$maxyeardummy
      fi
      if [ $count -eq 0 ]; then
         minyeardummy=${datayr[$count]}
         echo MINYR=$minyeardummy
      fi
      if [ ${datayr[$count]} -le $minyeardummy ]
      then
         minyeardummy=${datayr[$count]}
         echo MINYR=$minyeardummy
      fi
      #count=$count+1   
      echo count=$count
      ((count++))
   done



   dates_in_ann_fname='date_in_ann'$model'.txt' 
   for yr in `seq $minyeardummy $maxyeardummy`;do
      echo march thru yrs $yr
      longprefix=$fileprefix'_'$yr
      for ANNFILE in `ls -1 $datapath$longprefix*GLOBL.nc`; do
         ##################################################################
         fusestring=''
         XX=''
         
         endsig=0
         gosig=0
         endpunc=';'
         lines=0
         
         while [ $endsig -eq $gosig ]; do   ###these will be not equal each other when the endpunctuation is found in the ncdump of dates
            ((lines++))
            language="/Full_Dates =/ {nextline=NR+$lines}{if(NR==nextline){print}}"
            XX=$(ncdump -v Full_Dates $ANNFILE |awk "$language")
            fusestring=$fusestring' '$XX
            junkstring=${XX%%$endpunc*}
            endsig=${#XX}
            gosig=${#junkstring}  ## gosig will equal endsig if it does NOT find the endpunc
            #echo GO=$gosig
            #echo END=$endsig
            #echo lines=$lines
            #echo fusestring=$fusestring
         done

         lenFUSE=${#fusestring}
         echo lenstr=$lenFUSE
         
         #######
         fs2=$(echo $fusestring |awk -F ',' '{for(i=1; i <= NF; ++i) print $i}')   #eliminates commas
         fs3=$(echo $fs2 |awk -F ';' '{for(i=1; i <= NF; ++i) print $i}') #eliminates semicolon
         fs4=$(echo $fs3 |awk -F '{' '{for(i=1; i <= NF; ++i) print $i}') #eliminates {
         fs5=$(echo $fs4 |awk -F '_' '{for(i=1; i <= NF; ++i) print $i}') #eliminates _
         dates_in_ann=$(echo $fs5 |awk -F '}' '{for(i=1; i <= NF; ++i) print $i}') #eliminates }
         echo dates_in_ann=$dates_in_ann
         printf '%s\n' $dates_in_ann > $dates_in_ann_fname
         ################# MATCHING DATES FROM FULL LIST ###############
         break
         lendates=${#dates_in_ann}
         echo LENDATES=$lendates
      done
   done


   numyrs2load=$((maxyeardummy-minyeardummy+1))
   if [ $numyrs2load -eq 1 ]; then 
      filefordates=${fullname[0]}
      echo filefordates=$filefordates
   fi
   unset maxyeardummy
   unset minyeardummy
   unset datayr


   ((modct++))
done




for model in ${models[*]}; do
   listindx=0
   dates_in_ann_fname='date_in_ann'$model'.txt'
   while read -r line
   do
      templist[$listindx]="$line"
      date8[$listindx]=${templist[$listindx]:0:8}
      #echo date8=${date8[$listindx]}
      ((listindx++))
   done < "$dates_in_ann_fname"

   echo date8=${date8[*]}

   for modelB in ${models[*]}; do
      listindxB=0
      dates_in_ann_fname='date_in_ann'$model'.txt'
      while read -r line
      do
         temptext="$line"
         date8B[$listindxB]=${temptext:0:8}
         #echo date8B=${date8B[$listindxB]}
         ((listindxB++))
      done < "$dates_in_ann_fname"
   done

   rmold='rm /httpd-test/psd/forecast-modeling/gefsrr/data_assim/ANNUAL/datelist_conv_OVERLAP_'$model'_'$modelB'.txt'
   $rmold
   datecount=0
   dummydate=0
   for dateA in ${date8[*]}; do
      echo dateA=$dateA
      #if [ $datecount -ne 0 ]; then
      #   if [ $dateA -eq $prevdateA ]; then
      #      break
      #   fi
      #fi
      #echo dateA=$dateA
      for dateB in ${date8B[*]}; do
         if [ $dateB -eq $dateA ]; then
            result+=($dateA)
            if [ $dateB -ne $dummydate ]; then
               echo $dateA >> '/httpd-test/psd/forecast-modeling/gefsrr/data_assim/ANNUAL/datelist_conv_OVERLAP_'$model'_'$modelB'.txt'
               echo MATCH=$dateA
               dummydate=$dateB
            fi
      #      break
         fi
      done
      prevdateA=$dateA
     ((datecount++))
   done
done







