from netCDF4 import Dataset
from putdate_CFSR_annual_conv import putdate_CFSR_annual_conv
from create_annual_conv import create_annual_conv
import sys, os, dateutils
import numpy as np

print('python fillin_year_CFSR.py <year>')
print('This python scripts processes diag files for CFSR for one year')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 1:
    raise SystemExit('python fillin_year_CFSR.py <year>')
year = sys.argv[1]

regions=['GLOBL','TROPI','NORTH','SOUTH']
varnames=['t','u','v','q','ps','gps']

diagpath = '/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
outputpath = '/lfs3/projects/gfsenkf/ashlyaeva/monitor/'

dates = dateutils.daterange(year+'010100',year+'123118',6)

# create files if they don't exist yet
for var in varnames:
   if var == 'ps':
      pcutoffs=[0]
   else:
      pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
   for region in regions:
      outfile = outputpath+'/CONV_CFSR_'+str(year)+'_'+var+'_'+region+'.nc'
      if (not os.path.isfile(outfile)):
         print 'file ', outfile, ' doesnt exist; creating the file.'
         create_annual_conv(outfile, year, year, var, region, pcutoffs)

# read the dates already in the file
outfile=outputpath+'/CONV_CFSR_'+str(year)+'_t_GLOBL.nc'
anndata = Dataset(outfile, 'r')
# dates already filled in the file
fulldates=anndata['Full_Dates'][:]
anndata.close()
# set differences between user-specified dates and filled-in dates (so we don't fill in twice)
dates = np.setdiff1d(dates, fulldates)
for date in dates:
  print 'processing ', date
  putdate_CFSR_annual_conv(diagpath, date, outputpath)

