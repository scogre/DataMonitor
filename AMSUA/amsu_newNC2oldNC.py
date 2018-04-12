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


###########################


nan=float('nan')

starttime=clock()

punct=string.punctuation
space=' '
hyphen='-'
digits=string.digits


if len(sys.argv) < 4:
    raise SystemExit('python amsu_newNC2oldNC.py <date> <input amsu path> <output file path>')

# file names from command line args.
rundate = sys.argv[1]
diagpath = sys.argv[2]
ncoutfilename = sys.argv[3]


model_filepath=diagpath
##model_filepath='/lustre/f1/Gary.Bates/C128_C384_nsst/'+rundate+'/'
satlite='n15'

anlcontrolnc_file = model_filepath+'diag_amsua_'+satlite+'_anl.'+rundate+'_control.nc4'
nc_anl_ctrl = Dataset(anlcontrolnc_file,'r')
gescontrolnc_file = model_filepath+'diag_amsua_'+satlite+'_ges.'+rundate+'_control.nc4'
nc_ges_ctrl = Dataset(gescontrolnc_file,'r')
ensmeannc_file = model_filepath+'diag_amsua_'+satlite+'_ges.'+rundate+'_ensmean.nc4'
nc_ensdata = Dataset(ensmeannc_file,'r')
enssprdnc_file = model_filepath+'diag_amsua_'+satlite+'_ges.'+rundate+'_ensmean_spread.nc4'
nc_sprddata = Dataset(enssprdnc_file,'r')


###############################################################################

ANLlon_diag = nc_anl_ctrl['Longitude'][:]
ANLlat_diag = nc_anl_ctrl['Latitude'][:]
ANLnobs_diag = len(ANLlat_diag)
ANLtime_diag = nc_anl_ctrl['Obs_Time'][:]
ANLchanindx_diag = nc_anl_ctrl['Channel_Index'][:]
ANLchanlist_diag = nc_anl_ctrl['sensor_chan'][:]
#fn_diaganl
#npred_diaganl
obs_diaganl = nc_anl_ctrl['Observation'][:]
OmA_diag = nc_anl_ctrl['Obs_Minus_Forecast_adjusted'][:]
OmAnobc_diag = nc_anl_ctrl['Obs_Minus_Forecast_unadjusted'][:]
hx_diaganl = obs_diaganl - nc_anl_ctrl['Obs_Minus_Forecast_adjusted'][:]
hxnobc_diaganl = obs_diaganl - nc_anl_ctrl['Obs_Minus_Forecast_unadjusted'][:]
biascorr_diaganl = hx_diaganl - hxnobc_diaganl
#biaspred_diaganl 
oberr_diaganl = ((nc_anl_ctrl['Inverse_Observation_Error'][:])**2)**-1
oberr_orig_diaganl = oberr_diaganl
used_diaganl = nc_anl_ctrl['use_flag'][:]
qcmark_diaganl = nc_anl_ctrl['QC_Flag'][:]

###############################################################################

GESlon_diag = nc_ges_ctrl['Longitude'][:]
GESlat_diag = nc_ges_ctrl['Latitude'][:]
GESnobs_diag = len(GESlat_diag)
GEStime_diag = nc_ges_ctrl['Obs_Time'][:]
GESchan_diag = nc_ges_ctrl['Channel_Index'][:]
#fn_diagges
#npred_diagges
obs_diagges = nc_ges_ctrl['Observation'][:]
OmF_diag = nc_ges_ctrl['Obs_Minus_Forecast_adjusted'][:]
OmFnobc_diag = nc_ges_ctrl['Obs_Minus_Forecast_unadjusted'][:]
hx_diagges = obs_diagges - nc_ges_ctrl['Obs_Minus_Forecast_adjusted'][:]
hxnobc_diagges = obs_diagges - nc_ges_ctrl['Obs_Minus_Forecast_unadjusted'][:]
biascorr_diagges = hx_diagges - hxnobc_diagges
#biaspred_diagges 
oberr_diagges = ((nc_ges_ctrl['Inverse_Observation_Error'][:])**2)**-1
oberr_orig_diagges = oberr_diagges
used_diagges = nc_ges_ctrl['use_flag'][:]
qcmark_diagges = nc_ges_ctrl['QC_Flag'][:]

