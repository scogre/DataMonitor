from putdate_CFSR_annual_conv import putdate_CFSR_annual_conv
from create_annual_conv import create_annual_conv
import sys, os

print('python fillin_year_CFSR.py <year>')
print('This python scripts processes diag files for CFSR for one year')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 1:
    raise SystemExit('python fillin_year_CFSR.py <year>')
year = int(sys.argv[1])

regions=['GLOBL','TROPI','NORTH','SOUTH']
varnames=['t','u','v','q','ps','gps']

dayinmon=[31,29,31,30,31,30,31,31,30,31,30,31]

diagpath = '/lfs3/projects/gfsenkf/Scott.Gregory/CFSR/'
outputpath = '/lfs3/projects/gfsenkf/ashlyaeva/monitor/'

for var in varnames:
   if var == 'ps':
      pcutoffs=[0]
   else:
      pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
   for region in regions:
      outfile = outputpath+'/CONV_CFSR_'+str(year)+'_'+var+'_'+region+'.nc'
      if (not os.path.isfile(outfile)):
         print('file ', outfile, ' doesnt exist; creating the file.')
         create_annual_conv(outfile, year, year, var, region, pcutoffs)

for month in range(12):
  for day in range(dayinmon[month]):
     for hour in [0, 6, 12, 18]:
        date = year*1000000 + (month+1)*10000 + (day+1)*100 + hour
        print date
        putdate_CFSR_annual_conv(diagpath, date, outputpath)

