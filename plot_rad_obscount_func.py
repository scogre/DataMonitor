#!/usr/local/bin/python2.7
import numpy as np
import numpy.ma as ma
import dateutils
from netCDF4 import Dataset
from datetime import datetime, date, time, timedelta
from datetime import timedelta
import matplotlib as mpl
mpl.use('Agg') #for web 
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter, DayLocator, HourLocator, AutoDateLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import os
from time import gmtime, strftime


def plot_rad_obscount_func(stream,datapath,begindate,enddate,imagepath):
   modelstreams = [str(stream), 'CFSR']
   modelstreamnames = [str(stream)+" stream", "CFSR"]

   enddate=str(enddate)
   begindate=str(begindate)

   nummodel=len(modelstreams)

   ##############################
   ##############################
   beginyr=str(begindate)[0:4]
   endyr=str(enddate)[0:4]

   years = range(int(beginyr), int(endyr)+1)

   strdates = dateutils.daterange(begindate,enddate,24)
   dates = np.zeros(len(strdates))
   datetime_list = []
   for i in range(len(dates)):
      dates[i] = int(strdates[i])
      datetime_list.append(datetime.strptime(strdates[i], "%Y%m%d%H"))

   instrmnts = [ ('amsua','msu'), ('amsub', 'mhs'), ('hirs2', 'hirs3', 'hirs4'), ('iasi',), ('airs',), ('atms',), ('cris',), \
                 ('avhrr',), ('seviri',), ('sndr',), ('ssmis',)]
   numinstr = len(instrmnts)

   instnames = [""] * numinstr
   for i in range(numinstr):
     instnames[i] = instrmnts[i][0]
     for j in range(1, len(instrmnts[i])):
       instnames[i] = instnames[i] + ', ' + instrmnts[i][j]
 
   satlites = [ ['n15', 'n16', 'n18', 'n19', 'aqua', 'metop-a', 'metop-b', 'n11', 'n14'], \
                ['n15', 'n16', 'n17', 'n18', 'n19','metop-a', 'metop-b'],  \
                ['n11', 'n14', 'n15', 'n16', 'n17', 'metop-a', 'n19'], \
                ['metop-a', 'metop-b'], \
                ['aqua'], \
                ['npp'], \
                ['npp'], \
                ['n15', 'n16', 'n17', 'n18','metop-a'], \
                ['m09', 'm10'], \
                ['g08', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15'], \
                ['f17', 'f18'] ]

   maxnumsat = max(len(sat) for sat in satlites)

   nobs_used = ma.zeros((len(dates), nummodel, numinstr, maxnumsat));      nobs_used.mask = True

   for modct in range(nummodel):
     for iinstr in range(numinstr):
       for instropt in range(len(instrmnts[iinstr])):
         for isat in range(len(satlites[iinstr])):
           for year in years:
             #print('modelstream=',modelstream)
             modelfile=datapath+'/RAD_'+modelstreams[modct]+'_'+str(year)+'_'+instrmnts[iinstr][instropt]+'_'+satlites[iinstr][isat]+'_GLOBL.nc'
             print modelfile
             if (os.path.isfile(modelfile)):
               anndata  = Dataset(modelfile, 'r')
               thisdates = anndata['All_Dates'][:]
               indx_in = np.where(np.in1d(thisdates, dates)) [0]
               indx_out = np.where(np.in1d(dates, thisdates)) [0]
               ################
               nobs_used[indx_out,modct,iinstr,isat] = anndata['nobs_used'][indx_in,:].sum(axis=1)
               anndata.close()

   font = {'serif' : 'normal','weight' : 'bold','size'   : 12}
   mpl.rc('font', **font)
   mpl.rc('axes',titlesize=18)
   mpl.rc('legend', fontsize=12)
#   locator = AutoDateLocator(tz=None, minticks=5, maxticks=15, interval_multiples=False)
#   tick_format= DateFormatter("%m.%y")

   #############
   fig, ax = plt.subplots(numinstr, nummodel, figsize = (10*nummodel, 4*numinstr), sharey='row')
   for modct in range(nummodel):
      for iinstr in range(numinstr):
         for isat in range(len(satlites[iinstr])):
            ax[iinstr,modct].plot(datetime_list, nobs_used[:,modct,iinstr,isat])
         maxA = nobs_used[:,:,iinstr,:].max()
         minA = 0
         rangey = maxA-minA
         maxy= maxA + .05*rangey
         miny= minA - .05*rangey
         if modct == 0:
           ax[iinstr,modct].set_ylabel('number of obs')
         ax[iinstr,modct].set_ylim((miny,maxy))
         ax[iinstr,modct].set_xlim((datetime_list[0], datetime_list[len(datetime_list)-1]))
         if modct == 1:
           ax[iinstr,modct].legend(satlites[iinstr], loc='center left', bbox_to_anchor=(1.02, 0.5))
         ax[iinstr,modct].grid(True)
         ax[iinstr,modct].set_title('Number of '+instnames[iinstr]+' observations used in '+modelstreamnames[modct], fontsize=14, fontweight='bold')
   
#         ax[iinstr,modct].xaxis.set_major_locator(locator)
#         ax[iinstr,modct].xaxis.set_major_formatter(tick_format)
   
   fig.tight_layout(rect=[0, 0.05, 0.9, 0.98],h_pad=2)
   plt.text(0.05, 0.02, "Generated "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"UTC", fontsize=12, color='grey',transform=fig.transFigure)
   plt.savefig(imagepath+"/"+stream+"_rad_obscounts.png")
   plt.close()
   ##############################




