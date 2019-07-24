 -A nggps_psd
 #PBS -l partition=es,size=1,walltime=16:00:00
 #PBS -q rdtn
 #PBS -N htar_only_2003
 ##PBS -e htar_only_2003.err
 ##PBS -o htar_only_2003.out
 #PBS -S /bin/csh
 # need envars:  machine, analdate, datapath2, hsidir, save_hpss_full, save_hpss_subset, nanals, nanals_replay
 
 # one time- make dir for cfsr gaussian inits
 ##hsi mkdir /3year/NCEPDEV/GEFSRR/Gary.Bates/cfsr_gauss_inits
 ##hsi chmod 777 /3year/NCEPDEV/GEFSRR/Gary.Bates/cfsr_gauss_inits
 
 export analdate=2006021006
 export analdate_end=2006021006
 
 export exptname=2003stream
 export hsidir="/3year/NCEPDEV/GEFSRR/${exptname}"
 
 export enkfscripts="/lustre/f2/dev/${USER}/scripts/${exptname}"
 export incdate="${enkfscripts}/incdate.sh"
 
 export save_hpss_subset="true" # save a subset of data each analysis time to HPSS
 
 source $MODULESHOME/init/sh
 # Load HPSS on Gaea
 module load hsi
 
 export nanals=80
 # recenter nanals_replay ensemble around nanals ens mean
 export nanals_replay=10
 
 ## Main Loop
 while ((${analdate} <= ${analdate_end})); do
 
 export datapath2="/lustre/f2/scratch/${USER}/${exptname}/${analdate}"
 
 # only save full ensemble data to hpss if checkdate.py returns 0
 date_check=`python ${enkfscripts}/checkdate.py ${analdate}`
 if (($date_check == 0)); then
   export save_hpss_full="true"
 else
   export save_hpss_full="false"
 fi
 
 hr=`echo $analdate | cut -c9-10`
 export analdatem1=`${incdate} $analdate -6`
 exitstat=0
 

