from time import clock
import numpy as np
from netCDF4 import Dataset
import sys, os
import math
##########################################################################################

## DIMENSIONS
## NDAYSperYR X 4 for Ntime
## Nlevs 
## python make_TEMPLATE.py <stream start year> <data year> <variable> <region>
## e.g. python make_RAD_TEMPLATE.py 2003 2004 'AMSUA' 'n15' 'GLOBL'
if len(sys.argv) < 6:
    raise SystemExit('python make_TEMPLATE.py <stream start year> <data year> <instrument> <satellite> <region>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
instrmnt = sys.argv[3] #e.g. AMSUA,IASI
satlite = sys.argv[4] #e.g. n15
region = sys.argv[5]

annual_filename='FV3s'+str(streamyr)+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'

if float(datayr)/4!=datayr/4 or datayr==2000:
   ndays=365
else:
   ndays=366

total_ntime=ndays*4

anndata_nc = Dataset(annual_filename,'w',format='NETCDF4')
#anndata_nc.createDimension('Ncycles',None)
anndata_nc.createDimension('Ncycles',total_ntime)
anndata_nc.createDimension('Nchans',None)

anndata_nc.createVariable('All_Dates',np.int,('Ncycles'),zlib=False)
anndata_nc.createVariable('Full_Dates',np.int,('Ncycles'),zlib=False)
anndata_nc.createVariable('Channels',np.float32,('Nchans'),zlib=False)

anndata_nc.createVariable('nobs_all',np.int,('Ncycles','Nchans',),zlib=False)
anndata_nc.createVariable('nobs_used',np.int,('Ncycles','Nchans',),zlib=False)
anndata_nc.createVariable('nobs_qcd',np.int,('Ncycles','Nchans',),zlib=False)  ##

anndata_nc.createVariable('mean_obs_all',np.float32,('Ncycles','Nchans',),zlib=False)
anndata_nc.createVariable('mean_obs_used',np.float32,('Ncycles','Nchans',),zlib=False)
anndata_nc.createVariable('mean_obs_qcd',np.float32,('Ncycles','Nchans',),zlib=False)  ##

anndata_nc.createVariable('mean_omf_ctrl',np.float32,('Ncycles','Nchans',),zlib=False)##OmF_wBC_mean
anndata_nc.createVariable('mean_omf_ens',np.float32,('Ncycles','Nchans',),zlib=False)##ENS_OmF_wBC_mean
anndata_nc.createVariable('mean_oma_ctrl',np.float32,('Ncycles','Nchans',),zlib=False)##OmA_wBC_mean
anndata_nc.createVariable('mean_oma_ens',np.float32,('Ncycles','Nchans',),zlib=False)##ENS_OmA_wBC_mean

anndata_nc.createVariable('mean_biascor',np.float32,('Ncycles','Nchans',),zlib=False)
anndata_nc.createVariable('std_biascor',np.float32,('Ncycles','Nchans',),zlib=False)

anndata_nc.createVariable('spread_f',np.float32,('Ncycles','Nchans',),zlib=False)##ENSspredF_mean
anndata_nc.createVariable('std_omf_ens',np.float32,('Ncycles','Nchans',),zlib=False)##ENS_OmF_wBC_std
anndata_nc.createVariable('std_omf_ctrl',np.float32,('Ncycles','Nchans',),zlib=False)##OmF_wBC_std
anndata_nc.createVariable('spread_obserr_f',np.float32,('Ncycles','Nchans',),zlib=False)##ENSsprederrF_mean
anndata_nc.createVariable('spread_a',np.float32,('Ncycles','Nchans',),zlib=False)##ENSspredA_mean
anndata_nc.createVariable('std_oma_ens',np.float32,('Ncycles','Nchans',),zlib=False)##ENS_OmA_wBC_std
anndata_nc.createVariable('std_oma_ctrl',np.float32,('Ncycles','Nchans',),zlib=False)##OmA_wBC_std
anndata_nc.createVariable('spread_obserr_a',np.float32,('Ncycles','Nchans',),zlib=False)##ENSsprederrA_mean


anndata_nc.close()



## ??OmF_noBC_mean
## ??OmF_noBC_std
## ??OmA_noBC_mean
## ??OmA_noBC_std
#IDsat
#CHANnum





