###############################################################################

ENSlon_diag = nc_ensdata['Longitude'][:]
ENSlat_diag = nc_ensdata['Latitude'][:]
ENSnobs_diag = len(ENSlat_diag)
ENStime_diag = nc_ensdata['Obs_Time'][:]
ENSchan_diag = nc_ensdata['Channel_Index'][:]
#fn_diagges
#npred_diagges
obs_diagens = nc_ensdata['Observation'][:]
OmE_diag = nc_ensdata['Obs_Minus_Forecast_adjusted'][:]
OmEnobc_diag = nc_ensdata['Obs_Minus_Forecast_unadjusted'][:]
hx_diagens = obs_diagens - nc_ensdata['Obs_Minus_Forecast_adjusted'][:]
hxnobc_diagens = obs_diagens - nc_ensdata['Obs_Minus_Forecast_unadjusted'][:]
biascorr_diagens = hx_diagens - hxnobc_diagens
#biaspred_diagens 
oberr_diagens = ((nc_ensdata['Inverse_Observation_Error'][:])**2)**-1
oberr_orig_diagens = oberr_diagens
used_diagens = nc_ensdata['use_flag'][:]
qcmark_diagens = nc_ensdata['QC_Flag'][:]

###############################################################################

#nc_sprddata
used_diagsprd = nc_sprddata['EnKF_use_flag'][:]
OmFens_diag = nc_sprddata['EnKF_fit_ges'][:]
spredF = nc_sprddata['EnKF_spread_ges'][:]
OmAens_diag = nc_sprddata['EnKF_fit_anl'][:]
spredA = nc_sprddata['EnKF_spread_anl'][:]
print 'spredA=',spredA
###############################################################################
sprederrA = np.sqrt(spredA + oberr_diaganl)
sprederrF = np.sqrt(spredF + oberr_diagges)
###############################################################################
nc_anl_ctrl.close()
nc_ges_ctrl.close()
nc_ensdata.close()
nc_sprddata.close()
###############################################################################

nsats=1
IDsat=[206] ##### need to hook up the satellite codes
###################
ANLchan_diag=np.zeros(ANLnobs_diag)
for m in range(ANLnobs_diag):
   ANLchan_diag[m]=ANLchanlist_diag[ANLchanindx_diag[m]-1]
#print 'ANLchan_diag=',ANLchan_diag
###################
CHANnum = ANLchan_diag
gsianl_hxarray = hx_diaganl
gsiges_hxarray = hx_diagges
gsiobsarray = obs_diaganl
gsierrarray = oberr_diaganl
gsibiasAarray = biascorr_diaganl
gsibiasFarray = biascorr_diagges
gsiuseAarray = used_diaganl
gsiqcAarray = qcmark_diaganl
gsiuseFarray = used_diagges
gsiqcFarray = qcmark_diagges
gsilatarray = ANLlat_diag
gsilonarray = ANLlon_diag
gsichanarray = ANLchan_diag
gsiOmAarray = OmAnobc_diag
gsiOmA_BCarray = OmA_diag
gsiOmFarray = OmFnobc_diag
gsiOmF_BCarray = OmF_diag

gsiENS_latarray = ENSlat_diag
gsiENS_lonarray = ENSlon_diag
gsiENS_chanarray = ENSchan_diag
gsiENS_qcAarray = qcmark_diagens
gsiENS_qcFarray = qcmark_diagens
gsiENS_OmA_BCarray = OmAens_diag
gsiENS_OmF_BCarray = OmFens_diag 
gsiENS_spredAarray = np.sqrt(spredA)
gsiENS_spredFarray = np.sqrt(spredF)
gsiENS_sprederrAarray = sprederrA
gsiENS_sprederrFarray = sprederrF
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
######## Identify the variables in the diag so we can initialize arrays for the netcdf#####
diag_varbstr='TMBR'
diag_errstr='TMBRE'
diag_biasstr='TMBRbias'
diag_usestr='TMBRU'
diag_qcstr='TMBRQ'
ndiag_obd = len(diag_varbstr.split())
##################################################################################################
###########################

