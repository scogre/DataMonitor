from putdate_annual_conv import putdate_annual_conv
from putdate_CFSR_annual_conv import putdate_CFSR_annual_conv
from create_annual_conv import create_annual_conv
import os
import sys


if len(sys.argv) < 2:
   raise SystemExit('python call_putdate_CONV.py <modelstream> <date> <annual output path> <diagpath>')
modelstream = sys.argv[1]
date = int(sys.argv[2])
outputpath = sys.argv[3]
diagpath = sys.argv[4]
datayr=str(date)[0:4]

datayr=str(date)[0:4]
regions=['GLOBL','TROPI','NORTH','SOUTH']

variables=['t','u','v','q','ps','gps']

for var in variables:

   for region in regions:
      if region=='GLOBL':
         latrange=[-90, 90]
      elif region=='TROPI':
         latrange=[-20,20]
      elif region=='SOUTH':
         latrange=[-90,-20]
      elif region=='NORTH':
         latrange=[20,90]

      if var == 'ps':
         pcutoffs=[0]
      else:
         pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
   
      outfile = outputpath+'/CONV_'+var+'_'+modelstream+'_'+str(datayr)+'_'+region+'.nc'

      if os.path.isfile(outfile):
         if modelstream=='CFSR':
            putdate_CFSR_annual_conv(diagpath, date, var, latrange, outfile)
         else:
            putdate_annual_conv(diagpath, date, var, latrange, outfile)
      else:
         create_annual_conv(outfile, modelstream, int(datayr), var, region, pcutoffs)
         if modelstream=='CFSR':
            putdate_CFSR_annual_conv(diagpath, date, var, latrange, outfile)
         else:         
            putdate_annual_conv(diagpath, date, var, latrange, outfile)
 


