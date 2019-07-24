from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index
import read_diag

nan=float('nan')

#def putdate_CFSR_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile):
#python put_CFSR.py 1999 1999012418 /lfs3/projects/gfsenkf/Scott.Gregory/CFSR/ /lfs3/projects/gfsenkf/Scott.Gregory/CFSR/
date=1999012506
#2003122506
datayr=str(date)[0:4]
date10dig=str(date)
basepath='/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
diagpath=basepath+str(date)
instrmnt='amsua'
satlite='n15'
region='GLOBL'
outputpath = basepath
outfile = outputpath+'/RAD_CFSR_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
print 'outfile=',outfile
if region=='GLOBL':
   latrange=[-90, 90]
elif region=='TROPI':
   latrange=[-20,20]
elif region=='SOUTH':
   latrange=[-90,-20]
elif region=='NORTH':
   latrange=[20,90]

diaganl_obsfile = diagpath + '/diag_'  +  instrmnt + '_' + satlite + '_anl.' + date10dig
diaganl_rad = read_diag.diag_rad(diaganl_obsfile,endian='big')
diaganl_rad.read_obs()
print 'diagfile=', diaganl_obsfile

###########################

ANLnobs_diag = diaganl_rad.nobs
ANLlon_diag = diaganl_rad.lon
ANLlat_diag = diaganl_rad.lat
ANLtime_diag = diaganl_rad.time
ANLchan_diag = diaganl_rad.channel
fn_diaganl = diaganl_rad.filename
npred_diaganl = diaganl_rad.npred
hx_diaganl = diaganl_rad.hx
hxnobc_diaganl = diaganl_rad.hxnobc
biascorr_diaganl = diaganl_rad.biascorr
obs_diaganl = diaganl_rad.obs
oberr_diaganl = diaganl_rad.oberr
biaspred_diaganl = diaganl_rad.biaspred
oberr_orig_diaganl = diaganl_rad.oberr_orig
used_diaganl = diaganl_rad.used
qcmark_diaganl = diaganl_rad.qcmark
#############################

diagges_obsfile = diagpath + '/diag_'  +  instrmnt + '_' + satlite + '_ges.' + date10dig
diagges_rad = read_diag.diag_rad(diagges_obsfile,endian='big')
diagges_rad.read_obs()
print 'ges file=',diagges_obsfile

###########################
GESnobs_diag = diagges_rad.nobs
GESlon_diag = diagges_rad.lon
GESlat_diag = diagges_rad.lat
GEStime_diag = diagges_rad.time
GESchan_diag = diagges_rad.channel
fn_diagges = diagges_rad.filename
npred_diagges = diagges_rad.npred
hx_diagges = diagges_rad.hx
hxnobc_diagges = diagges_rad.hxnobc
biascorr_diagges = diagges_rad.biascorr
obs_diagges = diagges_rad.obs
oberr_diagges = diagges_rad.oberr
biaspred_diagges = diagges_rad.biaspred
oberr_orig_diagges = diagges_rad.oberr_orig
used_diagges = diagges_rad.used
qcmark_diagges = diagges_rad.qcmark
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################
obs = obs_diaganl
chan_diag = ANLchan_diag
lat  = ANLlat_diag 
latidx = np.logical_and(lat >= np.min(latrange), lat <= np.max(latrange))
omf_ctrl = hx_diagges
oma_ctrl = hx_diaganl
omf_ens  = nan*np.ones(ANLnobs_diag)
oma_ens  = nan*np.ones(ANLnobs_diag)
gsi_used  = used_diaganl
enkf_used = nan*np.ones(ANLnobs_diag)
gsi_qcd  = qcmark_diaganl
sprd_f =  nan*np.ones(ANLnobs_diag)
sprd_a =  nan*np.ones(ANLnobs_diag)
obserr = oberr_diaganl
biascorr = hxnobc_diagges - hx_diagges
print('chan_diag=',chan_diag)
print('uniqchan=',np.unique(chan_diag))
print('lenchandiag=',len(np.unique(chan_diag)))
print('GOT HERE #1')

############################################
anndata = Dataset(outfile, 'a')
alldate=anndata['All_Dates']
idate = np.nonzero(alldate[:]==date)[0][0]
anndata['Full_Dates'][idate] = date
##### ['Ncycles','Nchans']
chans = anndata['Channels'][:].tolist()
print 'lenannhan=',len(chans)
for ichan in range(len(chans)):
   print('GOT HERE ',ichan)
   chanidx = (chan_diag==chans[ichan])
   #chanidx = (chan_diag==chanlist_diag[ichan])
   #print 'lenlatindx,lenchanindx=',len(latidx),len(chanidx)
   chanlatidx = np.logical_and(chanidx, latidx)
   print('chanlatindx=',chanlatidx)
   qcdidx  = (gsi_qcd == 0)
   qidx = np.logical_and(qcdidx, chanlatidx)
   anndata['nobs_all'][idate,ichan]  = len(obs[chanlatidx])
   #anndata['nobs_used'][idate,ichan] = len(obs[idx])
   anndata['nobs_qcd'][idate,ichan] = len(obs[qidx])
   anndata['mean_obs_all'][idate,ichan]  = np.mean(obs[chanlatidx])
   anndata['mean_obs_used'][idate,ichan] = np.mean(obs[qidx])
   anndata['mean_obs_qcd'][idate,ichan] = np.mean(obs[qidx])
   anndata['mean_omf_ctrl'][idate,ichan] = np.mean(omf_ctrl[qidx])
   anndata['mean_oma_ctrl'][idate,ichan] = np.mean(oma_ctrl[qidx])
   anndata['std_omf_ctrl'][idate,ichan]  = np.sqrt(np.mean(omf_ctrl[qidx] ** 2))
   anndata['std_oma_ctrl'][idate,ichan]  = np.sqrt(np.mean(oma_ctrl[qidx] ** 2))
   #del idx
   #del useidx
   print('GOT HERE middle',ichan)
   useidx = (enkf_used == 1)  ## for enkf use only
   idx = np.logical_and(useidx, chanlatidx)
   anndata['nobs_used'][idate,ichan] = len(obs[idx])
   anndata['mean_omf_ens'][idate,ichan] = np.mean(omf_ens[idx])
   # LEAVING OUT FOR NOW     anndata['mean_oma_ens'][idate,ichan] = np.mean(oma_ens[idx])
   anndata['spread_f'][idate,ichan] = np.sqrt(np.mean(sprd_f[idx]))
   # LEAVING OUT FOR NOW     anndata['spread_a'][idate,ichan] = np.sqrt(np.mean(sprd_a[idx]))
   anndata['spread_obserr_f'][idate,ichan] = np.sqrt(np.mean(sprd_f[idx] + obserr[idx]))
   # LEAVING OUT FOR NOW     anndata['spread_obserr_a'][idate,ichan] = np.sqrt(np.mean(sprd_a[idx] + obserr[idx]))
   anndata['std_omf_ens'][idate,ichan]  = np.sqrt(np.mean(omf_ens[idx] ** 2))
   anndata['mean_biascor'][idate,ichan]=np.mean(biascorr[idx])
   anndata['std_biascor'][idate,ichan]=np.std(biascorr[idx])
   print('GOT HERE end',ichan)
print('finished loop')
anndata.close()

