from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index


def putdate_annual_rad(diagpath, date, stream, instrmnt, satlite, outputpath): 
   #print 'putdate_annual_rad:',date
   anlcontrolnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_anl.'+str(date)+'_control.nc4'
   if (not os.path.isfile(anlcontrolnc_file)):
      print '---', instrmnt, satlite, ' not available for ', date
      return
   diag_ctrl_a = Dataset(anlcontrolnc_file,'r')
   gescontrolnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_ges.'+str(date)+'_control.nc4'
   diag_ctrl_f = Dataset(gescontrolnc_file,'r')
   enssprdnc_file =  diagpath+'/'+str(date)+'/diag_'+instrmnt+'_'+satlite+'_ges.'+str(date)+'_ensmean_spread.nc4'
   sprdavail = False
   if (os.path.isfile(enssprdnc_file)):
     sprdavail = True
     diag_ens_sprd = Dataset(enssprdnc_file,'r')
     enkf_used = diag_ens_sprd['EnKF_use_flag'][:] ##dimension nobs....
     sprd_f =  diag_ens_sprd['EnKF_spread_ges'][:]
     omf_ens  = diag_ens_sprd['EnKF_fit_ges'][:]

   print 'Filling in ', instrmnt, satlite, ' for ', date

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

   gsi_used  = diag_ctrl_a['use_flag'][:] ##dimension nchan... says whether the channel is used in GSI
   gsi_qcd  = diag_ctrl_a['QC_Flag'][:]

   biascorr = diag_ctrl_f['Obs_Minus_Forecast_adjusted'][:] - diag_ctrl_f['Obs_Minus_Forecast_unadjusted'][:]

   regions=['GLOBL','TROPI','SOUTH','NORTH']
   minlat =[    -90,    -20,    -90,    20]
   maxlat =[     90,     20,    -20,    90]

   for ireg in range(len(regions)):
     outfile=outputpath+'/RAD_'+stream+'_'+str(date)[0:4]+'_'+instrmnt+'_'+satlite+'_'+regions[ireg]+'.nc'
     latidx = np.logical_and(lat >= minlat[ireg], lat <= maxlat[ireg])

     anndata = Dataset(outfile, 'a')
     alldate=anndata['All_Dates']
     idate = np.nonzero(alldate[:]==int(date))[0][0]
     anndata['Full_Dates'][idate] = int(date)
  
     ##### ['Ncycles','Nchans']
     chans = anndata['Channels'][:].tolist()
     for ichan in range(len(chans)):
        chanidx    = (chan_diag==chans[ichan])
        chanlatidx = np.logical_and(chanidx, latidx)
        obsidx = np.logical_and(obs < 1.e8, chanlatidx)
        qcdidx  = (gsi_qcd == 0)
        qidx    = np.logical_and(qcdidx, chanlatidx)
        anndata['nobs_all'][idate,ichan]  = len(obs[chanlatidx])
        anndata['nobs_qcd'][idate,ichan] = len(obs[qidx])
        anndata['mean_obs_all'][idate,ichan]  = np.mean(obs[obsidx])
        anndata['mean_obs_used'][idate,ichan] = np.mean(obs[qidx])
        anndata['mean_obs_qcd'][idate,ichan]  = np.mean(obs[qidx])
        anndata['mean_omf_ctrl'][idate,ichan] = np.mean(omf_ctrl[qidx])
        anndata['mean_oma_ctrl'][idate,ichan] = np.mean(oma_ctrl[qidx])
        anndata['std_omf_ctrl'][idate,ichan]  = np.sqrt(np.mean(omf_ctrl[qidx] ** 2))
        anndata['std_oma_ctrl'][idate,ichan]  = np.sqrt(np.mean(oma_ctrl[qidx] ** 2))
        if (sprdavail):
          useidx = (enkf_used == 1)  ## for enkf use only
          idx    = np.logical_and(useidx, chanlatidx)
          anndata['nobs_used'][idate,ichan] = len(obs[idx])
          anndata['mean_omf_ens'][idate,ichan] = np.mean(omf_ens[idx])
          anndata['spread_f'][idate,ichan] = np.sqrt(np.mean(sprd_f[idx]))
          anndata['spread_obserr_f'][idate,ichan] = np.sqrt(np.mean(sprd_f[idx]) + np.mean(obserr[idx]))
          anndata['std_omf_ens'][idate,ichan]  = np.sqrt(np.mean(omf_ens[idx] ** 2))
        anndata['mean_biascor'][idate,ichan] = np.mean(biascorr[qidx])
        anndata['std_biascor'][idate,ichan]  = np.std(biascorr[qidx])
     anndata.close()
   

