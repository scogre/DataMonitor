import sys
from create_annual_conv import create_annual_conv

## python make_TEMPLATE.py <stream start year> <data year> <variable> <region>
## e.g. python make_conv_annual_one.py  2003 2004 'U' 'GLOBL'
if len(sys.argv) < 5:
    raise SystemExit('python make_conv_annual_one.py <stream start year> <data year> <variable> <region>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
varb = sys.argv[3]
region = sys.argv[4]
pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
outpath='/lustre/f1/Scott.Gregory/'

outfile = outpath+'/FV3s'+str(streamyr)+'/FV3s'+str(streamyr)+'_'+str(datayr)+'_'+varb+'_'+region+'.nc'



create_annual_conv(outfile, streamyr, datayr, varb, region, pcutoffs)

