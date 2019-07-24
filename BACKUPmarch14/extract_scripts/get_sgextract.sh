#!/bin/sh

echo analdate is $enddate10dig
analdate=$enddate10dig
exptname=$exptname
mydatapath=$mydatapath
echo mydatapath is $mydatapath



#source /opt/cray/pe/modules/3.2.10.5/init/sh
#module avail
source $MODULESHOME/init/sh
echo new line of text
module load hsi
echo module loaded 

export hsidir=/3year/NCEPDEV/GEFSRR/${exptname}
echo hsidir is $hsidir

#export mydatapath=/lustre/f2/scratch/Oar.Esrl.Nggps_psd/${exptname}
export mydatapath=/lustre/f1/Scott.Gregory/${exptname}
echo mydatapath is $mydatapath

if [ -d $mydatapath/ ] #if directory exists
then
    echo 'out directory '$mydatapath' exists'
else
    echo 'making out directory '$mydatapath
    mkdir -p $mydatapath
fi

cd ${mydatapath}


rm -rf ${analdate}
echo "extract ${hsidir}/${analdate}_subset.tar"
htar -tvf ${hsidir}/${analdate}_subset.tar
htar -xvf ${hsidir}/${analdate}_subset.tar
echo "extracted? ${hsidir}/${analdate}_subset.tar"


