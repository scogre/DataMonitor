#!/bin/sh
#PBS -A nggps_psd
#PBS -l partition=es,size=1,walltime=5:00:00
#PBS -q rdtn
#PBS -N untar
###############PBS -e $mydatapath/sgextract_$enddate10dig.err
###############PBS -o $mydatapath/sgextract_$enddate10dig.out
#PBS -S /bin/sh
# need envars:  machine, analdate, datapath2, hsidir, save_hpss_full, save_hpss_subset




echo analdate is $enddate8dig
analdate=$enddate8dig
exptname=$exptname
mydatapath=$mydatapath
echo mydatapath is $mydatapath



#analdate=2003080100
#exptname='2003stream'
#mydatapath='/lustre/f1/Scott.Gregory/2003stream'
#echo mydatapath is $mydatapath



#source /opt/cray/pe/modules/3.2.10.5/init/sh
#module avail
source $MODULESHOME/init/sh
echo new line of text
module load hsi
echo module loaded 

export hsidir=/3year/NCEPDEV/GEFSRR/${exptname}
echo hsidir is $hsidir

##export mydatapath=/lustre/f2/scratch/Oar.Esrl.Nggps_psd/${exptname}
#export mydatapath=/lustre/f1/Scott.Gregory/${exptname}
#echo mydatapath is $mydatapath

if [ -d $mydatapath/ ] #if directory exists
then
    echo 'out directory '$mydatapath' exists'
else
    echo 'making out directory '$mydatapath
    mkdir -p $mydatapath
fi

cd ${mydatapath}


rm -rf ${analdate}'*'

hours=('00' '06' '12' '18')

for hr in ${hours[*]}; do
   echo "extract ${hsidir}/${analdate}${hr}_subset.tar"
   htar -tvf ${hsidir}/${analdate}${hr}_subset.tar
   htar -xvf ${hsidir}/${analdate}${hr}_subset.tar
   echo "extracted? ${hsidir}/${analdate}${hr}_subset.tar"
done



