from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index


def putdate_annual_rad(diagpath, date, stream, instrmnt, satlite, outputpath): 
   #print 'putdate_annual_rad:',date
   anlcontrolnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_anl.'+str(date)+'_control.nc4'
   if (not os.path.isfile(anlcontrolnc_file)):
      print instrmnt, satlite, ' not available for ', date
      return
   print anlcontrolnc_file
   diag_ctrl_a = Dataset(anlcontrolnc_file,'r')
   gescontrolnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_ges.'+str(date)+'_control.nc4'
   diag_ctrl_f = Dataset(gescontrolnc_file,'r')
   ensmeannc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_ges.'+str(date)+'_ensmean.nc4'
   diag_ens_mean = Dataset(ensmeannc_file,'r')
   enssprdnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_ges.'+str(date)+'_ensmean_spread.nc4'
   diag_ens_sprd = Dataset(enssprdnc_file,'r')

   ###############################################################################
   chanindx_diag = diag_ctrl_a['Channel_Index'][:]
   nobs_anl=len(chanindx_diag)
   chanlist_diag = diag_ctrl_a['sensor_chan'][:]
   obs = diag_ctrl_f['Observation'][:]
   
   obserr_diag = diag_ctrl_f['error_variance'][:]

   chan_diag=np.zeros(nobs_anl)
   obserr = np.zeros(nobs_anl)
   for m in range(nobs_anl):
      chan_diag[m]=chanlist_diag[chanindx_diag[m]-1]
      obserr[m] = obserr_diag[chanindx_diag[m]-1]**2

   lat  = diag_ctrl_f['Latitude'][:]

   omf_ctrl = diag_ctrl_f['Obs_Minus_Forecast_adjusted'][:]
   oma_ctrl = diag_ctrl_a['Obs_Minus_Forecast_adjusted'][:]
   omf_ens  = diag_ens_sprd['EnKF_fit_ges'][:]
   oma_ens  = diag_ens_sprd['EnKF_fit_anl'][:]

   gsi_used  = diag_ctrl_a['use_flag'][:] ##dimension nchan... says whether the channel is used in GSI
   enkf_used = diag_ens_sprd['EnKF_use_flag'][:] ##dimension nobs....
   gsi_qcd  = diag_ctrl_a['QC_Flag'][:]

   sprd_f =  diag_ens_sprd['EnKF_spread_ges'][:]
   sprd_a =  diag_ens_sprd['EnKF_spread_anl'][:]

   biascorr = diag_ctrl_f['Obs_Minus_Forecast_adjusted'][:] - diag_ctrl_f['Obs_Minus_Forecast_unadjusted'][:]

   regions=['GLOBL','TROPI','NORTH','SOUTH']

   for region in regions:
     if region=='GLOBL':
        latrange=[-90, 90]
     elif region=='TROPI':
        latrange=[-20,20]
     elif region=='SOUTH':
        latrange=[-90,-20]
     elif region=='NORTH':
        latrange=[20,90]

     datayr = date / 1000000
     outfile=outputpath+'/RAD_'+stream+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
     print outfile
     latidx = np.logical_and(lat >= np.min(latrange), lat <= np.max(latrange))

     anndata = Dataset(outfile, 'a')
     alldate=anndata['All_Dates']
     idate = np.nonzero(alldate[:]==date)[0][0]
     anndata['Full_Dates'][idate] = date
  
     ##### ['Ncycles','Nchans']
     chans = anndata['Channels'][:].tolist()
     #print 'lenchan=',len(chans)
     for ichan in range(len(chans)):
        chanidx    = (chan_diag==chans[ichan])
        chanlatidx = np.logical_and(chanidx, latidx)
        qcdidx  = (gsi_qcd == 0)
        qidx    = np.logical_and(qcdidx, chanlatidx)
        anndata['nobs_all'][idate,ichan]  = len(obs[chanlatidx])
        anndata['nobs_qcd'][idate,ichan] = len(obs[qidx])
        anndata['mean_obs_all'][idate,ichan]  = np.nan 
        anndata['mean_obs_used'][idate,ichan] = np.mean(obs[qidx])
        anndata['mean_obs_qcd'][idate,ichan] = np.mean(obs[qidx])
        anndata['mean_omf_ctrl'][idate,ichan] = np.mean(omf_ctrl[qidx])
        anndata['mean_oma_ctrl'][idate,ichan] = np.mean(oma_ctrl[qidx])
        anndata['std_omf_ctrl'][idate,ichan]  = np.sqrt(np.mean(omf_ctrl[qidx] ** 2))
        anndata['std_oma_ctrl'][idate,ichan]  = np.sqrt(np.mean(oma_ctrl[qidx] ** 2))
        useidx = (enkf_used == 1)  ## for enkf use only
        idx    = np.logical_and(useidx, chanlatidx)
        anndata['nobs_used'][idate,ichan] = len(obs[idx])
        anndata['mean_omf_ens'][idate,ichan] = np.mean(omf_ens[idx])
        # LEAVING OUT FOR NOW     anndata['mean_oma_ens'][idate,ichan] = np.mean(oma_ens[idx])
        anndata['spread_f'][idate,ichan] = np.sqrt(np.mean(sprd_f[idx]))
        # LEAVING OUT FOR NOW     anndata['spread_a'][idate,ichan] = np.sqrt(np.mean(sprd_a[idx]))
        anndata['spread_obserr_f'][idate,ichan] = np.sqrt(np.mean(sprd_f[idx]) + np.mean(obserr[idx]))
        # LEAVING OUT FOR NOW     anndata['spread_obserr_a'][idate,ichan] = np.sqrt(np.mean(sprd_a[idx] + obserr[idx]))
        anndata['std_omf_ens'][idate,ichan]  = np.sqrt(np.mean(omf_ens[idx] ** 2))
        anndata['mean_biascor'][idate,ichan] = np.mean(biascorr[idx])
        anndata['std_biascor'][idate,ichan]  = np.std(biascorr[idx])
     anndata.close()
   

