from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index


## TRANSLATE NORTH SOUTH GLOBL TROPI TO LATRANGES
#diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/2003stream/'
#date=2003010206
#instrmnt='amsua'
#satlite='n15'
#latrange=[-90, 90]
#outfile='/lustre/f1/Scott.Gregory/FV3s2003/FV3s2003_2003_AMSUA_n15_GLOBL.nc'

def putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile):
   anlcontrolnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_anl.'+date+'_control.nc4'
   diag_ctrl_a = Dataset(anlcontrolnc_file,'r')
   gescontrolnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_ges.'+date+'_control.nc4'
   diag_ctrl_f = Dataset(gescontrolnc_file,'r')
   ensmeannc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_ges.'+date+'_ensmean.nc4'
   diag_ens_mean = Dataset(ensmeannc_file,'r')
   enssprdnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_ges.'+date+'_ensmean_spread.nc4'
   diag_ens_sprd = Dataset(enssprdnc_file,'r')

   ###############################################################################
   chanindx_diag = nc_anl_ctrl['Channel_Index'][:]
   nobs_anl=len(chanindx_diag)
   chanlist_diag = nc_anl_ctrl['sensor_chan'][:]
   obs = diag_ctrl_f['Observation'][:]
   
   chan_diag=np.zeros(nobs_anl)
   for m in range(nobs_anl):
      chan_diag[m]=chanlist_diag[chanindx_diag[m]-1]

   lat  = diag_ctrl_f['Latitude'][:]
   latidx = np.logical_and(lat >= np.min(latrange), lat <= np.max(latrange))

   omf_ctrl = diag_ctrl_f['Obs_Minus_Forecast_adjusted'][:]
   oma_ctrl = diag_ctrl_a['Obs_Minus_Forecast_adjusted'][:]
   omf_ens  = diag_ens_sprd['EnKF_fit_ges'][:]
   oma_ens  = diag_ens_sprd['EnKF_fit_anl'][:]

   gsi_used  = diag_ctrl_a['use_flag'][:]
   print 'lengsiused=',len(gsi_used)
   enkf_used = diag_ens_sprd['EnKF_use_flag'][:]
   gsi_qcd  = diag_ctrl_a['QC_Flag'][:]

   sprd_f =  diag_ens_sprd['EnKF_spread_ges'][:]
   sprd_a =  diag_ens_sprd['EnKF_spread_anl'][:]
   obserr = 1. / ( diag_ctrl_f['Inverse_Observation_Error'][:]**2 )

   biascorr = diag_ctrl_f['Obs_Minus_Forecast_unadjusted'][:] - diag_ctrl_f['Obs_Minus_Forecast_adjusted'][:]

   anndata = Dataset(outfile, 'a')
   alldate=anndata['All_Dates']
   idate = np.nonzero(alldate[:]==date)[0][0]
   anndata['Full_Dates'][idate] = date

   ##### ['Ncycles','Nchans']
   chans = anndata['Channels'][:].tolist()
   print 'lenchan=',len(chans)
   for ichan in range(len(chans)):
      chanidx = (chan_diag==chanlist_diag[ichan])
      chanlatidx = np.logical_and(chanidx, latidx)
      useidx  = (gsi_used == 1)
      qcdidx  = (gsi_qcd == 0)
      idx = np.logical_and(useidx, chanlatidx)
      qidx = np.logical_and(qcdidx, chanlatidx)
      anndata['nobs_all'][idate,ichan]  = len(obs[chanlatidx])
      anndata['nobs_used'][idate,ichan] = len(obs[idx])
      anndata['nobs_qcd'][idate,ichan] = len(obs[qidx])
      anndata['mean_obs_all'][idate,ichan]  = np.mean(obs[chanlatidx])
      anndata['mean_obs_used'][idate,ichan] = np.mean(obs[idx])
      anndata['mean_obs_qcd'][idate,ichan] = np.mean(obs[qidx])
      anndata['mean_omf_ctrl'][idate,ichan] = np.mean(omf_ctrl[idx])
      anndata['mean_oma_ctrl'][idate,ichan] = np.mean(oma_ctrl[idx])
      anndata['std_omf_ctrl'][idate,ichan]  = np.sqrt(np.mean(omf_ctrl[idx] ** 2))
      anndata['std_oma_ctrl'][idate,ichan]  = np.sqrt(np.mean(oma_ctrl[idx] ** 2))
      del idx
      del useidx
      useidx = (enkf_used == 1)
      idx = np.logical_and(useidx, chanlatidx)
      anndata['mean_omf_ens'][idate,ichan] = np.mean(omf_ens[idx])
      # LEAVING OUT FOR NOW     anndata['mean_oma_ens'][idate,ichan] = np.mean(oma_ens[idx])
      anndata['spread_f'][idate,ichan] = np.sqrt(np.mean(sprd_f[idx]))
      # LEAVING OUT FOR NOW     anndata['spread_a'][idate,ichan] = np.sqrt(np.mean(sprd_a[idx]))
      anndata['spread_obserr_f'][idate,ichan] = np.sqrt(np.mean(sprd_f[idx] + obserr[idx]))
      # LEAVING OUT FOR NOW     anndata['spread_obserr_a'][idate,ichan] = np.sqrt(np.mean(sprd_a[idx] + obserr[idx]))
      anndata['std_omf_ens'][idate,ichan]  = np.sqrt(np.mean(omf_ens[idx] ** 2))
      anndata['mean_biascor'][idate,ichan]=np.mean(biascorr[idx])
      anndata['std_biascor'][idate,ichan]=np.std(biascorr[idx])
   anndata.close()
   

