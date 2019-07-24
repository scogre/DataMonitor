from netCDF4 import Dataset
from putdate_CFSR_annual_conv_obscount import putdate_CFSR_annual_conv_obscount
from create_annual_conv_obscount import create_annual_conv_obscount
import sys, os, dateutils
import numpy as np

print('python fillin_year_CFSR.py <year>')
print('This python scripts processes diag files for CFSR for one year')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 1:
    raise SystemExit('python fillin_year_CFSR.py <year>')
year = sys.argv[1]

varnames=['t','uv','q','ps']

diagpath = '/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
outputpath = '/lfs3/projects/gfsenkf/ashlyaeva/monitor/'

dates = dateutils.daterange(year+'010100',year+'123118',6)

# create files if they don't exist yet
for var in varnames:
   outfile = outputpath+'/CONV_CFSR_'+str(year)+'_'+var+'_obscounts.nc'
   if (not os.path.isfile(outfile)):
       print 'file ', outfile, ' doesnt exist; creating the file.'
       create_annual_conv_obscount(outfile, str(year))

# read the dates already in the file
outfile=outputpath+'/CONV_CFSR_'+str(year)+'_t_obscounts.nc'
anndata = Dataset(outfile, 'r')
# dates already filled in the file
fulldates=anndata['Full_Dates'][:]
anndata.close()
# set differences between user-specified dates and filled-in dates (so we don't fill in twice)
dates = np.setdiff1d(dates, fulldates)
for date in dates:
  print 'processing ', date
  putdate_CFSR_annual_conv_obscount(diagpath, date, outputpath)

