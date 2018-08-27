#!/usr/local/bin/python2.7
import numpy as np
import numpy.ma as ma
import dateutils
from netCDF4 import Dataset
from datetime import datetime, date, time
from datetime import timedelta
import matplotlib as mpl
mpl.use('Agg') #for web 
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter, DayLocator, HourLocator, AutoDateLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import os

def plot_conv_obscount_func(modelstreams,datapath,varb,begindate,enddate,IMAGES):
   nummodel=len(modelstreams)
   enddate=str(enddate)
   begindate=str(begindate)

   ##############################
   beginyr=str(begindate)[0:4]
   endyr=str(enddate)[0:4]

   years = range(int(beginyr), int(endyr)+1)

   print years 
   strdates = dateutils.daterange(begindate,enddate,12)
   dates = np.zeros(len(strdates))
   datetime_list = []
   for i in range(len(dates)):
      dates[i] = int(strdates[i])
      datetime_list.append(datetime.strptime(strdates[i], "%Y%m%d%H"))
   print len(datetime_list)
   timediff = datetime_list[len(dates)-1] - datetime_list[0]

   ##################################
   ##################################
   nobs_used = ma.zeros((len(dates), nummodel));      nobs_used.mask = True
   nobs_acft = ma.zeros((len(dates), nummodel));      nobs_acft.mask = True
   nobs_sfc  = ma.zeros((len(dates), nummodel));      nobs_sfc.mask  = True
   nobs_sond = ma.zeros((len(dates), nummodel));      nobs_sond.mask = True
   nobs_prof = ma.zeros((len(dates), nummodel));      nobs_prof.mask = True
   nobs_satw = ma.zeros((len(dates), nummodel));      nobs_satw.mask = True
   nobs_scatw = ma.zeros((len(dates), nummodel));     nobs_scatw.mask = True
   nobs_wind = ma.zeros((len(dates), nummodel));      nobs_wind.mask = True
   nobs_other = ma.zeros((len(dates), nummodel));     nobs_other.mask = True
   print len(dates)
   ##################################
   
   for modct in range(nummodel):
      for year in years:
        #print('modelstream=',modelstream)
        modelfile=datapath+'CONV_'+modelstreams[modct]+'_'+str(year)+'_'+varb+'_obscounts.nc'
        print modelfile
        anndata  = Dataset(modelfile, 'r')
        thisdates = anndata['All_Dates'][:]
        indx_in = np.where(np.in1d(thisdates, dates)) [0]
        indx_out = np.where(np.in1d(dates, thisdates)) [0]
        ################
        nobs_used[indx_out,modct] = anndata['nobs_used'][indx_in]
        nobs_acft[indx_out,modct] = anndata['nobs_acft'][indx_in]
        nobs_sfc[indx_out,modct]  = anndata['nobs_sfc'][indx_in]
        nobs_sond[indx_out,modct] = anndata['nobs_sond'][indx_in]
        nobs_prof[indx_out,modct] = anndata['nobs_prof'][indx_in]
        nobs_satw[indx_out,modct] = anndata['nobs_satw'][indx_in]
        nobs_scatw[indx_out,modct] = anndata['nobs_scatw'][indx_in]
        nobs_other[indx_out,modct] = anndata['nobs_other'][indx_in]
        nobs_wind[indx_out,modct] = anndata['nobs_prof'][indx_in] + anndata['nobs_satw'][indx_in] + anndata['nobs_scatw'][indx_in]
        anndata.close()

   ####################################################
   for modct in range(nummodel):
      model=modelstreams[modct]
      ######### PLOTTING
      modelname = model
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
   
   
      figname=IMAGES[modct]       
      fig, ax = plt.subplots(figsize=(10,5))
      ax.plot( datetime_list, nobs_used[:,modct],'k', \
                     datetime_list, nobs_sond[:,modct],'b', \
                     datetime_list, nobs_acft[:,modct],'g', \
                     datetime_list, nobs_sfc[:,modct],'r',  \
                     datetime_list, nobs_wind[:,modct], 'orange', \
                     datetime_list, nobs_other[:,modct], 'grey')
      ax.set_ylabel('number of obs')
      minval = 0
      maxval = nobs_used.max()
      rangey=maxval-minval
      minax = minval - .05*rangey
      maxax = maxval + .05*rangey
      ax.set_ylim((minax,maxax))
      #plt.legend(('all used obs', 'sondes', 'aircrafts', 'surface', 'satwinds + scatt.winds + wind profilers', 'other'),loc='center left')
      ax.legend(('all used obs', 'sondes', 'aircrafts', 'surface', 'sat/scatwinds + profilers'), loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
      ax.grid(True)
      ax.set_title('Number of conventional observations used', fontsize=14, fontweight='bold')

      ax.xaxis.set_major_locator(locator)
      ax.xaxis.set_major_formatter(tick_format)
      #for tick in ax.get_xticklabels():
      #    tick.set_rotation(70)
   
      plt.savefig(figname)
      plt.close()
   #########################
   #########################
   #########################
   #########################





