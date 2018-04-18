import sys
from create_annual_conv import create_annual_conv

## python make_TEMPLATE.py <stream start year> <data year> <variable> <region>
## e.g. python make_conv_annual_all.py 2003 2004 'U' 'GLOBL'
if len(sys.argv) < 2:
    raise SystemExit('python make_conv_annual_all.py <stream start year> <data year>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
outpath='/lustre/f1/Scott.Gregory/FV3s'

pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
regions=['GLOBL','TROPI','NORTH','SOUTH']
variables=['T','U','V','Q']
for var in variables:
  for reg in regions:
    create_annual_conv(outpath, streamyr, datayr, var, reg, pcutoffs)

var = 'PS'
pcutoffs=[0]
for reg in regions:
  create_annual_conv(outpath, streamyr, datayr, var, reg, pcutoffs)
