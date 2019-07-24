from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index


## example diagpath='/lustre/f2/scratch/Oar.Esrl.Nggps_psd/2003stream/'
## 
#def putdate_annual_conv(diagpath, date, var, diagpref, latrange, outfile):
def putdate_annual_conv(diagpath, date, var, latrange, outfile):
   if (var == 'u' or var =='v'):
      vardiag='uv'
      varprefix=var+'_'
   else:
      vardiag=var
      varprefix=''


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


   fname = diagpath+'/'+str(date)+'/diag_conv_'+vardiag+'_ges.'+str(date)+'_control.nc4'
   if (not os.path.isfile(fname)):
      print '---', var, ' not available for ', date
      return
   diag_ctrl_f = Dataset(fname,'r')

   fname = diagpath+'/'+str(date)+'/diag_conv_'+vardiag+'_anl.'+str(date)+'_control.nc4'
   diag_ctrl_a = Dataset(fname,'r')

   ensavail = True
   fname = diagpath+'/'+str(date)+'/diag_conv_'+vardiag+'_ges.ensmean_spread.nc4'
   if (not os.path.isfile(fname)):
     print '---', var, ' ENSSPRD not available for ', date
     ensavail = False
   else:
     diag_ens_sprd = Dataset(fname, 'r')
     omf_ens  = multvar * diag_ens_sprd[varprefix+'EnKF_fit_ges'][:]
     enkf_used = diag_ens_sprd[varprefix+'EnKF_use_flag'][:]
     sprd_f = (multvar**2) * diag_ens_sprd[varprefix+'EnKF_spread_ges'][:]
     sprd_a = (multvar**2) * diag_ens_sprd[varprefix+'EnKF_spread_anl'][:]



   # use diagpref to do u_Observation etc
   nobs = len(diag_ctrl_f.dimensions['nobs'])
   obs = diag_ctrl_f[varprefix+'Observation'][:] * multvar + addtovar


   omf_ctrl = multvar * diag_ctrl_f[varprefix+'Obs_Minus_Forecast_adjusted'][:]
   oma_ctrl = multvar * diag_ctrl_a[varprefix+'Obs_Minus_Forecast_adjusted'][:]

   gsi_used  = diag_ctrl_a['Analysis_Use_Flag'][:]
   obserr = 1. / ( diag_ctrl_f['Errinv_Input'][:]**2 )

   pres = diag_ctrl_f['Pressure'][:]
   lat  = diag_ctrl_f['Latitude'][:]

   latidx = np.logical_and(lat >= np.min(latrange), lat <= np.max(latrange))
   print 'lenlatidx=',len(latidx)
   print 'lenlat=',len(lat)

   anndata = Dataset(outfile, 'a')
   alldate=anndata['All_Dates']
   idate = np.nonzero(alldate[:]==date)[0][0]
   anndata['Full_Dates'][idate] = date

   levs = anndata['Plevels'][:].tolist()
   print 'lenlevs=',len(levs)
   levs.append(10000)
   print 'levs=',levs


   if (var == 'u' or var =='v'):
      obtyp_f=diag_ctrl_f['Observation_Type'][:]
      obtyp_a=diag_ctrl_a['Observation_Type'][:]
      obsubtyp_f=diag_ctrl_f['Observation_Subtype'][:]
      obsubtyp_a=diag_ctrl_a['Observation_Subtype'][:]
      print 'obtype_f=',obtyp_f
      print 'lenobtyp=',len(obtyp_f)
      print 'obtype_a=',obtyp_a
      print 'obsubtype_f=',obsubtyp_f
      print 'obsubtype_a=',obsubtyp_a
      satidx = np.logical_and(obtyp_f >= 240, obtyp_f <= 260)
      print 'satidx=',satidx
      print 'lensatidx=',len(obtyp_f[satidx])
      notsatidx = np.logical_or(obtyp_f < 240, obtyp_f > 260)
      print 'notsatidx=',notsatidx
      print 'lensatidxNOT=',len(obtyp_f[notsatidx])
      dumlatidx = latidx
      del latidx
      latidx = np.logical_and(notsatidx, dumlatidx)
      print 'lenlatidx_UV=',len(obtyp_f[latidx])
      if (len(obtyp_f[latidx])!=len(obtyp_f[dumlatidx])):
          print 'NOTequal, oldlatidx, newlatidx=',len(obtyp_f[dumlatidx]),len(obtyp_f[latidx])
      del dumlatidx

   for ilev in range(len(levs)-1):
      presidx = np.logical_and(pres >= levs[ilev], pres <= levs[ilev+1])
      areaidx = np.logical_and(presidx, latidx)
      useidx  = (gsi_used == 1)
      idx = np.logical_and(useidx, areaidx)
      anndata['nobs_all'][idate,ilev]  = len(obs[areaidx])
      anndata['nobs_used'][idate,ilev] = len(obs[idx])
      anndata['mean_obs_all'][idate,ilev]  = np.mean(obs[areaidx])
      anndata['mean_obs_used'][idate,ilev] = np.mean(obs[idx])
      anndata['mean_omf_ctrl'][idate,ilev] = np.mean(omf_ctrl[idx])
      anndata['mean_oma_ctrl'][idate,ilev] = np.mean(oma_ctrl[idx])
      anndata['std_omf_ctrl'][idate,ilev]  = np.sqrt(np.mean(omf_ctrl[idx] ** 2))
      anndata['std_oma_ctrl'][idate,ilev]  = np.sqrt(np.mean(oma_ctrl[idx] ** 2))
      if (ensavail):
         useidx = (enkf_used == 1)
         idx = np.logical_and(useidx, areaidx)
         anndata['mean_omf_ens'][idate,ilev] = np.mean(omf_ens[idx])
         anndata['spread_f'][idate,ilev] = np.sqrt(np.mean(sprd_f[idx]))
         anndata['spread_obserr_f'][idate,ilev] = np.sqrt(np.mean(sprd_f[idx] + obserr[idx]))
         anndata['std_omf_ens'][idate,ilev]  = np.sqrt(np.mean(omf_ens[idx] ** 2))
   anndata.close()

