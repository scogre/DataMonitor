from call_putdate_RAD import call_putdate_RAD
import sys

if len(sys.argv) < 3:
   raise SystemExit('python put_all.py <modelstream name> <date> <outputpath> <diagpath>')
modelstream = sys.argv[1]
date = int(sys.argv[2])
outputpath=sys.argv[3]
diagpath=sys.argv[4]
datayr=str(date)[0:4]

instrmnts=[ 'cris', \
            'hirs2', 'hirs2',  \
            'hirs3', 'hirs3' ]
satlites= [ 'npp', \
            'n11', 'n14',  \
            'n15', 'n16' ]


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





