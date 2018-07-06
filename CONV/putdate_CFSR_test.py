from putdate_CFSR_annual_conv import putdate_CFSR_annual_conv
from create_annual_conv import create_annual_conv
import os

diagpath='/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
date=2007041406
var='u'
region='GLOBL'
latrange=[-90, 90]
streamyr=2007
datayr=2007
outfile = diagpath+'/CONV_'+var+'_CFSR_'+str(datayr)+'_'+region+'.nc'
print('outfile=',outfile)

if var == 'ps':
   pcutoffs=[0]
else:
   pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]


if os.path.isfile(outfile):
   putdate_CFSR_annual_conv(diagpath, date, var, latrange, outfile)
else:
   create_annual_conv(outfile, streamyr, datayr, var, region, pcutoffs)
   putdate_CFSR_annual_conv(diagpath, date, var, latrange, outfile)



