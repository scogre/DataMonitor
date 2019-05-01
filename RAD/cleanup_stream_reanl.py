from netCDF4 import Dataset
from putdate_annual_rad import putdate_annual_rad
from create_annual_rad import create_annual_rad
import sys, os, dateutils
import numpy as np

print('python fillin_stream_reanl.py <stream> <start date> <end date>')
print('This python scripts processes diag files for reanalysis from start to end date')
print('NOTE: The paths to diags and to output are hardcoded in the script.')

if len(sys.argv) < 3:
    raise SystemExit('python fillin_stream_reanl.py <stream> <start date> <end date>')
modelstream = sys.argv[1]
date1  = sys.argv[2]
date2  = sys.argv[3]

regions=['GLOBL','TROPI','NORTH','SOUTH']

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
            'sndr', 'sndr', 'sndr','sndr', \
            'sndrd1', 'sndrd1','sndrd1','sndrd1','sndrd1',\
            'sndrd2', 'sndrd2','sndrd2','sndrd2','sndrd2',\
            'sndrd3', 'sndrd3','sndrd3','sndrd3','sndrd3',\
            'sndrd4', 'sndrd4','sndrd4','sndrd4','sndrd4',\
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
            'g08', 'g10', 'g11', 'g12', \
            'g11', 'g12', 'g13', 'g14', 'g15', \
            'g11', 'g12', 'g13', 'g14', 'g15', \
            'g11', 'g12', 'g13', 'g14', 'g15', \
            'g11', 'g12', 'g13', 'g14', 'g15', \
            'f17', 'f18' ]

diagpath = '/lustre/f2/scratch/Oar.Esrl.Nggps_psd/'+modelstream+'stream/'
outputpath = '/lustre/f2/dev/esrl/Anna.V.Shlyaeva/monitor/'
numinst=len(instrmnts)

years = range(int(date1[0:4]), int(date2[0:4])+1)

for nn in range(numinst):
   instrmnt=instrmnts[nn]
   satlite=satlites[nn]

   channelsname=instrmnt+'_channels'
   chanimport='from channel_dictionary import '+channelsname
   exec(chanimport)
   channels=eval(channelsname)

   # check if annual files are created; create them 
   for region in regions:
      for year in years:
        outfile = outputpath+'/RAD_'+modelstream+'_'+str(year)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
        if (not os.path.isfile(outfile)):
          print 'file ', outfile, ' doesnt exist; creating the file.'
          create_annual_rad(outfile, modelstream, str(year), instrmnt, channels, satlite, region)

   # dates requested by user
   dates = dateutils.daterange(date1,date2,6)
   # check which dates are filled in the global file already
   for year in years:
     outfile=outputpath+'/RAD_'+modelstream+'_'+str(year)+'_'+instrmnt+'_'+satlite+'_GLOBL.nc'
     anndata = Dataset(outfile, 'a')
     # dates already filled in the file
     fulldates=anndata['Full_Dates'][:]

     indx_in =  np.where(np.in1d(fulldates, dates)) [0]
     fulldates[indx_in].mask = True
     fulldates[indx_in] = -1
     anndata['Full_Dates'][:] = fulldates

#     print anndata['Full_Dates'][indx_in] 

     anndata.close()
   del channels

