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
## e.g. python make_TEMPLATE.py 2003 2004 'U' 'GLOBL'
if len(sys.argv) < 5:
    raise SystemExit('python make_TEMPLATE.py <stream start year> <data year> <variable> <region>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
varb = sys.argv[3]
region = sys.argv[4]

annual_filename='FV3s'+str(streamyr)+'_'+str(datayr)+'_'+varb+'_'+region+'.nc'

if float(datayr)/4!=datayr/4 or datayr==2000:
   ndays=365
else:
   ndays=366

total_ntime=ndays*4
pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
nlevs=len(pcutoffs)


anndata_nc = Dataset(annual_filename,'w',format='NETCDF4')
#anndata_nc.createDimension('Ncycles',None)
anndata_nc.createDimension('Ncycles',total_ntime)
anndata_nc.createDimension('Nlevs',None)

anndata_nc.createVariable('nobs_all',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('nobs_used',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('mean_obs_all',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('mean_obs_used',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('mean_omf_ctrl',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('mean_omf_ens',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('mean_oma_ctrl',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('mean_oma_ens',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('spread_f',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('std_omf_ens',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('std_omf_ctrl',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('spread_obserr_f',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('spread_a',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('std_oma_ens',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('std_oma_ctrl',np.float32,('Ncycles','Nlevs',),zlib=False)
anndata_nc.createVariable('spread_obserr_a',np.float32,('Ncycles','Nlevs',),zlib=False)

anndata_nc.close()





