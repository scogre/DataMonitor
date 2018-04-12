###from __future__ import print_function
import ncepbufr
import numpy as np
from netCDF4 import Dataset
from ncepbufr import prepbufr_mnemonics_dict as mnemonics_dict
from ncepbufr import rad_header_dict as header_dict
from ncepbufr import satellite_names as code2sat_name
from ncepbufr import satinstrmnt_names as code2instrmnt_name
from ncepbufr import satellite_codes as sat_name2code
from ncepbufr import instrument_codes as instrmnt_name2code
from time import clock

import sys
import datetime
import string
import re
from datetime import timedelta
import math
import time
import hashlib
import datetime
import matplotlib.pyplot as plt



##########################################################################################
nan=float('nan')
merged_nc_filename = sys.argv[1]
ncplotdata_filename = sys.argv[2]

print 'merged_nc_filename=',merged_nc_filename

lenfilename=len(ncplotdata_filename)

##########################################################################################
emptyval = -99999
##########################################################################################
nc_merged = Dataset(merged_nc_filename,'r')

gsichan=nc_merged['gsichan'][:]
IDsat=nc_merged['IDsat'][:]
CHANnum=nc_merged['CHANnum'][:]

gsianl_hx=nc_merged['gsianl_hx'][:]
gsiges_hx=nc_merged['gsiges_hx'][:]
gsierr=nc_merged['gsierr'][:]
gsiobs=nc_merged['gsiobs'][:]
gsibiasA=nc_merged['gsibiasA'][:]
gsibiasF=nc_merged['gsibiasF'][:]
gsiuseA=nc_merged['gsiuseA'][:]
gsiqcA=nc_merged['gsiqcA'][:]
gsiuseF=nc_merged['gsiuseF'][:]
gsiqcF=nc_merged['gsiqcF'][:]
gsilat=nc_merged['gsilat'][:]
gsilon=nc_merged['gsilon'][:]
gsichan=nc_merged['gsichan'][:]

gsiOmA=nc_merged['gsiOmA'][:]
gsiOmA_BC=nc_merged['gsiOmA_BC'][:]
gsiOmF=nc_merged['gsiOmF'][:]
gsiOmF_BC=nc_merged['gsiOmF_BC'][:]

gsiENS_OmA_BC    =nc_merged['gsiENS_OmA_BC'][:]
gsiENS_OmF_BC    =nc_merged['gsiENS_OmF_BC'][:]
gsiENS_spredA    =nc_merged['gsiENS_spredA'][:]
gsiENS_spredF    =nc_merged['gsiENS_spredF'][:]
gsiENS_sprederrA =nc_merged['gsiENS_sprederrA'][:]
gsiENS_sprederrF =nc_merged['gsiENS_sprederrF'][:]
gsiENS_chan = nc_merged['gsiENS_chan'][:]
gsiENS_qcA  = nc_merged['gsiENS_qcA'][:]
gsiENS_qcF  = nc_merged['gsiENS_qcF'][:]


numob=len(gsiobs)
print 'numob=', numob



uniqdiagchan=np.unique(gsichan)
print 'unique channels=', uniqdiagchan
numdiagchan=len(uniqdiagchan)
print 'len uniq=', numdiagchan



chans=nc_merged['gsichan'][:]
uniqdiagchan=np.unique(chans)
sat_parse=IDsat
satno=0    ############################## THIS WILL HAVE TO BE MODIFIED FOTR MULTIPLE SATELLITES
########## AND chase down the 'satno' elsewhere ###################################################



#########################################################################################
full_gsiobs=nc_merged['gsiobs'][:]
lendata=full_gsiobs.shape[0]
print 'lendata=',lendata
indcs_master=np.arange(lendata)
print 'lenmaster=', len(indcs_master)

full_gsilat = nc_merged['gsilat'][:]
print 'shapelat=', full_gsilat.shape
print 'lat1to10=', full_gsilat
print 'maxfullat=', np.max(full_gsilat)

