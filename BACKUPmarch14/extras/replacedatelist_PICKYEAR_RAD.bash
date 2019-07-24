#!/bin/bash
### need to sort out the variable inputs
module load PythonEnv-noaa
module load cray-hdf5
module load cray-netcdf
module load gcp
module load hpcrpt
module load alcrpt
#module load moab
#module load moab/stub
#module use -a /ncrc/home2/fms/local/modulefiles
#source /etc/profile.d/moab.csh 

#yearruns=('1999' '2003' '2007' '2011' '2015')
#datayrs=('1999' '2003' '2007' '2011' '2015')
yearruns=$yearrun
datayrs=$datayr
count=0
outpath='/lustre/f2/dev/Scott.Gregory/'




modahr=(122000 122006 122012 122018 122100 122106 122112 122118 122200 122206 122212 122218 122300 122306 122312 122318 122400 122406 122412 122418 122500 122506 122512 122518 122600 122606 122612 122618 122700 122706 122712 122718 122800 122806 122812 122818 122900 122906 122912 122918 123000 123006 123012 123018 123100 123106 123112 123118)





for Y in "${yearruns[@]}"
do
   modelname=FV3s$Y
   YEARRUN=$Y
   echo YRRUN=$YEARRUN
   echo $count
   echo "$Y"

   ###################################################################
   diagpath='/lustre/f2/scratch/Oar.Esrl.Nggps_psd/'$YEARRUN'stream/'
   #diagpath=$outpath$YEARRUN'stream/' ### when I download from the hpss
   #diagpath='/lustre/f2/dev/Scott.Gregory/'$YEARRUN'stream/'
   #diagpath='/lustre/f2/dev/Anna.V.Shlyaeva/fv3reanl_diag/'
   echo diagpath is $diagpath
   ###################################################################

   ###################################################################
   outputpath=$outpath$modelname'/'
   ###################################################################
 
   ################################################################################################################
   RADputcode='/ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/RAD/put_all.py'
   CONVputcode='/ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/CONV/call_putdate_CONV.py'
   for mdh in ${modahr[*]}; do
      date=$Y$mdh
      echo running $date

      echo python $RADputcode $modelname $date $outputpath $diagpath
      echo 'date='$date
      python $RADputcode $modelname $date $outputpath $diagpath

      #echo python $CONVputcode $modelname $date $outputpath $diagpath
      #echo 'date='$date
      #python $CONVputcode $modelname $date $outputpath $diagpath
   done
   unset date10dig
   unset date
   ################################################################################################################
   break #this will break it out of the looping over all ANNFILES because all of that looping will happen in the subroutines
   cp $outputpath/RAD*nc /lustre/f2/dev/Scott.Gregory/transferDIR/.
   cp $outputpath/CONV*nc /lustre/f2/dev/Scott.Gregory/transferDIR/.
   cd /lustre/f2/dev/Scott.Gregory/transferDIR/
   tar -czvpf RADannuals.tar.gz RAD_*nc
   gcp -v RADannuals.tar.gz jet:/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/.
   #tar -czvpf CONVannuals.tar.gz CONV_*nc
   #gcp -v CONVannuals.tar.gz jet:/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/.
   unset outputpath
   unset diagpath
   unset RAD_ANNFILES
   unset CONV_ANNFILES
   ((count++))
done
