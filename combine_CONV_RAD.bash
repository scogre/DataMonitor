######################################################################
####### PYTHON CONV
from putdate_annual_conv import putdate_annual_conv

diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/2003stream/'
date=2003010206
var='ps'
latrange=[-90, 90]
outfile='/lustre/f1/Scott.Gregory/FV3s2003/FV3s2003_testest_GLOBL.nc'




putdate_annual_conv(diagpath, dates, var, latrange, outfile)


   variables=['t','u','v','q','gps']




   regions=['GLOBL','TROPI','NORTH','SOUTH']
   for region in regions:
      if region=='GLOBL':
         latrange=[-90, 90]
      elif region=='TROPI':
         latrange=[-20,20]
      elif region=='SOUTH':
         latrange=[-90,-20]
      elif region=='NORTH':
         latrange=[20,90]








if var = 'ps':
   pcutoffs=[0]
else:
   pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]






if os.path.isfile(outfile):
   putdate_annual_conv(diagpath, date, var, diagpref, latrange, outfile)
else:
   pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
   variables=['t','u','v','q','gps']
   for var in variables:
      for reg in regions:
         create_annual_conv(outpath, streamyr, datayr, var, reg, pcutoffs)
         putdate_annual_conv(diagpath, date, var, diagpref, latrange, outfile)
   var = 'ps'
   pcutoffs=[0]
   for reg in regions:
      create_annual_conv(outpath, streamyr, datayr, var, reg, pcutoffs)
      putdate_annual_conv(diagpath, date, var, diagpref, latrange, outfile)








import sys
from create_annual_conv import create_annual_conv

## python make_TEMPLATE.py <stream start year> <data year> <variable> <region>
## e.g. python make_conv_annual_all.py 2003 2004 'U' 'GLOBL'
if len(sys.argv) < 2:
    raise SystemExit('python make_conv_annual_all.py <stream start year> <data year>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
outpath='/lustre/f1/Scott.Gregory/FV3s'

pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
regions=['GLOBL','TROPI','NORTH','SOUTH']
variables=['T','U','V','Q']
for var in variables:
  for reg in regions:
    create_annual_conv(outpath, streamyr, datayr, var, reg, pcutoffs)

var = 'PS'
pcutoffs=[0]
for reg in regions:
  create_annual_conv(outpath, streamyr, datayr, var, reg, pcutoffs)


















######################################################################
######################################################################
####### PYTHON RAD
from putdate_annual_rad import putdate_annual_rad
import os

def call_putdate( streamyr,  date, instrmnt, satlite):
   datayr=str(date)[0:4]
   diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/'+str(streamyr)+'stream/'
   regions=['GLOBL','TROPI','NORTH','SOUTH']
   for region in regions:
      if region=='GLOBL':
         latrange=[-90, 90]
      elif region=='TROPI':
         latrange=[-20,20]
      elif region=='SOUTH':
         latrange=[-90,-20]
      elif region=='NORTH':
         latrange=[20,90]

      outfile='/lustre/f1/Scott.Gregory/FV3s'+str(streamyr)+'/FV3s'+str(streamyr)+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      #print 'outfile=',outfile
      if os.path.isfile(outfile):
         putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)
      else:
         channelsname=instrmnt+'_channels'
         chanimport='from channel_dictionary import '+channelsname
         exec(chanimport)
         channels=eval(channelsname)
         create_annual_rad(outpath, streamyr, datayr, instrmnt, channels, satlite, region)
         putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)