for mm in range(4):
	print 'mm=', mm
	if mm==0:
		boundaries=(-90,-20)
		suffix='_SOUTH'
	elif mm==1:
		boundaries=(-20,20)
		suffix='_TROPI'
	elif mm==2:
		boundaries=(20,90)
		suffix='_NORTH'
	elif mm==3:
		boundaries=(-90,90)
		suffix='_GLOBL'
	minlat=min(boundaries)
	maxlat=max(boundaries)
	print 'maxlat=', maxlat
	print 'numgreater=', len(full_gsilat[:,satno]>=minlat)
	print 'numlesser=', len(indcs_master[full_gsilat[:,satno]<=maxlat])
#	full_gsilatindcs=(indcs_master[(full_gsilat[:]>=minlat) & (full_gsilat[:]<=maxlat)] )
        print('fullgsilat.shape=',full_gsilat.shape)
        full_gsilatindcs=(indcs_master[(full_gsilat[:,satno]>=minlat) & (full_gsilat[:,satno]<=maxlat)] )
        latindcs=(indcs_master[(full_gsilat[:,satno]>=minlat) & (full_gsilat[:,satno]<=maxlat)] )
	print 'lenlat=', len(latindcs)
        print 'len all lat=', len(full_gsilatindcs)
	
	#########################################################################################
        all_satobsindcs=full_gsilatindcs
	satobsindcs=latindcs
	#satobsindcs=np.arange(numob)
	#print 'satobind=',satobsindcs
	#########################################################################################
	GEOncplotdata_filename= ncplotdata_filename[0:lenfilename-3] + suffix +'.nc'
	print 'geoname=',GEOncplotdata_filename
	plotdata_nc = Dataset(GEOncplotdata_filename,'w',format='NETCDF4')
	
	#############################################################################################
	############################### initialize plotdata file
	#############################################################
	#plotdata_ncfilename='AMSUAplotdata_' + date10dig + '.nc'

	nsatd = plotdata_nc.createDimension('nsats',None)
	numchand = plotdata_nc.createDimension('numchan',None)
	numobs_tot =\
	plotdata_nc.createVariable('numobs_tot',np.int,('nsats','numchan'),zlib=False)
	numobs_diag =\
	plotdata_nc.createVariable('numobs_diag',np.int,('nsats','numchan'),zlib=False)
	numobs_use =\
	plotdata_nc.createVariable('numobs_use',np.int,('nsats','numchan'),zlib=False)
	numobs_qc =\
	plotdata_nc.createVariable('numobs_qc',np.int,('nsats','numchan'),zlib=False)
	
	Tmean_allbufr =\
	plotdata_nc.createVariable('Tmean_allbufr',np.float32,('nsats','numchan'),zlib=False)
	Tmean_alldiag =\
	plotdata_nc.createVariable('Tmean_alldiag',np.float32,('nsats','numchan'),zlib=False)
	Tmean_use =\
	plotdata_nc.createVariable('Tmean_use',np.float32,('nsats','numchan'),zlib=False)
	Tmean_qc =\
	plotdata_nc.createVariable('Tmean_qc',np.float32,('nsats','numchan'),zlib=False)
	
	Biascorr_mean =\
	plotdata_nc.createVariable('Biascorr_mean',np.float32,('nsats','numchan'),zlib=False)
	Biascorr_std =\
	plotdata_nc.createVariable('Biascorr_std',np.float32,('nsats','numchan'),zlib=False)
	
	OmF_noBC_mean =\
	plotdata_nc.createVariable('OmF_noBC_mean',np.float32,('nsats','numchan'),zlib=False)
	OmF_wBC_mean =\
	plotdata_nc.createVariable('OmF_wBC_mean',np.float32,('nsats','numchan'),zlib=False)
	OmF_noBC_std =\
	plotdata_nc.createVariable('OmF_noBC_std',np.float32,('nsats','numchan'),zlib=False)
	OmF_wBC_std =\
	plotdata_nc.createVariable('OmF_wBC_std',np.float32,('nsats','numchan'),zlib=False)
	
	
	OmA_noBC_mean =\
	plotdata_nc.createVariable('OmA_noBC_mean',np.float32,('nsats','numchan'),zlib=False)
	OmA_wBC_mean =\
	plotdata_nc.createVariable('OmA_wBC_mean',np.float32,('nsats','numchan'),zlib=False)
	OmA_noBC_std =\
	plotdata_nc.createVariable('OmA_noBC_std',np.float32,('nsats','numchan'),zlib=False)
	OmA_wBC_std =\
	plotdata_nc.createVariable('OmA_wBC_std',np.float32,('nsats','numchan'),zlib=False)
	
	
	######
	ENSspredA_mean =\
	plotdata_nc.createVariable('ENSspredA_mean',np.float32,('nsats','numchan'),zlib=False)
	ENSsprederrA_mean =\
	plotdata_nc.createVariable('ENSsprederrA_mean',np.float32,('nsats','numchan'),zlib=False)
	ENS_OmA_wBC_std =\
	plotdata_nc.createVariable('ENS_OmA_wBC_std',np.float32,('nsats','numchan'),zlib=False)
	ENS_OmA_wBC_mean =\
	plotdata_nc.createVariable('ENS_OmA_wBC_mean',np.float32,('nsats','numchan'),zlib=False)
	ENSspredF_mean =\
	plotdata_nc.createVariable('ENSspredF_mean',np.float32,('nsats','numchan'),zlib=False)
	ENSsprederrF_mean =\
	plotdata_nc.createVariable('ENSsprederrF_mean',np.float32,('nsats','numchan'),zlib=False)
	ENS_OmF_wBC_std =\
	plotdata_nc.createVariable('ENS_OmF_wBC_std',np.float32,('nsats','numchan'),zlib=False)
	ENS_OmF_wBC_mean =\
	plotdata_nc.createVariable('ENS_OmF_wBC_mean',np.float32,('nsats','numchan'),zlib=False)
	######
	IDsat_plotnc =\
	plotdata_nc.createVariable('IDsat',np.int,('nsats'),zlib=False)
	CHANnum =\
	plotdata_nc.createVariable('CHANnum',np.int,('nsats','numchan'),zlib=False)
	##############################################################


	print 'lenindcs=',len(satobsindcs)
	for nchan in range(numdiagchan):
	    DUMMYsatchanobsindcs=np.nonzero(gsichan[all_satobsindcs]==uniqdiagchan[nchan])[0]
	    satchanobsindcs=all_satobsindcs[DUMMYsatchanobsindcs]
	    numinsatchan=len(satchanobsindcs)               #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    dummy_satobs = gsiobs[satchanobsindcs]
	    notnanindcs=[i for i, v in enumerate(dummy_satobs) if v>0 and v<350 and not(math.isnan(v))]
	    diagsatobs=dummy_satobs[notnanindcs]
	    #if len(diagsatobs)>0:
	    #	meanTbufr=np.mean(diagsatobs)               #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    #else:
	    meanTbufr=float('nan')
	    #################################################################################################
	
	    #################################################################################################
	    #satchandiagindcs= np.nonzero(dummy_channum==uniqdiagchan[nchan])[0]
	    DUMMYsatchandiagindcs= np.nonzero(gsichan[satobsindcs]==uniqdiagchan[nchan])[0]
	    satchandiagindcs= satobsindcs[DUMMYsatchandiagindcs]
	    numindiagsatchan =len(satchandiagindcs)         #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    dummy_diagobsCHAN = np.empty(len(satchandiagindcs))
	    #dummy_diagobsCHAN=dummy_diagobs[satchandiagindcs]
	    dummy_diagobsCHAN=gsiobs[satchandiagindcs]
	    notnanindcs=[i for i, v in enumerate(dummy_diagobsCHAN) if v>0 and v<9999 and not(math.isnan(v))]
	    diagobs_notnan=dummy_diagobsCHAN[notnanindcs]
	    #meanTdiag=np.mean(diagobs_notnan)                      #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    if len(diagobs_notnan)>0:
	    	meanTdiag=np.mean(diagobs_notnan)               #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    else:
	    	meanTdiag=float('nan')
	    print 'meanTdiag=', meanTdiag
	
	    dummy_useFLAGCHAN=gsiuseA[satchandiagindcs]
	    useFLAG=np.empty(len(satchandiagindcs))
	    useFLAG=dummy_useFLAGCHAN
	    sumNUMused=sum(useFLAG==1)
	    usedindcs=[i for i, v in enumerate(useFLAG) if v==1 ]
	    diagUSEDobs=dummy_diagobsCHAN[usedindcs]
	    numuseddiagsatchan = len(diagUSEDobs)
	    print 'numuseddiagsatchan=', numuseddiagsatchan
	    if numuseddiagsatchan>0:
	    	meanTuseddiag=np.mean(diagUSEDobs)              #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    else:
	    	meanTuseddiag=float('nan')
	    print 'meanTuseddiag=', meanTuseddiag


	
	    dummy_A_qcFLAGCHAN=gsiqcA[satchandiagindcs]
            qcFLAG_A=nan*np.ones(len(satchandiagindcs))
	    qcFLAG_A=dummy_A_qcFLAGCHAN
	    sumNUMqc_A=sum(qcFLAG_A==0)
	    qcindcs_A=[i for i, v in enumerate(qcFLAG_A) if v==0 ]
            print 'qcFLAG_A[qcindcs_A]=', qcFLAG_A[qcindcs_A]
	    diagQCobs_A=dummy_diagobsCHAN[qcindcs_A]
	    numqcdiagsatchan_A = len(diagQCobs_A)
	    #if numqcdiagsatchan_A>0:
            if sumNUMqc_A!=0:
	    	meanT_qc_diag_A=np.mean(diagQCobs_A)              #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    else:
	    	meanT_qc_diag_A=float('nan')
	    print 'meanT_qc_diag_A=', meanT_qc_diag_A
            print 'numqcdiagsatchan_A=', numqcdiagsatchan_A



	
	    dummy_F_qcFLAGCHAN=gsiqcF[satchandiagindcs]
	    qcFLAG_F=np.empty(len(satchandiagindcs))
	    qcFLAG_F=dummy_F_qcFLAGCHAN
	    sumNUMqc_F=sum(qcFLAG_F==0)
	    qcindcs_F=[i for i, v in enumerate(qcFLAG_F) if v==0 ]
	    diagQCobs_F=dummy_diagobsCHAN[qcindcs_F]
	    numqcdiagsatchan_F = len(diagQCobs_F)
	    #if numqcdiagsatchan_A>0:
            if sumNUMqc_F!=0:
	    	meanT_qc_diag_F=np.mean(diagQCobs_F)              #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    else:
	    	meanT_qc_diag_F=float('nan')
	    print 'meanT_qc_diag_F=', meanT_qc_diag_F
	
	
	
	    #################################################################################################
	
	    dummy_biasanlCHAN = np.empty(len(satchandiagindcs))
	    dummy_biasanlCHAN=gsibiasA[satchandiagindcs]
	    biasANLindcs=qcindcs_A
	    biasanl=dummy_biasanlCHAN[biasANLindcs]
	
	    dummy_biasgesCHAN = np.empty(len(satchandiagindcs))
	    dummy_biasgesCHAN=gsibiasF[satchandiagindcs]
	    biasGESindcs=qcindcs_F
	    biasges=dummy_biasgesCHAN[biasGESindcs]         #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	
	    dummy_OmF_CHAN = np.empty(len(satchandiagindcs))
	    dummy_OmF_CHAN = gsiOmF[satchandiagindcs]
	    OmFindcs=qcindcs_F
	    OmF_CHAN= dummy_OmF_CHAN[OmFindcs]
	
	    dummy_BC_OmF_CHAN = np.empty(len(satchandiagindcs))
	    dummy_BC_OmF_CHAN = gsiOmF_BC[satchandiagindcs]
	    OmFBCindcs=qcindcs_F
	    OmF_BC_CHAN= dummy_BC_OmF_CHAN[OmFBCindcs]
	
	    dummy_OmA_CHAN = np.empty(len(satchandiagindcs))
	    dummy_OmA_CHAN = gsiOmA[satchandiagindcs]
	    OmAindcs=qcindcs_A
	    OmA_CHAN= dummy_OmA_CHAN[OmAindcs]
	
	    dummy_BC_OmA_CHAN = np.empty(len(satchandiagindcs))
	    dummy_BC_OmA_CHAN = gsiOmA_BC[satchandiagindcs]
	    OmABCindcs=qcindcs_A
	    OmA_BC_CHAN= dummy_BC_OmA_CHAN[OmABCindcs]
	    
	    del OmABCindcs
	    del qcindcs_A
	    del qcindcs_F
	
	
	 
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	 
	 
	 
	    dummy_ENS_A_qcFLAGCHAN=gsiENS_qcA[satchandiagindcs]
	    qcENS_FLAG_A=np.empty(len(satchandiagindcs))
	    qcENS_FLAG_A=dummy_A_qcFLAGCHAN
	    sumNUMqcENS_A=sum(qcENS_FLAG_A==0)
	    qcENS_indcs_A=[i for i, v in enumerate(qcENS_FLAG_A) if v==0 ]
	
	
	
	    dummy_ENS_OmA_wBC = np.empty(len(satchandiagindcs))
	    dummy_ENS_OmA_wBC = gsiENS_OmA_BC[satchandiagindcs]
	    ENS_Aindcs = qcENS_indcs_A
	    dummy2=dummy_ENS_OmA_wBC[ENS_Aindcs]
	    dummy3=dummy2[abs(dummy2)<9999]
	    #try:
	    #	print 'min dummyENS_OmA_wBC=',np.min(dummy3)
	    #except:
	    #	print 'not conforming'
	    if len(dummy3)>0:
	    	ENS_OmA_wBC_mean[satno,nchan] = np.mean(dummy3)               #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    	ENS_OmA_wBC_std[satno,nchan]  = np.std(dummy3)
	    else:
	    	ENS_OmA_wBC_mean[satno,nchan]=float('nan')
	    	ENS_OmA_wBC_std[satno,nchan]=float('nan')
