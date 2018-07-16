from putdate_CFSR_annual_rad import putdate_CFSR_annual_rad
from create_annual_rad import create_annual_rad
import sys
###python make_rad_annual_CFSR.py 1999 1999 /lfs3/projects/gfsenkf/Scott.Gregory/CFSR/
regions=['GLOBL','TROPI','NORTH','SOUTH']


instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'atms' , 'avhrr'  , 'avhrr', 'avhrr', 'avhrr', 'avhrr', 'cris', 'hirs2' , 'hirs3', 'hirs3', 'hirs4'   , 'hirs4' , 'iasi'   ,    'mhs',     'mhs', 'mhs' , 'mhs', 'msu', 'seviri', 'sndr', 'sndr']
satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n16'  , 'n18'  , 'n19'  , 'n15'  , 'n16'  , 'n17'  , 'npp'  , 'metop-a', 'n15'  , 'n16'  , 'n17'  , 'n18'  , 'npp' , 'n14'   , 'n16'  , 'n17'  , 'metop-a' , 'n19'   , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'n14',  'm10'  , 'g08' , 'g11' ]

diagpath = '/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
outputpath = '/lfs3/projects/gfsenkf/ashlyaeva/monitor/CFSR/'
numinst=len(instrmnts)
#for instrmnt in instrmnts:
for nn in range(numinst):
   instrmnt=instrmnts[nn]
   satlite=satlites[nn]

   channelsname=instrmnt+'_channels'
   chanimport='from channel_dictionary import '+channelsname
   exec(chanimport)
   channels=eval(channelsname)

   print 'channels_name,channels=', channelsname,channels
   year = 1999
   for region in regions:
      outfile=outputpath+'/RAD_CFSR_'+str(year)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      create_annual_rad(outfile, year, year, instrmnt, channels, satlite, region)
   for month in range(12):
     for day in range(1):
       for hour in [0, 6, 12, 18]:
         date = year*1000000 + (month+1)*10000 + (day+1)*100 + hour
         print date
         putdate_CFSR_annual_rad(diagpath, date, instrmnt, satlite, outputpath)
   del channels
