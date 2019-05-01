# script to create all annual files for all streams
from create_annual_rad import create_annual_rad
regions=['GLOBL','TROPI','NORTH','SOUTH']

instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'atms' , 'avhrr'  , 'avhrr', 'avhrr', 'avhrr', 'avhrr', 'cris', 'hirs2' , 'hirs3', 'hirs3', 'hirs4'   , 'hirs4' , 'iasi'   ,    'mhs',     'mhs', 'mhs' , 'mhs', 'msu', 'seviri', 'sndr', 'sndr']
satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n16'  , 'n18'  , 'n19'  , 'n15'  , 'n16'  , 'n17'  , 'npp'  , 'metop-a', 'n15'  , 'n16'  , 'n17'  , 'n18'  , 'npp' , 'n14'   , 'n16'  , 'n17'  , 'metop-a' , 'n19'   , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'n14',  'm10'  , 'g08' , 'g11' ]


numinst=len(instrmnts)
outputpath='/lustre/f2/dev/esrl/Anna.V.Shlyaeva/monitor/fv3_reanl/'
for streamyear in [1999, 2003, 2007, 2011, 2015]:
  for year in range(5):
   for nn in range(numinst):
      instrmnt=instrmnts[nn]
      satlite=satlites[nn]
      channelsname=instrmnt+'_channels'
      chanimport='from channel_dictionary import '+channelsname
      exec(chanimport)
      channels=eval(channelsname)
      print 'channels_name,channels=', channelsname,channels
      for region in regions:
         outfile=outputpath+'/RAD_' + str(streamyear) + '_'+str(streamyear+year)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
         print outfile
         create_annual_rad(outfile, streamyear, streamyear+year, instrmnt, channels, satlite, region)
      del channels



