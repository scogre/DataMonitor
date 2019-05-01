from netCDF4 import Dataset
from putdate_annual_conv import putdate_annual_conv
from create_annual_conv import create_annual_conv
import sys, os, dateutils
import numpy as np

print('python fillin_year_reanl.py <stream> <start date> <end date>')
print('This python scripts processes diag files for reanalysis from start to end date')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 3:
    raise SystemExit('python fillin_year_reanl.py <stream> <start date> <end date>')
modelstream = sys.argv[1]
date1  = sys.argv[2]
date2  = sys.argv[3]

regions=['GLOBL','TROPI','NORTH','SOUTH']
varnames=['t','u','v','q','ps']

diagpath = '/lustre/f2/scratch/Oar.Esrl.Nggps_psd/'+modelstream+'stream/'
outputpath = '/lustre/f2/dev/esrl/Anna.V.Shlyaeva/monitor/'

years = range(int(date1[0:4]), int(date2[0:4])+1)

for var in varnames:
   for region in regions:
      # check if annual files are created; create them 
      if var == 'ps':
         pcutoffs=[0]
      else:
         pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
      for year in years:
        outfile = outputpath+'/CONV_'+modelstream+'_'+str(year)+'_'+var+'_'+region+'.nc'
        if (not os.path.isfile(outfile)):
          print('file ' + outfile +' doesnt exist; creating the file.')
          create_annual_conv(outfile, modelstream, str(year), var, region, pcutoffs)

   # dates requested by user
   dates = dateutils.daterange(date1,date2,6)

   # check which dates are filled in the global file already
   for year in years:
     outfile=outputpath+'/CONV_'+modelstream+'_'+str(year)+'_'+var+'_GLOBL.nc'
     anndata = Dataset(outfile, 'a')
     # dates already filled in the file
     fulldates=anndata['Full_Dates'][:]

     indx_in =  np.where(np.in1d(fulldates, dates)) [0]
     fulldates[indx_in].mask = True
     fulldates[indx_in] = -1
     anndata['Full_Dates'][:] = fulldates

     anndata.close()

