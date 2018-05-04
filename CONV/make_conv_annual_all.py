import sys
from create_annual_conv import create_annual_conv

## python make_TEMPLATE.py <stream start year> <data year> <variable> <region>
## e.g. python make_conv_annual_all.py 2003 2004 'U' 'GLOBL'
if len(sys.argv) < 2:
    raise SystemExit('python make_conv_annual_all.py <stream start year> <data year>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
outpath='/lustre/f1/Scott.Gregory/'


pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
regions=['GLOBL','TROPI','NORTH','SOUTH']
variables=['t','u','v','q']

for var in variables:
   for region in regions:
      outfile = outpath+'/FV3s'+str(streamyr)+'/FV3s'+str(streamyr)+'_'+str(datayr)+'_'+var+'_'+region+'.nc'
      create_annual_conv(outfile, streamyr, datayr, var, region, pcutoffs)
     
var = 'ps'
pcutoffs=[0]
for region in regions:
   outfile = outpath+'/FV3s'+str(streamyr)+'/FV3s'+str(streamyr)+'_'+str(datayr)+'_'+var+'_'+region+'.nc'
   create_annual_conv(outfile, streamyr, datayr, var, region, pcutoffs)
