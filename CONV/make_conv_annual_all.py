import sys
from create_annual_conv import create_annual_conv
from netCDF4 import Dataset

if len(sys.argv) < 3:
    raise SystemExit('python make_conv_annual_all.py <modelstream> <data year> <output path>')
modelstream = sys.argv[1]
datayr = int(sys.argv[2])
outputpath = sys.argv[3]
#outpath='/lustre/f1/Scott.Gregory/'

pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
regions=['GLOBL','TROPI','NORTH','SOUTH']
variables=['t','u','v','q','gps']

for var in variables:
   for region in regions:
      outfile = outputpath+'/CONV_'+var+'_'+modelstream+'_'+str(datayr)+'_'+region+'.nc'
      create_annual_conv(outfile, modelstream , datayr, var, region, pcutoffs)
      print 'outfile=',outfile     
var = 'ps'
pcutoffs=[0]
for region in regions:
   outfile = outputpath+'/CONV_'+var+'_'+modelstream+'_'+str(datayr)+'_'+region+'.nc'
   create_annual_conv(outfile, modelstream, datayr, var, region, pcutoffs)
   print 'outfile=',outfile