nc_diagdata=Dataset(ncoutfilename,'w')
diag_obs = nc_diagdata.createDimension('diaginfo',len(diag_varbstr.split()))



#################################
instrmnt='AMSU-A' #official table name
print 'instrument=', instrmnt
instrument_code = instrmnt_name2code[instrmnt]
instrmnt_lower = instrmnt.lower
instrmnt_nopunct = "".join(c for c in instrmnt_lower() if c not in punct)
instrmnt_nopunctnospace = "".join(c for c in instrmnt_nopunct if c not in space)
diag_intstname=instrmnt_nopunct
###############################################################################
#satlite_all=['NOAA 15', 'NOAA 18', 'NOAA 19', 'METOP-1', 'METOP-2',  'AQUA']
satlite_all=['NOAA 15']
#satlite_all=['n15']

nsats = len(satlite_all)
nsatd = nc_diagdata.createDimension('nsats',None)
numbufrchand = nc_diagdata.createDimension('numbufrchan',None)

#IDsat=nc_diagdata.createVariable('IDsat',np.int,('nsats'),zlib=False)
#CHANnum=nc_diagdata.createVariable('CHANnum',np.int,('nsats','numbufrchan'),zlib=False)
################################################################################
nobs_diag=ANLnobs_diag
###########################
print 'CHANnum=',CHANnum
print 'IDsat=',IDsat

nobsd = nc_diagdata.createDimension('nobs',None)

nc_diagdata.createVariable('IDsat',np.int,('nsats'),zlib=False)
nc_diagdata.createVariable('CHANnum',np.int,('nobs'),zlib=False)


