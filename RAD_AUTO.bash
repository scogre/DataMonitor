#!/bin/bash
#models[1]=CFSR
models[0]=FV3s1999
models[1]=FV3s2003
models[2]=FV3s2007
models[3]=FV3s2011
models[4]=FV3s2015
models[5]=CFSR


#obtype=CONV_t
#bash /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/ANNUAL/DataMonitor/make_OVERLAP_ALL.bash ${models[*]} $obtype
obtype=RAD
bash /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/ANNUAL/DataMonitor/make_OVERLAP_ALL.bash ${models[*]} $obtype


/httpd-test/psd/forecast-modeling/gefsrr/data_assim/ANNUAL/datelist_RAD_OVERLAP_FV3s2011_FV3s2003.txt




for model in ${models[*]}; do
        echo $model
        #echo ls -1 /Projects/gefsrr/amsu_plotdata_$model/*plotdata*
        count=0
        for x in `ls -1 /Projects/gefsrr/amsu_plotdata_$model/*plotdata*`; do
                ((count++))
        done

        xlast=$x
        echo 'lastone='$xlast
        echo 'numfiles='$count

        pattern='([[:digit:]])'
        NUMBERzz=$(echo $xlast | tr -dc $pattern)
        echo 'zznum='$NUMBERzz

        lennum=${#NUMBERzz}
        echo 'size='$lennum

        echo ${NUMBERzz:$lennum-10:10}

        lastdate=${NUMBERzz:$lennum-10:10}
        #lastdatefile='lastdate.txt'
        #lastdatefile='/httpd-test/psd/forecast-modeling/gefsrr/data_assim/lastdate_amsu.txt'
        lastdatefile='/httpd-test/psd/forecast-modeling/gefsrr/data_assim/AMSUA/lastdate_amsu_'$model'.txt'
        echo $lastdatefile
        rm $lastdatefile
        echo $lastdate >> $lastdatefile
        echo $lastdate

done





















for model in ${models[*]}; do
	echo $model
	#echo ls -1 /Projects/gefsrr/amsu_plotdata_$model/*plotdata*
	count=0
	for x in `ls -1 /Projects/gefsrr/amsu_plotdata_$model/amsu_plotdata*00_GLOBL.nc`; do
		((count++))
	done
	
	xlast=$x
	echo 'lastone='$xlast
	echo 'numfiles='$count

	pattern='([[:digit:]])'
	NUMBERzz=$(echo $xlast | tr -dc $pattern)
	echo 'zznum='$NUMBERzz
	
	lennum=${#NUMBERzz}
	echo 'size='$lennum
	
	echo ${NUMBERzz:$lennum-10:10}
	
	lastdate=${NUMBERzz:$lennum-10:10}
        lastdatefile='/httpd-test/psd/forecast-modeling/gefsrr/data_assim/AMSUA/lastdate_amsu_'$model'.txt'
	echo $lastdatefile
	rm $lastdatefile


	echo $lastdate >> $lastdatefile
	echo $lastdate
	
        prevlastdatefile='/httpd-test/psd/forecast-modeling/gefsrr/data_assim/AMSUA/prevlastdate_amsu_'$model'.txt'
        if [ -f $prevlastdatefile ];
        then
                while read -r line
                do
                        prevlastdate="$line"
                        echo 'prevlastdate='$prevlastdate
                done < $prevlastdatefile

        else
                echo 'making prevlastdate'
                let prevlastdate="$lastdate-10000" #subtracted 10000 months NOT EQUAL EACH other
                echo 'prevdatezzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz='$prevlastdate
                echo $prevlastdate >> $prevlastdatefile
        fi

        if [ "$prevlastdate" -ne "$lastdate" ];
        then
                echo 'ALL ACTIONS GO HERE WHEN lastdate not equal to previous lastdate'
##################      
                let y0="${lastdate:0:4}"
                let m0_1="${lastdate:4:1}" #splitting the digits of month because the octal-decimal issue
                let m0_2="${lastdate:5:1}" #splitting the digits of month because the octal-decimal issue
                m02dig=${lastdate:4:2}

                if [ "$m0_1" = "0" ]
                then
                        echo firstdigitzero
                        m0=$m0_2
                else
                        m0=$m0_1$m0_2
                fi

                echo M0=$m0
                echo M0-1=$[m0-1]
###################
                let yprev=$[y0-1]
                let mprev=$[m0-1]

                echo YPREV=$yprev
                echo MPREV=$mprev
###################
                let yp="${prevlastdate:0:4}"
                let mp_1="${prevlastdate:4:1}" #splitting the digits of month because the octal-decimal issue
                let mp_2="${prevlastdate:5:1}" #splitting the digits of month because the octal-decimal issue

                echo mp1=$mp_1
                echo mp2=$mp_2

                if [ "$mp_1" = "0" ]
                then
                        echo firstdigitzero
                        mp=$mp_2
                else
                        mp=$mp_1$mp_2
                fi

                echo MPrevlastdate=$mp
                echo MPrevlastdate-1=$[mp-1]
###################
                if [ "$mprev" -eq "0" ];
                then
                        echo 'ZERO found'
                        mprev=12
                else
                        echo 'NOT ZERO'
                        yprev=$y0
                fi

                if [ $mprev -lt 10 ];
                then
                        mprev2dig='0'$mprev
                        echo LT10 MPREV2digit=$mprev2dig
                else
                        mprev2dig=$mprev
                        echo GT10 MPREV2digit=$mprev2dig
                fi



                runm0="bash $makemocode $model $m0 $y0"
                $runm0
                prevmonthaccumfile='/Projects/gefsrr/amsu_plotdata_'$model'/AMSU_'$yprev'_'$mprev2dig'_GLOBL.nc'
                #if [ ! -f $prevmonthaccumfile ]; #if file does NOT exist ... thats what the '!' is for
                echo PREVIOUS= $mp
                echo THIS= $m0
		runprev_command="bash $makemocode $model $mprev $yprev"
                if [ ! -f $prevmonthaccumfile ]; #if file does NOT exist ... thats what the '!' is for  
                then
                        echo $runprev_command
                        echo 'RUNPREV GOING'
                        $runprev_command
                else
                        if [ "$mp" -ne "$m0" ];
                        then
                                echo $runprev_command
                                echo 'RUNPREV GOING'
                                $runprev_command
                        else
                                echo 'NO RUNPREV'
                        fi
                fi

########

                runCFSR_m0="bash $makemocode CFSR $m0 $y0"
                $runCFSR_m0
                prevmonthaccumfile='/Projects/gefsrr/amsu_plotdata_CFSR/AMSU_'$yprev'_'$mprev2dig'_GLOBL.nc'
                echo 'CFSR prev='$prevmonthaccumfile
                runCFSR_mprev_command="bash $makemocode CFSR $mprev $yprev"
                if [ ! -f $prevmonthaccumfile ]; #if file does NOT exist ... thats what the '!' is for
                then
                        echo $runCFSR_mprev_command
                        $runCFSR_mprev_command
                else
                        if [ "$mp" -ne "$m0" ];
                        then
                                echo $runCFSR_mprev_command
                               $runCFSR_mprev_command
                        fi
                fi

        else
                echo 'NO month accum action necessary current date equal to previous lastdate'
        fi


       cp $lastdatefile $prevlastdatefile
       #python /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/AMSUA/amsu_autoplot_subprocess.py $lastdatefile $model
#       echo python /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/AMSUA/amsu_autoplot_subprocess_TESTINGnoBUFR_CLEAN6.py  $lastdatefile $model
#       python /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/AMSUA/amsu_autoplot_subprocess_TESTINGnoBUFR_CLEAN6.py  $lastdatefile $model
       echo python /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/AMSUA/amsu_auto_MAY30.py $lastdatefile $model
       python /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/AMSUA/amsu_auto_MAY30.py $lastdatefile $model
#       rm $lastdatefile
#       rm $prevlastdatefile
       cp /Projects/gefsrr/AUTOPLOTS/autoplotdir/images/$model/*png /httpd-test/psd/forecast-modeling/gefsrr/data_assim/AUTOPLOTS/$model/.
done




