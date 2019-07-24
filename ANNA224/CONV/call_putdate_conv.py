from putdate_annual_conv import putdate_annual_conv
from create_annual_conv import create_annual_conv
import os
import sys

print('python call_putdate_conv.py <modelstream> <date>')
print('This python scripts processes diag files for modelstream ')
print(' for date <date>. ')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 2:
    raise SystemExit('python call_putdate_conv.py <modelstream name> <data year>')
modelstream = sys.argv[1]
date = int(sys.argv[2])

datayr=str(date)[0:4]

regions=['GLOBL','TROPI','NORTH','SOUTH']
varnames=['t','u','v','q','ps','gps']

diagpath = '/lustre/f2/scratch/Oar.Esrl.Nggps_psd/'+modelstream+'stream/'
outputpath = '/lustre/f2/dev/Anna.V.Shlyaeva/monitor/'
for var in varnames:
   for region in regions:
      if var == 'ps':
         pcutoffs=[0]
      else:
         pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
      outfile = outputpath+'/CONV_'+modelstream+'_'+str(datayr)+'_'+var+'_'+region+'.nc'
      if (not os.path.isfile(outfile)):
         print('file ' + outfile +' doesnt exist; creating the file.')
         create_annual_conv(outfile, modelstream, int(datayr), var, region, pcutoffs)

   print('filling in reanalysis data')
   putdate_annual_conv(diagpath, date, modelstream, var, outputpath)

