#!/bin/bash

#models[0]=FV3s2010
#models[1]=FV3s2011

#models[0]=FV3s1999
#models[1]=FV3s2000
#models[2]=FV3s2001
#models[3]=FV3s2003
#models[4]=FV3s2005
#models[5]=FV3s2007
#models[6]=FV3s2010
#models[7]=FV3s2011
#models[8]=FV3s2015
#models[9]=CFSR


#models[0]=FV3s2015
#models[1]=CFSR


models[0]=FV3s1999
models[1]=FV3s2003
models[2]=FV3s2007
models[3]=FV3s2011
models[4]=FV3s2015
models[5]=CFSR


bash /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/makeOVERLAPconv.bash ${models[*]}

makemocode='/httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/make_CONV_automonths.bash' #has all variables

for model in ${models[*]}; do
        
        echo $model
        count=0
        for x in `ls -1 /Projects/gefsrr/prep_plotdata_$model/prep_plotdata*00_GLOBL.nc`; do
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
        lastdatefile='/httpd-test/psd/forecast-modeling/gefsrr/data_assim/CONV/lastdate_conv_'$model'.txt'
        echo $lastdatefile
        rm $lastdatefile
        echo $lastdate >> $lastdatefile
        echo $lastdate
        
        prevlastdatefile='/httpd-test/psd/forecast-modeling/gefsrr/data_assim/CONV/prevlastdate_conv_'$model'.txt'
        if [ -f $prevlastdatefile ];
        then
                while read -r line
                do
                        prevlastdate="$line"
                        echo 'prevlastdate='$prevlastdate
                done < $prevlastdatefile
        
        else
                echo 'making prevlastdate'
                let prevlastdate="$lastdate-10000" #subtracted one just to make them NOT EQUAL EACH other
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
##################        
                runm0="bash $makemocode $model $m0 $y0"
                $runm0
		prevmonthaccumfile='/Projects/gefsrr/prep_plotdata_'$model'/Q_'$yprev'_'$mprev2dig'_GLOBL.nc' #check with Q,GLOBL
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
##################
                runCFSR_m0="bash $makemocode CFSR $m0 $y0"
                $runCFSR_m0
                prevmonthaccumfile='/Projects/gefsrr/prep_plotdata_CFSR/Q_'$yprev'_'$mprev2dig'_GLOBL.nc' #check with Q,GLOBL
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
        #python /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/CONV/conv_autoplot_subprocess.py $lastdatefile $model
        python /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/CONV/conv_autoplot_subprocess_TESTINGnoBUFR.py $lastdatefile $model
#        rm $lastdatefile
#        rm $prevlastdatefile
done



