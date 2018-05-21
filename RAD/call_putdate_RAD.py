from putdate_annual_rad import putdate_annual_rad
from create_annual_rad import create_annual_rad
import os

def call_putdate_RAD( diagpath, streamyr,  date, instrmnt, satlite, outputpath, region):
   datayr=str(date)[0:4]

   if region=='GLOBL':
      latrange=[-90, 90]
   elif region=='TROPI':
      latrange=[-20,20]
   elif region=='SOUTH':
      latrange=[-90,-20]
   elif region=='NORTH':
      latrange=[20,90]

   outfile=outputpath+'/RAD_FV3s'+str(streamyr)+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'

   print 'outfile=',outfile
   if os.path.isfile(outfile):
      putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)
   else:
      channelsname=instrmnt+'_channels'
      chanimport='from channel_dictionary import '+channelsname
      exec(chanimport)
      channels=eval(channelsname)
      create_annual_rad(outfile, streamyr, int(datayr), instrmnt, channels, satlite, region)         
      putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)



