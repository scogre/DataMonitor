from putdate_annual_rad import putdate_annual_rad
from putdate_CFSR_annual_rad import putdate_CFSR_annual_rad
from create_annual_rad import create_annual_rad
import os

def call_putdate_RAD( diagpath, modelstream,  date, instrmnt, satlite, outputpath, region):
   datayr=str(date)[0:4]

   if region=='GLOBL':
      latrange=[-90, 90]
   elif region=='TROPI':
      latrange=[-20,20]
   elif region=='SOUTH':
      latrange=[-90,-20]
   elif region=='NORTH':
      latrange=[20,90]

   outfile=outputpath+'/RAD_'+modelstream+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'

   print 'outfile=',outfile
   if os.path.isfile(outfile):
      if modelstream=='CFSR':
         putdate_CFSR_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)
      else:
         putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)
   else:
      channelsname=instrmnt+'_channels'
      chanimport='from channel_dictionary import '+channelsname
      exec(chanimport)
      channels=eval(channelsname)
      create_annual_rad(outfile, modelstream, int(datayr), instrmnt, channels, satlite, region)         
      if modelstream=='CFSR':
         putdate_CFSR_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)
      else:
         putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)



