from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index


## example diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/2003stream/'
## 
#def putdate_annual_conv(diagpath, date, var, diagpref, latrange, outfile):
def putdate_annual_conv(diagpath, date, var, latrange, outfile):

   fname = diagpath+'/'+str(date)+'/diag_conv_'+var+'_ges.'+str(date)+'_ensmean.nc4'
   print 'fname 1=',fname
   diag_ctrl_f = Dataset(fname,'r')

   fname = diagpath+'/'+str(date)+'/diag_conv_'+var+'_anl.'+str(date)+'_control.nc4'
   print 'fname 2=',fname
   diag_ctrl_a = Dataset(fname,'r')

   fname = diagpath+'/'+str(date)+'/diag_conv_'+var+'_ges.ensmean_spread.nc4'
   print 'fname 3=',fname
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
   print 'lengsiused=',len(gsi_used)
   enkf_used = diag_ens_sprd['EnKF_use_flag'][:]
   sprd_f = (multvar**2) * diag_ens_sprd['EnKF_spread_ges'][:]
   sprd_a = (multvar**2) * diag_ens_sprd['EnKF_spread_anl'][:]
   obserr = 1. / ( diag_ctrl_f['Errinv_Input'][:]**2 )

   pres = diag_ctrl_f['Pressure'][:]
   lat  = diag_ctrl_f['Latitude'][:]

   latidx = np.logical_and(lat >= np.min(latrange), lat <= np.max(latrange))
   print 'lenlatidx=',len(latidx)
   print 'lenlat=',len(lat)

   anndata = Dataset(outfile, 'a')
#   idate = date2index(date, anndata['time'])
   alldate=anndata['All_Dates']
   idate = np.nonzero(alldate[:]==date)[0][0]
   anndata['Full_Dates'][idate] = date

   levs = anndata['Plevels'][:].tolist()
   #levs=np.asarray(levs)
   print 'lenlevs=',len(levs)
   levs.append(10000)
   print 'levs=',levs
   for ilev in range(len(levs)-1):
      print 'levs[ilev],levs[ilev+1]=',levs[ilev],levs[ilev+1]	
      presidx = np.logical_and(pres >= levs[ilev], pres <= levs[ilev+1])
      areaidx = np.logical_and(presidx, latidx)
      useidx  = (gsi_used == 1)
      print 'useidx  =',useidx
      print 'areaidx  =',areaidx
      print 'lenuse=',len(useidx)
      print 'lenarea=',len(areaidx)
      idx = np.logical_and(useidx, areaidx)
      anndata['nobs_all'][idate,ilev]  = len(obs[areaidx])
      anndata['nobs_used'][idate,ilev] = len(obs[idx])
      anndata['mean_obs_all'][idate,ilev]  = np.mean(obs[areaidx])
      anndata['mean_obs_used'][idate,ilev] = np.mean(obs[idx])
      anndata['mean_omf_ctrl'][idate,ilev] = np.mean(omf_ctrl[idx])
      anndata['mean_oma_ctrl'][idate,ilev] = np.mean(oma_ctrl[idx])
      anndata['std_omf_ctrl'][idate,ilev]  = np.sqrt(np.mean(omf_ctrl[idx] ** 2))
      anndata['std_oma_ctrl'][idate,ilev]  = np.sqrt(np.mean(oma_ctrl[idx] ** 2))
      useidx = (enkf_used == 1)
      idx = np.logical_and(useidx, areaidx)
      anndata['mean_omf_ens'][idate,ilev] = np.mean(omf_ens[idx])
# LEAVING OUT FOR NOW     anndata['mean_oma_ens'][idate,ilev] = np.mean(oma_ens[idx])
      anndata['spread_f'][idate,ilev] = np.sqrt(np.mean(sprd_f[idx]))
# LEAVING OUT FOR NOW     anndata['spread_a'][idate,ilev] = np.sqrt(np.mean(sprd_a[idx]))
      anndata['spread_obserr_f'][idate,ilev] = np.sqrt(np.mean(sprd_f[idx] + obserr[idx]))
# LEAVING OUT FOR NOW     anndata['spread_obserr_a'][idate,ilev] = np.sqrt(np.mean(sprd_a[idx] + obserr[idx]))
      anndata['std_omf_ens'][idate,ilev]  = np.sqrt(np.mean(omf_ens[idx] ** 2))
#      print 'oma_ens[idx]=',oma_ens[idx]
#      print 'oma_ens[idx]**2=',(oma_ens[idx] ** 2)
      anndata['std_oma_ens'][idate,ilev]  = np.sqrt(np.mean(oma_ens[idx] ** 2))
   anndata.close()	
