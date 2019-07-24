from call_putdate_RAD import call_putdate_RAD
import sys

if len(sys.argv) < 3:
   raise SystemExit('python put_all.py <modelstream name> <date> <outputpath> <diagpath>')
modelstream = sys.argv[1]
date = int(sys.argv[2])
outputpath=sys.argv[3]
diagpath=sys.argv[4]
datayr=str(date)[0:4]

instrmnts=[ 'airs',  \
            'amsua', 'amsua', 'amsua', 'amsua', 'amsua', 'amsua', 'amsua',   \
            'amsub', 'amsub', 'amsub', \
            'atms',  \
            'avhrr', 'avhrr', 'avhrr', 'avhrr', 'avhrr', \
            'cris', \
            'hirs2', 'hirs2',  \
            'hirs3', 'hirs3', 'hirs3',   \
            'hirs4', 'hirs4',   \
            'iasi', 'iasi',  \
            'mhs', 'mhs', 'mhs', 'mhs',  \
            'msu', 'msu', \
            'seviri', 'seviri', \
            'sndr', 'sndr', 'sndr','sndr','sndr','sndr','sndr', \
            'ssmis', 'ssmis' ]
satlites= [ 'aqua', \
            'aqua', 'metop-a', 'metop-b', 'n15', 'n16', 'n18', 'n19', \
            'n15', 'n16', 'n17',  \
            'npp', \
            'metop-a', 'n15', 'n16', 'n17', 'n18',  \
            'npp', \
            'n11', 'n14',  \
            'n15', 'n16', 'n17',  \
            'metop-a', 'n19', \
            'metop-a', 'metop-b', \
            'metop-a', 'metop-b', 'n18', 'n19',  \
            'n11', 'n14',  \
            'm09', 'm10',  \
            'g08', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15', \
            'f17', 'f18' ]


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





