from call_putdate_RAD import call_putdate_RAD
import sys

if len(sys.argv) < 3:
   raise SystemExit('python put_all.py <modelstream name> <date> <outputpath> <diagpath>')
modelstream = sys.argv[1]
date = int(sys.argv[2])
outputpath=sys.argv[3]
diagpath=sys.argv[4]
datayr=str(date)[0:4]

if modelstream=='FV3s1999':
   instrmnts=['amsua', 'avhrr', 'hirs2', 'msu', 'sndr']
   satlites=[ 'n15'  , 'n15'  , 'n14'  , 'n14', 'g08' ]
elif modelstream=='FV3s2003':
   instrmnts=['amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'avhrr', 'avhrr', 'hirs2', 'hirs3', 'hirs3', 'msu', 'sndr']
   satlites=[ 'n15'  , 'n16'  , 'n15'  , 'n16'  , 'n17'  , 'n16'  , 'n17'  , 'n14'  , 'n16'  , 'n17'  , 'n14', 'g08']
elif modelstream=='FV3s2007':
   instrmnts=['airs', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'hirs3', 'mhs', 'sndr']
   satlites=[ 'aqua', 'aqua' , 'n15'  , 'n18'  , 'n15'  , 'n16'  , 'n17'  , 'n17'  , 'n18', 'g11']
elif modelstream=='FV3s2011':
   instrmnts=['airs', 'amsua',  'amsua', 'amsua', 'amsua', 'amsua', 'avhrr'    , 'avhrr', 'hirs3', 'hirs4'   ,'hirs4', 'iasi'   , 'mhs'    ,'mhs', 'mhs' ]
   satlites=[ 'aqua', 'aqua' ,'metop-a', 'n15'  , 'n18'  , 'n19'  , 'metop-a'  , 'n18'  , 'n17'  , 'metop-a' , 'n19' , 'metop-a', 'metop-a','n18', 'n19' ]
elif modelstream=='FV3s2015':
   instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'atms' , 'avhrr'    , 'avhrr', 'cris', 'hirs4'   , 'iasi'   ,     'mhs',     'mhs', 'mhs' , 'mhs','seviri' ]
   satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n18'  , 'npp'  , 'metop-a'  , 'n18'  , 'npp' , 'metop-a' , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'm10' ]
else:
   instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'atms' , 'avhrr'  , 'avhrr', 'avhrr', 'avhrr', 'avhrr', 'cris', 'hirs2' , 'hirs3', 'hirs3', 'hirs4'   , 'hirs4' , 'iasi'   ,    'mhs',     'mhs', 'mhs' , 'mhs', 'msu', 'seviri', 'sndr', 'sndr']
   satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n16'  , 'n18'  , 'n19'  , 'n15'  , 'n16'  , 'n17'  , 'npp'  , 'metop-a', 'n15'  , 'n16'  , 'n17'  , 'n18'  , 'npp' , 'n14'   , 'n16'  , 'n17'  , 'metop-a' , 'n19'   , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'n14',  'm10'  , 'g08' , 'g11' ]
#   instrmnts=['hirs2','msu','avhrr','hirs3','amsua','amsub' ,'hirs4','sndr', 'mhs','ssmis','airs','atms','cris','seviri','iasi']
#   satlites= [''     ,''   ,''      ,''     ,''     ,''     ,''     ,''    ,''    ,''     ,''    ,''    ,''    ,''      ,''   ]
numinst=len(instrmnts)


###################
regions=['GLOBL','TROPI','NORTH','SOUTH']
###########

for nn in range(numinst):
   instrmnt=instrmnts[nn]
   satlite=satlites[nn]

   for region in regions:
      try:
         call_putdate_RAD( diagpath, modelstream, date, instrmnt, satlite, outputpath, region)
      except:
         print 'unable to putdate...=',modelstream, date, instrmnt, satlite, region

      info=outputpath+'/RAD_'+modelstream+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc '+str(date)
      print 'info=',info





