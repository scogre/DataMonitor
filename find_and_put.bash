#!/bin/bash
### need to sort out the variable inputs
yearruns=('2003' '2007' '2011' '2015')
count=0
outpath='/lustre/f1/Scott.Gregory/'
for Y in "${yearruns[@]}"
do
   YEARRUN=$Y
   echo YRRUN=$YEARRUN
   echo $count
   echo "$Y"
   ((count++))
   ANNFILES=$(ls -1d /lustre/f1/Scott.Gregory/FV3s$YEARRUN/*FV3s$YEARRUN*nc)
   #echo $ANNFILES
   numfile=${#ANNFILES}
   echo numfile=${#ANNFILES}
   if [ "$numfile" == "0" ]
   then
      echo 'making blanks for '$streamyr
      makeblanks='python RAD/make_rad_annual_all.py '$YEARRUN' '$YEARRUN
      $makeblanks
      ANNFILES=$(ls -1d /lustre/f1/Scott.Gregory/FV3s$YEARRUN/*FV3s$YEARRUN*nc)
      #echo $ANNFILES
      numfile=${#ANNFILES}
       echo numfile=${#ANNFILES}
   fi


   ###################################################################
   diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/'$YEARRUN'stream/'
   outputpath=outpath+'FV3s'$YEARRUN'/'
   ###################################################################
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
   ## listing the completed model dates
   ls -1d $diagpath$YEARRUN* | xargs -n 1 basename  > $listfilename
   modeldates=$(ls -1d $diagpath$YEARRUN* | xargs -n 1 basename)
   echo modeldates=$modeldates
   ##################################################################



   for ANNFILE in ${ANNFILES[*]}; do
      echo ANNFILE=$ANNFILE
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
         echo GO=$gosig
         echo END=$endsig
         echo lines=$lines
         echo fusestring=$fusestring
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
      #echo lenanndates=${#dates_in_ann}
      
      
      ################# MATCHING DATES FROM FULL LIST ###############
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
      
      ###date10dig is the list of dates for adding to the annual file
      ##### then we feed this list of dates to the PUT
################################################################################################################
      RADputcode='/ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/RAD/put_all.py'
      CONVputcode='/ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/CONV/call_putdate_CONV.py'
      for date in ${date10dig[*]}; do
         #echo python $RADputcode $YEARRUN $date
         echo 'date='$date
         python $RADputcode $YEARRUN $date $outpath
         #outfile=outpath+'FV3s'+str(streamyr)+'/CONV_'+var+'_FV3s'+str(streamyr)+'_'+str(datayr)+'_'+region+'.nc'
         #python $CONVputcode $YEARRUN $date $outfile
      done
      ## outfile='/lustre/f1/Scott.Gregory/FV3s'+str(streamyr)+'/FV3s'+str(streamyr)+'_'+str(datayr)+'_'+var+'_'+region+'.nc'
      ## call_putdate_CONV( streamyr,  date, var, outfile)
      ##     put_all.py
      ###      call_putdate( streamyr, date, instrmnt, satlite)
      ###         putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)
################################################################################################################

   done
done

