from netCDF4 import Dataset
from putdate_annual_conv_obscount import putdate_annual_conv_obscount
from create_annual_conv_obscount import create_annual_conv_obscount
import sys, os, dateutils
import numpy as np

print('python fillin_year_reanl_obscount.py <stream> <start date> <end date>')
print('This python scripts processes diag files for reanalysis from start to end date')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 3:
    raise SystemExit('python fillin_year_reanl_obscount.py <stream> <start date> <end date>')
modelstream = sys.argv[1]
date1  = sys.argv[2]
date2  = sys.argv[3]

varnames=['t','uv','q','ps']

diagpath = '/lustre/f2/scratch/Oar.Esrl.Nggps_psd/'+modelstream+'stream/'
outputpath = '/lustre/f2/dev/esrl/Anna.V.Shlyaeva/monitor/'

years = range(int(date1[0:4]), int(date2[0:4])+1)
print years

for var in varnames:
   # dates requested by user
   dates = dateutils.daterange(date1,date2,6)
   for year in years:
      outfile = outputpath+'/CONV_'+modelstream+'_'+str(year)+'_'+var+'_obscounts.nc'
      if (not os.path.isfile(outfile)):
        print('file ' + outfile +' doesnt exist; creating the file.')
        create_annual_conv_obscount(outfile, str(year))
      anndata = Dataset(outfile, 'a')
      fulldates=anndata['Full_Dates'][:]
      indx_in =  np.where(np.in1d(fulldates, dates)) [0]
      fulldates[indx_in].mask = True
      fulldates[indx_in] = -1
      anndata['Full_Dates'][:] = fulldates
      anndata.close()
      dates = np.setdiff1d(dates, fulldates)


