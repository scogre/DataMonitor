from netCDF4 import Dataset
from putdate_CFSR_annual_rad import putdate_CFSR_annual_rad
from create_annual_rad import create_annual_rad
import sys, os, dateutils
import numpy as np

print('python fillin_year_CFSR.py <year>')
print('This python scripts processes diag files for CFSR for one year')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 1:
    raise SystemExit('python fillin_year_CFSR.py <year>')
year = sys.argv[1]

regions=['GLOBL','TROPI','NORTH','SOUTH']

instrmnts=[ 'airs',  \
            'amsua', 'amsua', 'amsua', 'amsua', 'amsua', 'amsua', 'amsua',   \
            'amsub', 'amsub', 'amsub', \
            'atms',  \
            'avhrr', 'avhrr', 'avhrr', 'avhrr', 'avhrr', \
            'cris', \
            'hirs2', 'hirs2',  \
            'hirs3', 'hirs3', 'hirs3',   \
            'hirs4', 'hirs4',   \
            'iasi', 'iasi',  \
            'mhs', 'mhs', 'mhs', 'mhs',  \
            'msu', 'msu', \
            'seviri', 'seviri', \
            'sndr', 'sndr', 'sndr','sndr', \
            'sndrd1', 'sndrd1','sndrd1','sndrd1','sndrd1',\
            'sndrd2', 'sndrd2','sndrd2','sndrd2','sndrd2',\
            'sndrd3', 'sndrd3','sndrd3','sndrd3','sndrd3',\
            'sndrd4', 'sndrd4','sndrd4','sndrd4','sndrd4',\
            'ssmis', 'ssmis' ]
satlites= [ 'aqua', \
            'aqua', 'metop-a', 'metop-b', 'n15', 'n16', 'n18', 'n19', \
            'n15', 'n16', 'n17',  \
            'npp', \
            'metop-a', 'n15', 'n16', 'n17', 'n18',  \
            'npp', \
            'n11', 'n14',  \
            'n15', 'n16', 'n17',  \
            'metop-a', 'n19', \
            'metop-a', 'metop-b', \
            'metop-a', 'metop-b', 'n18', 'n19',  \
            'n11', 'n14',  \
            'm09', 'm10',  \
            'g08', 'g10', 'g11', 'g12', \
            'g11', 'g12', 'g13', 'g14', 'g15', \
            'g11', 'g12', 'g13', 'g14', 'g15', \
            'g11', 'g12', 'g13', 'g14', 'g15', \
            'g11', 'g12', 'g13', 'g14', 'g15', \
            'f17', 'f18' ]

numinst=len(instrmnts)

diagpath = '/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
outputpath = '/lfs3/projects/gfsenkf/ashlyaeva/monitor/'

for nn in range(numinst):
   instrmnt=instrmnts[nn]
   satlite=satlites[nn]

   channelsname=instrmnt+'_channels'
   chanimport='from channel_dictionary import '+channelsname
   exec(chanimport)
   channels=eval(channelsname)

   # check if annual files are created; create them
   for region in regions:
      outfile=outputpath+'/RAD_CFSR_'+str(year)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      if (not os.path.isfile(outfile)):
        print 'file ', outfile, ' doesnt exist; creating the file.'
        create_annual_rad(outfile, year, year, instrmnt, channels, satlite, region)

   # dates requested by user
   dates = dateutils.daterange(year+'010100',year+'123118',6)

   # check which dates are filled in the global file already
   outfile=outputpath+'/RAD_CFSR_'+str(year)+'_'+instrmnt+'_'+satlite+'_GLOBL.nc'
   anndata = Dataset(outfile, 'r')
   # dates already filled in the file
   fulldates=anndata['Full_Dates'][:]
   anndata.close()
   # set differences between user-specified dates and filled-in dates (so we don't fill in twice)
   dates = np.setdiff1d(dates, fulldates)

   for date in dates:
     putdate_CFSR_annual_rad(diagpath, date, instrmnt, satlite, outputpath)
   del channels

