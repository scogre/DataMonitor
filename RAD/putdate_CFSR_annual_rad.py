from netCDF4 import Dataset
import numpy as np
import os
import read_diag

def putdate_CFSR_annual_rad(diagpath, date, instrmnt, sat, outputpath):
   date10dig=str(date)

   diaganl_obsfile = diagpath + '/' + date10dig + '/diag_'  +  instrmnt + '_' + sat + '_anl.' + date10dig
   if (not os.path.isfile(diaganl_obsfile)):
      print '---', instrmnt, sat, ' not available for ', date
      return
   print 'Filling in ', instrmnt, sat, ' for ', date

   diaganl_rad = read_diag.diag_rad(diaganl_obsfile,endian='big')
   diaganl_rad.read_obs()
   
   nobs = diaganl_rad.nobs
   lat  = diaganl_rad.lat
   chan = diaganl_rad.channel
   obs  = diaganl_rad.obs
   obserr = diaganl_rad.oberr_orig
   gsi_used = diaganl_rad.used
   gsi_qcd  = diaganl_rad.qcmark
   oma_ctrl = obs - diaganl_rad.hx
   #############################
   
   diagges_obsfile = diagpath +date10dig+ '/diag_'  +  instrmnt + '_' + sat + '_ges.' + date10dig
   diagges_rad = read_diag.diag_rad(diagges_obsfile,endian='big')
   diagges_rad.read_obs()

   omf_ctrl = obs - diagges_rad.hx
   biascorr = diagges_rad.biascorr
   ###########################################

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
  
     outfile=outputpath+'/RAD_CFSR_'+str(date)[0:4]+'_'+instrmnt+'_'+sat+'_'+region+'.nc'
     latidx = np.logical_and(lat >= np.min(latrange), lat <= np.max(latrange))
     ############################################
  
     anndata = Dataset(outfile, 'a')
     alldate=anndata['All_Dates']
     idate = np.nonzero(alldate[:]==int(date))[0][0]
     anndata['Full_Dates'][idate] = int(date)
     ##### ['Ncycles','Nchans']
     chans = anndata['Channels'][:].tolist()
     for ichan in range(len(chans)):
        chanidx    = (chan==chans[ichan])
        chanlatidx = np.logical_and(chanidx, latidx)
        qcdidx     = (gsi_qcd == 0)
        qidx       = np.logical_and(qcdidx, chanlatidx)
        anndata['nobs_all'][idate,ichan]  = len(obs[chanlatidx])
        anndata['nobs_qcd'][idate,ichan]  = len(obs[qidx])
        anndata['mean_obs_all'][idate,ichan]  = np.mean(obs[chanlatidx])
        anndata['mean_obs_used'][idate,ichan] = np.mean(obs[qidx])
        anndata['mean_obs_qcd'][idate,ichan]  = np.mean(obs[qidx])
        anndata['mean_omf_ctrl'][idate,ichan] = np.mean(omf_ctrl[qidx])
        anndata['mean_oma_ctrl'][idate,ichan] = np.mean(oma_ctrl[qidx])
        anndata['std_omf_ctrl'][idate,ichan]  = np.sqrt(np.mean(omf_ctrl[qidx] ** 2))
        anndata['std_oma_ctrl'][idate,ichan]  = np.sqrt(np.mean(oma_ctrl[qidx] ** 2))
        anndata['nobs_used'][idate,ichan] = len(obs[qidx])
        anndata['mean_biascor'][idate,ichan]=np.mean(biascorr[qidx])
        anndata['std_biascor'][idate,ichan]=np.std(biascorr[qidx])
        # no info from ensemble in CFSR:
     anndata.close()






