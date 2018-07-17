from netCDF4 import Dataset
import numpy as np
import os
import read_diag

def putdate_CFSR_annual_conv(diagpath, date, outputpath):
   #######################################
   fname_ges = diagpath+'/'+str(date)+'/diag_conv_ges.'+str(date)
   print 'fname ges=',fname_ges
   
   fname_anl = diagpath+'/'+str(date)+'/diag_conv_anl.'+str(date)
   print 'fname anl=',fname_anl
   
   diag_ctrl_f = read_diag.diag_conv(fname_ges,endian='big',fformat='old')
   diag_ctrl_f.read_obs()
   diag_ctrl_a = read_diag.diag_conv(fname_anl,endian='big',fformat='old')
   diag_ctrl_a.read_obs()
   
   nobs_all = diag_ctrl_f.nobs
   print('nobs=',nobs_all)

   varnames = ['  t',  '  u', '  v', '  q', ' ps', 'gps']
   addtovar = [ -273.15,   0,     0,     0,     0,     0]
   multvar  = [       1,   1,     1,  1.e6,     1,     1]
   
   regions=['GLOBL','TROPI','SOUTH','NORTH']
   minlat =[    -90,    -20,    -90,    20]
   maxlat =[     90,     20,    -20,    90]

   obs      = diag_ctrl_a.obs
   omf_ctrl = diag_ctrl_f.obs - diag_ctrl_f.hx
   oma_ctrl = diag_ctrl_a.obs - diag_ctrl_a.hx
   pres     = diag_ctrl_f.press
   lat      = diag_ctrl_f.lat
   gsi_used = diag_ctrl_f.used
   obtype   = diag_ctrl_f.obtype

   useidx = (gsi_used == 1)
   for ivar in range(len(varnames)):
     varidx = varnames[ivar] == obtype
     for ireg in range(len(regions)):
       latidx = np.logical_and(lat >= minlat[ireg], lat <= maxlat[ireg])
       varlatidx = np.logical_and(varidx, latidx)
       outfile=outputpath+'/CONV_CFSR_'+str(date)[0:4]+'_'+varnames[ivar].strip()+'_'+regions[ireg]+'.nc'
       anndata = Dataset(outfile, 'a')

       alldate=anndata['All_Dates']
       idate = np.nonzero(alldate[:]==date)[0][0]
       anndata['Full_Dates'][idate] = date
   
       levs = anndata['Plevels'][:].tolist()
       levs.append(10000)

       for ilev in range(len(levs)-1):
         presidx = np.logical_and(pres >= levs[ilev], pres <= levs[ilev+1])
         areaidx = np.logical_and(presidx, varlatidx)
         idx     = np.logical_and(useidx, areaidx)
         anndata['nobs_all'][idate,ilev]  = len(obs[areaidx])
         anndata['nobs_used'][idate,ilev] = len(obs[idx])
         anndata['mean_obs_all'][idate,ilev]  = np.mean(obs[areaidx])*multvar[ivar]+addtovar[ivar]
         anndata['mean_obs_used'][idate,ilev] = np.mean(obs[idx])*multvar[ivar]+addtovar[ivar]
         anndata['mean_omf_ctrl'][idate,ilev] = np.mean(omf_ctrl[idx])*multvar[ivar]
         anndata['mean_oma_ctrl'][idate,ilev] = np.mean(oma_ctrl[idx])*multvar[ivar]
         anndata['std_omf_ctrl'][idate,ilev]  = np.sqrt(np.mean(omf_ctrl[idx] ** 2))*multvar[ivar]
         anndata['std_oma_ctrl'][idate,ilev]  = np.sqrt(np.mean(oma_ctrl[idx] ** 2))*multvar[ivar]
         # no info from ensemble in CFSR
         anndata['mean_omf_ens'][idate,ilev] = np.nan
         anndata['mean_oma_ens'][idate,ilev] = np.nan
         anndata['std_omf_ens'][idate,ilev]  = np.nan
         anndata['std_oma_ens'][idate,ilev]  = np.nan
         anndata['spread_f'][idate,ilev] = np.nan
         anndata['spread_a'][idate,ilev] = np.nan
         anndata['spread_obserr_f'][idate,ilev] = np.nan
         anndata['spread_obserr_a'][idate,ilev] = np.nan
       anndata.close()