#	    print 'ENS_OmA_wBC_mean=', ENS_OmA_wBC_mean
	    #ENS_OmA_wBC_mean[satno,nchan] = np.mean(dummy3)
	    #ENS_OmA_wBC_std[satno,nchan]  = np.std(dummy3)
	    del dummy2
	    del dummy3
	    
	    
	    dummy_ENSspredA = np.empty(len(satchandiagindcs))
	    dummy_ENSspredA = gsiENS_spredA[satchandiagindcs]
	    ENS_Aindcs = qcENS_indcs_A
	    dummy2=dummy_ENSspredA[ENS_Aindcs]
	    dummy3=dummy2[abs(dummy2)<9999]
	    if len(dummy3)>0:
	    	ENSspredA_mean[satno,nchan] = np.mean(dummy3)
	    else:
	    	ENSspredA_mean[satno,nchan] = float('nan')
	    del dummy2
	    del dummy3
	        
	    dummy_ENSsprederrA = np.empty(len(satchandiagindcs))
	    dummy_ENSsprederrA = gsiENS_sprederrA[satchandiagindcs]
	    ENS_Aindcs = qcENS_indcs_A
	    dummy2=dummy_ENSsprederrA[ENS_Aindcs]
	    dummy3=dummy2[abs(dummy2)<9999]
	    if len(dummy3)>0:
	    	ENSsprederrA_mean[satno,nchan] = np.mean(dummy3)
	    else:
	    	ENSsprederrA_mean[satno,nchan] =float('nan')
	    del dummy2
	    del dummy3
	    
	    del qcENS_indcs_A
	    del ENS_Aindcs
	    
	    ######################################################################################
	
	    dummy_ENS_F_qcFLAGCHAN=gsiENS_qcF[satchandiagindcs]
	    qcENS_FLAG_F=np.empty(len(satchandiagindcs))
	    qcENS_FLAG_F=dummy_F_qcFLAGCHAN
	    sumNUMqcENS_F=sum(qcENS_FLAG_F==0)
	    qcENS_indcs_F=[i for i, v in enumerate(qcENS_FLAG_F) if v==0 ]
	
	
	
	    dummy_ENS_OmF_wBC = np.empty(len(satchandiagindcs))
	    dummy_ENS_OmF_wBC = gsiENS_OmF_BC[satchandiagindcs]
	    ENS_Findcs=qcENS_indcs_F
	    dummy2=dummy_ENS_OmF_wBC[ENS_Findcs]
	    dummy3=dummy2[abs(dummy2)<9999]
	    #try:
	    #	print 'min dummyENS_OmF_wBC=',np.min(dummy3)
	    #except:
	    #	print 'not conforming'
	    if len(dummy3)>0:
	    	ENS_OmF_wBC_mean[satno,nchan] = np.mean(dummy3)               #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	    	ENS_OmF_wBC_std[satno,nchan]  = np.std(dummy3)
	    else:
	    	ENS_OmF_wBC_mean[satno,nchan]=float('nan')
	    	ENS_OmF_wBC_std[satno,nchan]=float('nan')
