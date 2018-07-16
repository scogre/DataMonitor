from putdate_annual_rad import putdate_annual_rad
from create_annual_rad import create_annual_rad
import sys
import os

print('python call_putdate_rad.py <modelstream> <date>')
print('This python scripts processes diag files for modelstream ')
print(' for date <date>. ')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 2:
    raise SystemExit('python call_putdate_rad.py <modelstream name> <data year>')
modelstream = sys.argv[1]
date = int(sys.argv[2])

datayr=str(date)[0:4]

regions=['GLOBL','TROPI','NORTH','SOUTH']


instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'atms' , 'avhrr'  , 'avhrr', 'avhrr', 'avhrr', 'avhrr', 'cris', 'hirs2' , 'hirs3', 'hirs3', 'hirs4'   , 'hirs4' , 'iasi'   ,    'mhs',     'mhs', 'mhs' , 'mhs', 'msu', 'seviri', 'sndr', 'sndr']
satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n16'  , 'n18'  , 'n19'  , 'n15'  , 'n16'  , 'n17'  , 'npp'  , 'metop-a', 'n15'  , 'n16'  , 'n17'  , 'n18'  , 'npp' , 'n14'   , 'n16'  , 'n17'  , 'metop-a' , 'n19'   , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'n14',  'm10'  , 'g08' , 'g11' ]


diagpath = '/lustre/f1/Oar.Esrl.Nggps_psd/'+modelstream+'stream/'
outputpath = '/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/fv3_reanl/'
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
   for region in regions:
      outfile=outputpath+'/RAD_'+modelstream+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      if (not os.path.isfile(outfile)):
        print('file ', outfile, ' doesnt exist; creating the file.')
        create_annual_rad(outfile, modelstream, int(datayr), instrmnt, channels, satlite, region)
   print('filling in reanalysis data')
   putdate_annual_rad(diagpath, date, modelstream, instrmnt, satlite, outputpath)
