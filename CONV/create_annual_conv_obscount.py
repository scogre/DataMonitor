import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta

## DIMENSIONS
## NDAYSperYR X 4 for Ntime
def create_annual_conv_obscount(outfile, datayr):
   if float(datayr)/4!=int(datayr)/4 or int(datayr)==2000:
      ndays=365
   else:
      ndays=366
   total_ntime=ndays*4
   anndata_nc = Dataset(outfile,'w',format='NETCDF4')
   anndata_nc.createDimension('Ncycles', total_ntime)
   
   anndata_nc.createVariable('All_Dates',np.int,('Ncycles'),zlib=False)
   anndata_nc.createVariable('Full_Dates',np.int,('Ncycles'),zlib=False)

   dates = [datetime(int(datayr),1,1)+i*timedelta(hours=6) for i in range(total_ntime)]
   alldate=[dates[i].strftime('%Y%m%d%H') for i in range(total_ntime)]
   anndata_nc['All_Dates'][:] = alldate[:]

   anndata_nc.createVariable('nobs_used',np.int,('Ncycles',),zlib=False)
   anndata_nc.createVariable('nobs_acft',np.int,('Ncycles',),zlib=False)
   anndata_nc.createVariable('nobs_sfc', np.int,('Ncycles',),zlib=False)
   anndata_nc.createVariable('nobs_sond',np.int,('Ncycles',),zlib=False)
   anndata_nc.createVariable('nobs_prof',np.int,('Ncycles',),zlib=False)
   anndata_nc.createVariable('nobs_satw',np.int,('Ncycles',),zlib=False)
   anndata_nc.createVariable('nobs_scatw',np.int,('Ncycles',),zlib=False)
   anndata_nc.createVariable('nobs_other',np.int,('Ncycles',),zlib=False)
   
   anndata_nc.close()