#	    print 'ENS_OmF_wBC_mean=', ENS_OmF_wBC_mean
	    del dummy2
	    del dummy3
	    
	    dummy_ENSspredF = np.empty(len(satchandiagindcs)) 
	    dummy_ENSspredF = gsiENS_spredF[satchandiagindcs]
	    ENS_Findcs = qcENS_indcs_F
	    dummy2=dummy_ENSspredF[ENS_Findcs]
	    dummy3=dummy2[abs(dummy2)<9999]
	    if len(dummy3)>0:
	    	ENSspredF_mean[satno,nchan] = np.mean(dummy3)
	    else:
	    	ENSspredF_mean[satno,nchan] = float('nan')
	    del dummy2
	    del dummy3
	    
	    dummy_ENSsprederrF = np.empty(len(satchandiagindcs)) 
	    dummy_ENSsprederrF = gsiENS_sprederrF[satchandiagindcs]
	    ENS_Findcs = qcENS_indcs_F
	    dummy2=dummy_ENSsprederrF[ENS_Findcs]
	    dummy3=dummy2[abs(dummy2)<9999]
	    if len(dummy3)>0:
	    	ENSsprederrF_mean[satno,nchan] = np.mean(dummy3)
	    else:
	    	ENSsprederrF_mean[satno,nchan] =float('nan')
	    del dummy2
	    del dummy3
	    
	    del qcENS_indcs_F
	    del ENS_Findcs
	    
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	    #################################################################################################
	
	    numobs_tot[satno,nchan] = numinsatchan; del numinsatchan
	    numobs_diag[satno,nchan] = numindiagsatchan; del numindiagsatchan
	    numobs_use[satno,nchan] = numuseddiagsatchan; del numuseddiagsatchan
	    numobs_qc[satno,nchan] = numqcdiagsatchan_A; del numqcdiagsatchan_A  ##QCmark=0
	    Tmean_allbufr[satno,nchan] = meanTbufr; del meanTbufr
	    Tmean_alldiag[satno,nchan] = meanTdiag; del meanTdiag
	    Tmean_use[satno,nchan] = meanTuseddiag; del meanTuseddiag   #################### THURSDAY MORNING
            print 'meanT_qc_diag_A=',meanT_qc_diag_A
	    Tmean_qc[satno,nchan] = meanT_qc_diag_A; del meanT_qc_diag_A   #####
            
	    Biascorr_mean[satno,nchan] = np.mean(biasges)
	    Biascorr_std[satno,nchan] = np.std(biasges); del biasges 
	
	    OmF_noBC_mean[satno,nchan] = np.mean(OmF_CHAN) 
	    OmF_wBC_mean[satno,nchan] = np.mean(OmF_BC_CHAN) 
	    OmF_noBC_std[satno,nchan] = np.std(OmF_CHAN); del OmF_CHAN
	    OmF_wBC_std[satno,nchan] = np.std(OmF_BC_CHAN); del OmF_BC_CHAN
	
	    OmA_noBC_mean[satno,nchan] = np.mean(OmA_CHAN) 
	    OmA_wBC_mean[satno,nchan] = np.mean(OmA_BC_CHAN)
	    OmA_noBC_std[satno,nchan] = np.std(OmA_CHAN); del OmA_CHAN
	    OmA_wBC_std[satno,nchan] = np.std(OmA_BC_CHAN); del OmA_BC_CHAN
	    #print 'OmA_wBC_mean=',np.mean(OmA_BC_CHAN)
	    CHANnum[satno,nchan] = uniqdiagchan[nchan]
	#IDsat[satno] = sat_parse
	
	
	#########################################################################################    
        print 'suffix=',suffix
        print 'numobs_tot=',numobs_tot
	plotdata_nc['numobs_tot'][:] =      numobs_tot[:]
	plotdata_nc['numobs_diag'][:] =     numobs_diag[:]
	plotdata_nc['numobs_use'][:] =      numobs_use[:]
	plotdata_nc['numobs_qc'][:] =       numobs_qc[:]
	plotdata_nc['Tmean_allbufr'][:] =   Tmean_allbufr[:]
	plotdata_nc['Tmean_alldiag'][:] =   Tmean_alldiag[:]
	plotdata_nc['Tmean_use'][:] =       Tmean_use[:]
	plotdata_nc['Tmean_qc'][:] =        Tmean_qc[:]
	plotdata_nc['Biascorr_mean'][:] =   Biascorr_mean[:]
	plotdata_nc['Biascorr_std'][:] =    Biascorr_std[:]
	plotdata_nc['OmF_noBC_mean'][:] =   OmF_noBC_mean[:]
	plotdata_nc['OmF_wBC_mean'][:] =    OmF_wBC_mean[:]
	plotdata_nc['OmF_noBC_std'][:] =    OmF_noBC_std[:]
	plotdata_nc['OmF_wBC_std'][:] =     OmF_wBC_std[:]
	
	plotdata_nc['OmA_noBC_mean'][:] =   OmA_noBC_mean[:]
	plotdata_nc['OmA_wBC_mean'][:] =    OmA_wBC_mean[:]
	plotdata_nc['OmA_noBC_std'][:] =    OmA_noBC_std[:]
	plotdata_nc['OmA_wBC_std'][:] =     OmA_wBC_std[:]
	
	plotdata_nc['ENS_OmA_wBC_mean'][:]= ENS_OmA_wBC_mean[:]
	plotdata_nc['ENS_OmA_wBC_std'][:] = ENS_OmA_wBC_std[:]
	plotdata_nc['ENSspredA_mean'][:] =  ENSspredA_mean[:]
	plotdata_nc['ENSsprederrA_mean'][:]=ENSsprederrA_mean[:]
	plotdata_nc['ENS_OmF_wBC_mean'][:]= ENS_OmF_wBC_mean[:]
	plotdata_nc['ENS_OmF_wBC_std'][:] = ENS_OmF_wBC_std[:]
	plotdata_nc['ENSspredF_mean'][:] =  ENSspredF_mean[:]
	plotdata_nc['ENSsprederrF_mean'][:]=ENSsprederrF_mean[:]
	
	plotdata_nc['IDsat'][:] = IDsat; print 'IDsat=', IDsat
	plotdata_nc['CHANnum'][:] = CHANnum[:]
	
	plotdata_nc.close()
	del satobsindcs
	del all_satobsindcs
		
	del numobs_tot
	del numobs_diag 
	del numobs_use
	del numobs_qc
	del Tmean_allbufr 
	del Tmean_alldiag 
	del Tmean_use
	del Tmean_qc
	del Biascorr_mean
	del Biascorr_std
	del OmF_noBC_mean
	del OmF_wBC_mean
	del OmF_noBC_std
	del OmF_wBC_std
	
	del OmA_noBC_mean
	del OmA_wBC_mean
	del OmA_noBC_std
	del OmA_wBC_std

	del ENS_OmA_wBC_mean
	del ENS_OmA_wBC_std
	del ENSspredA_mean
	del ENSsprederrA_mean
	del ENS_OmF_wBC_mean
	del ENS_OmF_wBC_std
	del ENSspredF_mean
	del ENSsprederrF_mean
	
	del DUMMYsatchanobsindcs
	del satchandiagindcs

nc_merged.close()
















