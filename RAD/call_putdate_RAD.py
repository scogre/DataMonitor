from putdate_annual_rad import putdate_annual_rad
import os

def call_putdate_RAD( streamyr,  date, instrmnt, satlite, outpath, region):
   datayr=str(date)[0:4]
   diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/'+str(streamyr)+'stream/'
   if region=='GLOBL':
      latrange=[-90, 90]
   elif region=='TROPI':
      latrange=[-20,20]
   elif region=='SOUTH':
      latrange=[-90,-20]
   elif region=='NORTH':
      latrange=[20,90]

   outfile=outpath+'FV3s'+str(streamyr)+'/RAD_FV3s'+str(streamyr)+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'

   #print 'outfile=',outfile
   if os.path.isfile(outfile):
      putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)
   else:
      channelsname=instrmnt+'_channels'
      chanimport='from channel_dictionary import '+channelsname
      exec(chanimport)
      channels=eval(channelsname)
      create_annual_rad(outfile, streamyr, datayr, instrmnt, channels, satlite, region)         
      putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)



