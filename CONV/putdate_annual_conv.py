from netCDF4 import Dataset
import numpy as np
import sys, os


def putdate_annual_conv(diagpath, date, var, diagpref, latrange, outfile):
   fname = diagpath+'/diag_conv_'+var+'_ges.'+date+'_control.nc4'
   diag_ctrl_f = Dataset(fname,'r')
   fname = diagpath+'/diag_conv_'+var+'_anl.'+date+'_control.nc4'
   diag_ctrl_a = Dataset(fname,'r')
   fname = diagpath+'/diag_conv_'+var+'_ges.ensmean_spread.nc4'
   diag_ens_sprd = Dataset(fname, 'r')

# move to parameters
   if var == 't':
     addtovar = -273.15
     multvar = 1.0
   elif var == 'q':
     addtovar = 0
     multvar = 1e6
   else:
     addtovar = 0
     multvar =1.0

   # use diagpref to do u_Observation etc
   nobs = len(diag_ctrl_f.dimensions['nobs'])
   obs = diag_ctrl_f['Observation'][:] * multvar + addtovar

   omf_ctrl = multvar * diag_ctrl_f['Obs_Minus_Forecast_adjusted'][:]
   oma_ctrl = multvar * diag_ctrl_a['Obs_Minus_Forecast_adjusted'][:]
   omf_ens  = multvar * diag_ens_sprd['EnKF_fit_ges'][:]
   oma_ens  = multvar * diag_ens_sprd['EnKF_fit_anl'][:]

   gsi_used  = diag_ctrl_a['Analysis_Use_Flag'][:]
   enkf_used = diag_ens_sprd['EnKF_use_flag'][:]
   sprd_f = multvar * diag_ens_sprd['EnKF_spread_ges'][:]
   sprd_a = multvar * diag_ens_sprd['EnKF_spread_anl'][:]
   obserr = 1. / ( diag_ctrl_f['Errinv_Input'][:]**2 )

   pres = diag_ctrl_f['Pressure'][:]
   lat  = diag_ctrl_f['Latitude'][:]

   latidx = np.logical_and(lat >= np.min(latrange), lat <= np.max(latrange))

   anndata_nc = Dataset(outfile, 'a')
   idate = date2index(date, anndata['time'])
   levs = [anndata_nc['Plevels'][:],10000]
   for ilev in range(len(levs)):	
      presidx = np.logical_and(pres >= levs[ilev], pres <= levs[ilev+1])
      areaidx = np.logical_and(presidx, latidx)
      useidx  = (gsi_used == 1)
      idx = np.logical_and(useidx, areaidx)
      anndata['nobs_all'][idate,ilev]  = len(obs[areaidx])
      anndata['nobs_used'][idate,ilev] = len(obs[idx])
      anndata['mean_obs_all'][idate,ilev]  = mean(obs[areaidx])
      anndata['mean_obs_used'][idate,ilev] = mean(obs[idx])
      anndata['mean_omf_ctrl'][idate,ilev] = mean(omf_ctrl[idx])
      anndata['mean_oma_ctrl'][idate,ilev] = mean(oma_ctrl[idx])
      anndata['std_omf_ctrl'][idate,ilev]  = sqrt(mean(omf_ctrl[idx] ** 2))
      anndata['std_oma_ctrl'][idate,ilev]  = sqrt(mean(oma_ctrl[idx] ** 2))
      useidx = (enkf_used == 1)
      idx = np.logical_and(useidx, areaidx)
      anndata['mean_omf_ens'][idate,ilev] = mean(omf_ens[idx])
      anndata['mean_oma_ens'][idate,ilev] = mean(oma_ens[idx])
      anndata['spread_f'][idate,ilev] = sqrt(mean(sprd_f[idx]))
      anndata['spread_a'][idate,ilev] = sqrt(mean(sprd_a[idx]))
      anndata['spread_obserr_f'][idate,ilev] = sqrt(mean(sprd_f[idx] + obserr[idx]))
      anndata['spread_obserr_a'][idate,ilev] = sqrt(mean(sprd_a[idx] + obserr[idx]))
      anndata['std_omf_ens'][idate,ilev]  = sqrt(mean(omf_ens[idx] ** 2))
      anndata['std_oma_ens'][idate,ilev]  = sqrt(mean(oma_ens[idx] ** 2))

		
