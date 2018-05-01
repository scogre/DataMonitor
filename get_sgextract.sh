#!/bin/sh

echo analdate is $enddate10dig
analdate=$enddate10dig
exptname=$exptname
mydatapath=$mydatapath

source $MODULESHOME/init/sh
module load hsi

export hsidir=/3year/NCEPDEV/GEFSRR/${exptname}

#export mydatapath=/lustre/f1/Oar.Esrl.Nggps_psd/${exptname}
export mydatapath=/lustre/f1/Scott.Gregory/${exptname}

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


