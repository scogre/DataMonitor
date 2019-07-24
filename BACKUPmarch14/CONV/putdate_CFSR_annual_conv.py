from netCDF4 import Dataset
import numpy as np
import sys, os
from netCDF4 import num2date, date2num, date2index
import read_diag


def putdate_CFSR_annual_conv(diagpath, date, var, latrange, outfile):
   if var == 'ps':
      pcutoffs=[0]
   else:
      pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
   
   #######################################
   space=' '
   if (var == 'u' or var =='v'):
      vardiag='uv'
      varprefix=var+'_'
   else:
      vardiag=var
      varprefix=''
   
   fname_ges = diagpath+'/'+str(date)+'/diag_conv_ges.'+str(date)
   print 'fname ges=',fname_ges
   
   fname_anl = diagpath+'/'+str(date)+'/diag_conv_anl.'+str(date)
   print 'fname anl=',fname_anl
   
   try:
      print('initial try')
      diag_ctrl_f = read_diag.diag_conv(fname_ges,endian='big')
      diag_ctrl_f.read_obs()
      print('f read, now a read')
      diag_ctrl_a = read_diag.diag_conv(fname_anl,endian='big')
      diag_ctrl_a.read_obs()
   except:
      print('exception')
      diag_ctrl_f = read_diag.diag_conv(fname_ges,endian='big',fformat='old')
      diag_ctrl_f.read_obs()
      print('f read, now a read')
      diag_ctrl_a = read_diag.diag_conv(fname_anl,endian='big',fformat='old')
      diag_ctrl_a.read_obs()
   
   nobs_diag=diag_ctrl_f.nobs
   print('nobs_diag=',nobs_diag)
   
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
   
   obs=[]
   omf_ctrl=[]
   oma_ctrl=[]
   pres=[]
   lat=[]
   obserr=[]
   gsi_used=[]

   for nob in range(nobs_diag):
      obtype = diag_ctrl_a.obtype[nob]
      obtype = "".join(c for c in obtype if c not in space)
      if obtype==var:
         obs.append(diag_ctrl_a.obs[nob] * multvar + addtovar)
         omf_ctrl.append(multvar * diag_ctrl_f.hx[nob])
         oma_ctrl.append(multvar * diag_ctrl_a.hx[nob])
         pres.append(diag_ctrl_f.press[nob])
         lat.append(diag_ctrl_f.lat[nob])
         obserr.append(diag_ctrl_a.oberr[nob])
         gsi_used.append(diag_ctrl_f.used[nob])
   nobs=len(obs)
   print('nobs=',nobs)
   #print('pres=',pres)
   print 'lenuse=',len(gsi_used)
   print 'minpres=',np.min(pres)
   print 'mindx=',pres.index(np.min(pres))
   #
   latidx = np.logical_and(lat >= np.min(latrange), lat <= np.max(latrange))
   print 'lenlatidx=',len(latidx)
   print 'lenlat=',len(lat)
   
   anndata = Dataset(outfile, 'a')
   #idate = date2index(date, anndata['time'])
   alldate=anndata['All_Dates']
   idate = np.nonzero(alldate[:]==date)[0][0]
   anndata['Full_Dates'][idate] = date
   print 'idate=',idate
   
   levs = anndata['Plevels'][:].tolist()
   #levs=np.asarray(levs)
   print 'lenlevs=',len(levs)
   levs.append(10000)
   print 'levs=',levs
   for ilev in range(len(levs)-1):
      print 'levs[ilev],levs[ilev+1]=',levs[ilev],levs[ilev+1]
      presidx = np.logical_and(np.asarray(pres) >= levs[ilev], np.asarray(pres) <= levs[ilev+1])
      print 'presidx  =',presidx
      areaidx = np.logical_and(presidx, latidx)
      #useidx  = (gsi_used == 1)
      useidx = (np.asarray(gsi_used) == 1)
      #useidx = np.where(np.asarray(gsi_used) == 1)
      print 'useidx  =',useidx
      print 'areaidx  =',areaidx
      print 'lenuse=',len(useidx)
      print 'lenarea=',len(areaidx)
      idx = np.logical_and(useidx, areaidx)
      print 'idx=',idx
      print 'lenidx=',len(idx)
      print 'idate,ilev,lenareaidx=',idate,ilev,len(areaidx)
      anndata['nobs_all'][idate,ilev]  = len(areaidx)
      anndata['nobs_used'][idate,ilev] = len(idx)
      anndata['mean_obs_all'][idate,ilev]  = np.mean(np.asarray(obs)[areaidx])
      anndata['mean_obs_used'][idate,ilev] = np.mean(np.asarray(obs)[idx])
      anndata['mean_omf_ctrl'][idate,ilev] = np.mean(np.asarray(omf_ctrl)[idx])
      anndata['mean_oma_ctrl'][idate,ilev] = np.mean(np.asarray(oma_ctrl)[idx])
      anndata['std_omf_ctrl'][idate,ilev]  = np.sqrt(np.mean(np.asarray(omf_ctrl)[idx] ** 2))
      anndata['std_oma_ctrl'][idate,ilev]  = np.sqrt(np.mean(np.asarray(oma_ctrl)[idx] ** 2))
      #useidx = (enkf_used == 1)
      #idx = np.logical_and(useidx, areaidx)
      #anndata['mean_omf_ens'][idate,ilev] = np.mean(np.asarray(omf_ens)[idx])
      #anndata['spread_f'][idate,ilev] = np.sqrt(np.mean(np.asarray(sprd_f)[idx]))
      #anndata['spread_obserr_f'][idate,ilev] = np.sqrt(np.mean(np.asarray(sprd_f)[idx] + np.asarray(obserr)[idx]))
      #anndata['std_omf_ens'][idate,ilev]  = np.sqrt(np.mean(np.asarray(omf_ens)[idx] ** 2))
      #print 'oma_ens[idx]=',oma_ens[idx]
      #print 'oma_ens[idx]**2=',(oma_ens[idx] ** 2)
      #anndata['std_oma_ens'][idate,ilev]  = np.sqrt(np.mean(np.asarray(oma_ens)[idx] ** 2))
   anndata.close()

