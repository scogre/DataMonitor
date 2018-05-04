from putdate_annual_conv import putdate_annual_conv
from create_annual_conv import create_annual_conv
import os

diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/2003stream/'
date=2003040100
var='ps'
region='GLOBL'
latrange=[-90, 90]
outfile='/lustre/f1/Scott.Gregory/FV3s2003/FV3s2003_2003_ps_GLOBL.nc'
outpath='/lustre/f1/Scott.Gregory/FV3s'
streamyr=2003
datayr=2003

if var == 'ps':
   pcutoffs=[0]
else:
   pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]


if os.path.isfile(outfile):
   putdate_annual_conv(diagpath, date, var, latrange, outfile)
else:
   create_annual_conv(outpath, streamyr, datayr, var, region, pcutoffs)
   putdate_annual_conv(diagpath, date, var, latrange, outfile)



