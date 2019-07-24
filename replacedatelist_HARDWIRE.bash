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
yearruns=('1999')
datayrs=('2000')
count=0
outpath='/lustre/f2/dev/Scott.Gregory/'

startdir=${PWD}
run_store_dir='/lustre/f2/dev/Scott.Gregory/'
cd $run_store_dir



#modahr=(031500 031506 031512 031518 031600 031606 031612 031618 031700 031706 031712 031718 031800 031806 031812 031818 031900 031906 031912 031918 032000 032006 032012 032018 032100 032106 032112 032118 032200 032206 032212 032218 032300 032306 032312 032318 032400 032406 032412 032418 050500 050506 050512 050518 050600 050606 050612 050618 050700 050706 050712 050718) 
modahr=(122506 122512 122518 122600 122606 122612 122618 122700 122706 122712 122718 122800 122806 122812 122818 122900 122906 122912 122918 123000 123006 123012 123018 123100 123106 123112 123118)
#modahr=(010100 010106 010112 010118 010200 010206 010212 010218 010300 010306 010312 010318 010400 010406 010412 010418 010500 010506 010512 010518 010600 010606 010612 010618 010700 010706 010712 010718 010800 010806 010812 010818 010900 010906 010912 010918 011000 011006 011012 011018 011100 011106 011112 011118 011200 011206 011212 011218 011300 011306 011312 011318 011400 011406 011412 011418 011500 011506 011512 011518 011600 011606 011612 011618 011700 011706 011712 011718 011800 011806 011812 011818 011900 011906 011912 011918 012000 012006 012012 012018 012100 012106 012112 012118 012200 012206 012212 012218 012300 012306 012312 012318 012400 012406 012412 012418 012500 012506 012512 012518 012600 012606 012612 012618 012700 012706 012712 012718 012800 012806 012812 012818 012900 012906 012912 012918 013000 013006 013012 013018 013100 013106 013112 013118 020100 020106 020112 020118 020200 020206 020212 020218 020300 020306 020312 020318 020400 020406 020412 020418 020500 020506 020512 020518 020600 020606 020612 020618 020700 020706 020712 020718 020800 020806 020812 020818 020900 020906 020912 020918 021000 021006 021012 021018) 




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
      date=${datayrs[$count]}$mdh
      echo running $date

      echo python $RADputcode $modelname $date $outputpath $diagpath
      echo 'date='$date
      python $RADputcode $modelname $date $outputpath $diagpath

      echo python $CONVputcode $modelname $date $outputpath $diagpath
      echo 'date='$date
      python $CONVputcode $modelname $date $outputpath $diagpath
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
   tar -czvpf CONVannuals.tar.gz CONV_*nc
   gcp -v CONVannuals.tar.gz jet:/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/.
   unset outputpath
   unset diagpath
   unset RAD_ANNFILES
   unset CONV_ANNFILES
   ((count++))
done

cd $startdir
