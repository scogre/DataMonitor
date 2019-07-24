#!/bin/sh
#PBS -A nggps_psd
#PBS -l partition=es,size=1,walltime=5:00:00
#PBS -q rdtn
#PBS -N untar100_102
###############PBS -e $mydatapath/sgextract_$enddate10dig.err
###############PBS -o $mydatapath/sgextract_$enddate10dig.out
#PBS -S /bin/sh
# need envars:  machine, analdate, datapath2, hsidir, save_hpss_full, save_hpss_subset


#source /opt/cray/pe/modules/3.2.10.5/init/sh
#module avail
#source /opt/cray/pe/modules/3.2.10.5/init/sh
source $MODULESHOME/init/sh
echo new line of text
module load hsi
echo module loaded 


startdir=${PWD}
cd /lustre/f2/dev/Scott.Gregory/forgary
mkdir exptnum100
cd exptnum100
htar -xvf /3year/NCEPDEV/GEFSRR/Scott.Gregory/1999stream/2000011100_exptnum100.tar
echo extracted 100

cd ..
mkdir exptnum101
cd exptnum101
htar -xvf /3year/NCEPDEV/GEFSRR/Scott.Gregory/1999stream/2000011100_exptnum101.tar
echo extracted 101

cd ..
mkdir exptnum102
cd exptnum102
htar -xvf /3year/NCEPDEV/GEFSRR/Scott.Gregory/1999stream/2000011100_exptnum102.tar
echo extracted 102

cd $startdir



