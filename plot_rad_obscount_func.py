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

def plot_rad_obscount_func(modelstreams,datapath,instrmnt,begindate,enddate,IMAGES):
   enddate=str(enddate)
   begindate=str(begindate)

   nummodel=len(modelstreams)

   ##############################
   ##############################
   beginyr=str(begindate)[0:4]
   endyr=str(enddate)[0:4]

   years = range(int(beginyr), int(endyr)+1)

   strdates = dateutils.daterange(begindate,enddate,6)
   dates = np.zeros(len(strdates))
   datetime_list = []
   for i in range(len(dates)):
      dates[i] = int(strdates[i])
      datetime_list.append(datetime.strptime(strdates[i], "%Y%m%d%H"))
   timediff = datetime_list[len(dates)-1] - datetime_list[0]

   satlites = ['aqua', 'metop-a', 'metop-b', 'n15', 'n16', 'n18', 'n19']
   numsat = len(satlites)
   nobs_used = ma.zeros((len(dates), nummodel, numsat));      nobs_used.mask = True

   for modct in range(nummodel):
     for isat in range(numsat):
      for year in years:
        #print('modelstream=',modelstream)
        modelfile=datapath+'/RAD_'+modelstreams[modct]+'_'+str(year)+'_'+instrmnt+'_'+satlites[isat]+'_GLOBL.nc'
        print modelfile
        anndata  = Dataset(modelfile, 'r')
        thisdates = anndata['All_Dates'][:]
        indx_in = np.where(np.in1d(thisdates, dates)) [0]
        indx_out = np.where(np.in1d(dates, thisdates)) [0]
        ################
        nobs_used[indx_out,modct,isat] = anndata['nobs_used'][indx_in,:].sum()
        anndata.close()
   for modct in range(nummodel):
      model=modelstreams[modct]
      ######### PLOTTING
      #############
      font = {'serif' : 'normal','weight' : 'bold','size'   : 12}
      mpl.rc('font', **font)
      mpl.rc('axes',titlesize=18)
      mpl.rc('legend', fontsize=12)
      #############
   
      #############
      axdays = DayLocator()
      axweek = WeekdayLocator(byweekday=SU)
      axsemiweek = WeekdayLocator(byweekday=(SU,WE))
      axmonth =MonthLocator()
      axhours = HourLocator((6,12,18))
      #axhours = HourLocator((0,6,12,18))
      hr6fmt= DateFormatter("%H:00")
      #dayFmt = DateFormatter("%m/%d/%y %H:00")
      #dayFmt = DateFormatter("%b%d.%Y-%Hz")
      #dayFmt = DateFormatter("%b%d.%Y")
      dayFmt = DateFormatter("%m.%d.%y")
      #dayFmt = DateFormatter("%b.%d")
      locator = AutoDateLocator(tz=None, minticks=5, maxticks=15, interval_multiples=False)
      #locator.intervald[HOURLY] = [6] # only show every 6 hours
      if timediff.days<=5:
         ticklocat=axhours
         tick_format= DateFormatter("%m.%d.%y---%H:00")
      elif timediff.days<=15:
         ticklocat=axdays
         tick_format= DateFormatter("%m.%d.%y")
      elif timediff.days<=50:
         ticklocat=axsemiweek
         tick_format= DateFormatter("%m.%d.%y")
      elif timediff.days<=100:
         ticklocat=axweek
         tick_format= DateFormatter("%m.%d.%y")
      elif timediff.days<=365:
         ticklocat=axmonth
         tick_format= DateFormatter("%m.%d.%y")
      else:
         ticklocat=axdays
         tick_format= DateFormatter("%m.%y")
      #############
   
      #############
      figname=IMAGES[modct] 
      #############
      f, ax = plt.subplots()#figsize=(17,5))#plt.subplots(figsize=(20, 10))
      #############
   
      #############
   
      for isat in range(numsat):
        ax.plot(datetime_list, nobs_used[:,modct,isat])
      #####################################
      maxA = nobs_used.max()
      minA = 0
      rangey = maxA-minA
      maxy= maxA + .05*rangey
      miny= minA - .05*rangey
      ax.set_ylabel('number of obs')
      ax.set_ylim((miny,maxy))
      ax.set_xlim((datetime_list[0], datetime_list[len(datetime_list)-1]))
      #####################################
      ax.legend(satlites, loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=numsat)
      ax.grid(True)
      ax.set_title('Number of Observations used', fontsize=14, fontweight='bold')
      #############
   
      ax.xaxis.set_major_locator(locator)
      ax.xaxis.set_major_formatter(tick_format)
   
     # for tick in axarr[5].get_xticklabels():
     #    tick.set_rotation(70)
      os.system("rm "+figname)
      plt.savefig(figname)
      plt.close()
   ##############################