gsianl_hx =\
nc_diagdata.createVariable('gsianl_hx',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiges_hx =\
nc_diagdata.createVariable('gsiges_hx',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsierr =\
nc_diagdata.createVariable('gsierr',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsibiasA =\
nc_diagdata.createVariable('gsibiasA',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsibiasF =\
nc_diagdata.createVariable('gsibiasF',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiobs =\
nc_diagdata.createVariable('gsiobs',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiuseA =\
nc_diagdata.createVariable('gsiuseA',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiqcA =\
nc_diagdata.createVariable('gsiqcA',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiuseF =\
nc_diagdata.createVariable('gsiuseF',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiqcF =\
nc_diagdata.createVariable('gsiqcF',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsilat =\
nc_diagdata.createVariable('gsilat',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsilon =\
nc_diagdata.createVariable('gsilon',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsichan =\
nc_diagdata.createVariable('gsichan',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))
################
gsiOmA =\
nc_diagdata.createVariable('gsiOmA',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiOmA_BC =\
nc_diagdata.createVariable('gsiOmA_BC',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiOmF =\
nc_diagdata.createVariable('gsiOmF',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiOmF_BC =\
nc_diagdata.createVariable('gsiOmF_BC',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_OmA_BC=\
nc_diagdata.createVariable('gsiENS_OmA_BC',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_OmF_BC=\
nc_diagdata.createVariable('gsiENS_OmF_BC',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_spredA=\
nc_diagdata.createVariable('gsiENS_spredA',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_spredF =\
nc_diagdata.createVariable('gsiENS_spredF',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_sprederrA=\
nc_diagdata.createVariable('gsiENS_sprederrA',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_sprederrF=\
nc_diagdata.createVariable('gsiENS_sprederrF',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_lat=\
nc_diagdata.createVariable('gsiENS_lat',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_lon=\
nc_diagdata.createVariable('gsiENS_lon',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_chan =\
nc_diagdata.createVariable('gsiENS_chan',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_qcA =\
nc_diagdata.createVariable('gsiENS_qcA',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENS_qcF =\
nc_diagdata.createVariable('gsiENS_qcF',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsianl_hx.diaginfo = diag_varbstr
gsiges_hx.diaginfo = diag_varbstr
gsierr.diaginfo = diag_errstr
gsibiasA.diaginfo = diag_biasstr
gsibiasF.diaginfo = diag_biasstr
gsiuseA.diaginfo = diag_usestr
gsiqcA.diaginfo = diag_qcstr
gsiuseF.diaginfo = diag_usestr
gsiqcF.diaginfo = diag_qcstr

gsianl_hx.desc = 'gsi analysis Hx'
gsiges_hx.desc = 'gsi first guess Hx'
gsierr.desc = 'observation errors used by GSI'
gsibiasA.desc = 'bias correction analysis'
gsibiasF.desc = 'bias correction 1st guess'
gsiuseA.desc = 'gsi ANL use flags'
gsiqcA.desc = 'gsi ANL QC flags'
gsiuseF.desc = 'gsi 1st guess use flags'
gsiqcF.desc = 'gsi 1st guess QC flags'

#################################################################################
#nc_diagdata['IDsat'][:] = IDsat
#print 'IDsat=',IDsat
nc_diagdata['IDsat'][:] = IDsat
nc_diagdata['CHANnum'][:] = CHANnum

nc_diagdata['gsianl_hx'][:] = gsianl_hxarray[:]
nc_diagdata['gsiges_hx'][:] = gsiges_hxarray[:]
nc_diagdata['gsiobs'][:] =  gsiobsarray[:]
nc_diagdata['gsierr'][:] = gsierrarray[:]
nc_diagdata['gsibiasA'][:] = gsibiasAarray[:]
nc_diagdata['gsibiasF'][:] = gsibiasFarray[:]
nc_diagdata['gsiuseA'][:] =  gsiuseAarray[:]
nc_diagdata['gsiqcA'][:] =  gsiqcAarray[:]
nc_diagdata['gsiuseF'][:] =  gsiuseFarray[:]
nc_diagdata['gsiqcF'][:] =  gsiqcFarray[:]
nc_diagdata['gsilat'][:] = gsilatarray[:]
nc_diagdata['gsilon'][:] = gsilonarray[:]
nc_diagdata['gsichan'][:] = gsichanarray[:]

nc_diagdata['gsiOmA'][:] = gsiOmAarray[:]
nc_diagdata['gsiOmA_BC'][:] = gsiOmA_BCarray[:]
nc_diagdata['gsiOmF'][:] = gsiOmFarray[:]
nc_diagdata['gsiOmF_BC'][:] = gsiOmF_BCarray[:]
print 'maxomfbc=', np.max(gsiOmF_BCarray)

nc_diagdata['gsiENS_lat'][:]    = gsiENS_latarray[:]
nc_diagdata['gsiENS_lon'][:]    = gsiENS_lonarray[:]
nc_diagdata['gsiENS_chan'][:]   = gsiENS_chanarray[:]
nc_diagdata['gsiENS_qcA'][:]    = gsiENS_qcAarray[:]
nc_diagdata['gsiENS_qcF'][:]    = gsiENS_qcFarray[:]
nc_diagdata['gsiENS_OmA_BC'][:]    = gsiENS_OmA_BCarray[:]
nc_diagdata['gsiENS_OmF_BC'][:]    = gsiENS_OmF_BCarray[:]
nc_diagdata['gsiENS_spredA'][:]    = gsiENS_spredAarray[:]
nc_diagdata['gsiENS_spredF'][:]    = gsiENS_spredFarray[:]
nc_diagdata['gsiENS_sprederrA'][:] = gsiENS_sprederrAarray[:]
nc_diagdata['gsiENS_sprederrF'][:] = gsiENS_sprederrFarray[:]
#################################################################################
nc_diagdata.close()
#################################################################################
#################################################################################
#################################################################################


