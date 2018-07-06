from call_putdate_CFSR_RAD import call_putdate_CFSR_RAD
from netCDF4 import Dataset
import sys

if len(sys.argv) < 3:
   raise SystemExit('python put_CFSR.py <stream start year> <date> <outputpath> <diagpath>')
streamyr = int(sys.argv[1])
date = int(sys.argv[2])
outputpath=sys.argv[3]
diagpath=sys.argv[4]
datayr=str(date)[0:4]
#print 'streamyr,date=',streamyr,date 



instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'atms' , 'avhrr'  , 'avhrr', 'avhrr', 'avhrr', 'avhrr', 'cris', 'hirs2' , 'hirs3', 'hirs3', 'hirs4'   , 'hirs4' , 'iasi'   ,    'mhs',     'mhs', 'mhs' , 'mhs', 'msu', 'seviri', 'sndr', 'sndr']
satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n16'  , 'n18'  , 'n19'  , 'n15'  , 'n16'  , 'n17'  , 'npp'  , 'metop-a', 'n15'  , 'n16'  , 'n17'  , 'n18'  , 'npp' , 'n14'   , 'n16'  , 'n17'  , 'metop-a' , 'n19'   , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'n14',  'm10'  , 'g08' , 'g11' ]

#instrmnts=['amsua']
#satlites=['n15']

numinst=len(instrmnts)



###################
regions=['GLOBL','TROPI','NORTH','SOUTH']
###########

for nn in range(numinst):
   instrmnt=instrmnts[nn]
   satlite=satlites[nn]

   for region in regions:
      call_putdate_CFSR_RAD( diagpath, streamyr, date, instrmnt, satlite, outputpath, region)
      #try:
      #   call_putdate_CFSR_RAD( diagpath, streamyr, date, instrmnt, satlite, outputpath, region)
      #except:
      #   print 'unable to putdate...=',streamyr, date, instrmnt, satlite, region
      info=outputpath+'RAD_CFSR_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc '+str(date)
      print 'info=',info





