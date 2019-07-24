import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta
from netCDF4 import num2date, date2num
import time

## DIMENSIONS
## NDAYSperYR X 4 for Ntime
## Nlevs  
def create_annual_conv(outfile, modelstream, datayr, varb, region, pcutoffs):
   annual_filename = outfile
   if float(datayr)/4!=datayr/4 or datayr==2000:
      ndays=365
   else:
      ndays=366
   total_ntime=ndays*4
   nlevs=len(pcutoffs)
   anndata_nc = Dataset(annual_filename,'w',format='NETCDF4')
   anndata_nc.createDimension('Ncycles', total_ntime)
   anndata_nc.createDimension('Nlevs', nlevs)
   
   anndata_nc.createVariable('All_Dates',np.int,('Ncycles'),zlib=False)
   anndata_nc.createVariable('Full_Dates',np.int,('Ncycles'),zlib=False)

   dates = [datetime(datayr,1,1)+i*timedelta(hours=6) for i in range(total_ntime)]
   alldate=[dates[i].strftime('%Y%m%d%H') for i in range(total_ntime)]
   anndata_nc['All_Dates'][:] = alldate[:]

######
#   times = anndata_nc.createVariable('time',np.float64,('Ncycles'),zlib=False)
#   times.units = "hours since 0001-01-01 00:00:00.0"
#   times.calendar = "gregorian"
#   times[:] = date2num(dates,units=times.units,calendar=times.calendar)
######


   anndata_nc.createVariable('Plevels',np.float32,('Nlevs'),zlib=False)
   anndata_nc.variables['Plevels'][:] = pcutoffs

   anndata_nc.createVariable('nobs_all',np.int,('Ncycles','Nlevs',),zlib=False)
   anndata_nc.createVariable('nobs_used',np.int,('Ncycles','Nlevs',),zlib=False)
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


