import sys
from create_annual_rad import create_annual_rad

if len(sys.argv) < 2:
    raise SystemExit('python make_rad_annual_all.py <stream start year> <data year>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
outpath='/lustre/f1/Scott.Gregory/FV3s'
regions=['GLOBL','TROPI','NORTH','SOUTH']
instrmnt='AMSUA'
satlite='n15'
for reg in regions:
  create_annual_rad(outpath, streamyr, datayr, instrmnt, satlite, reg)


## create_annual_rad(outpath, streamyr, datayr, instrmnt, satlite, region).. 2003 2004 'AMSUA' 'n15' 'GLOBL'
##def create_annual_rad(outpath, streamyr, datayr, instrmnt, satlite, region):







