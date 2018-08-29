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
from time import gmtime, strftime

def plot_conv_obscount_func(stream,datapath,begindate,enddate,imagepath):
   modelstreams = [str(stream), 'CFSR']
   modelstreamnames = [str(stream)+" stream", "CFSR"]
   nummodel = len(modelstreams)
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

   varnames = ['t', 'uv', 'ps']
   numvars = len(varnames)

   ##################################
   ##################################
   nobs_used = ma.zeros((len(dates), numvars, nummodel));      nobs_used.mask = True
   nobs_acft = ma.zeros((len(dates), numvars, nummodel));      nobs_acft.mask = True
   nobs_sfc  = ma.zeros((len(dates), numvars, nummodel));      nobs_sfc.mask  = True
   nobs_sond = ma.zeros((len(dates), numvars, nummodel));      nobs_sond.mask = True
   nobs_prof = ma.zeros((len(dates), numvars, nummodel));      nobs_prof.mask = True
   nobs_satw = ma.zeros((len(dates), numvars, nummodel));      nobs_satw.mask = True
   nobs_scatw = ma.zeros((len(dates), numvars, nummodel));     nobs_scatw.mask = True
   nobs_wind = ma.zeros((len(dates), numvars, nummodel));      nobs_wind.mask = True
   nobs_other = ma.zeros((len(dates), numvars, nummodel));     nobs_other.mask = True
   print len(dates)
   ##################################
   
   for modct in range(nummodel):
      for year in years:
        for ivar in range(numvars):
          #print('modelstream=',modelstream)
          modelfile=datapath+'CONV_'+modelstreams[modct]+'_'+str(year)+'_'+varnames[ivar]+'_obscounts.nc'
          print modelfile
          anndata  = Dataset(modelfile, 'r')
          thisdates = anndata['All_Dates'][:]
          indx_in = np.where(np.in1d(thisdates, dates)) [0]
          indx_out = np.where(np.in1d(dates, thisdates)) [0]
          ################
          nobs_used[indx_out,ivar,modct] = anndata['nobs_used'][indx_in]
          nobs_acft[indx_out,ivar,modct] = anndata['nobs_acft'][indx_in]
          nobs_sfc[indx_out,ivar,modct]  = anndata['nobs_sfc'][indx_in]
          nobs_sond[indx_out,ivar,modct] = anndata['nobs_sond'][indx_in]
          nobs_prof[indx_out,ivar,modct] = anndata['nobs_prof'][indx_in]
          nobs_satw[indx_out,ivar,modct] = anndata['nobs_satw'][indx_in]
          nobs_scatw[indx_out,ivar,modct] = anndata['nobs_scatw'][indx_in]
          nobs_other[indx_out,ivar,modct] = anndata['nobs_other'][indx_in]
          nobs_wind[indx_out,ivar,modct] = anndata['nobs_prof'][indx_in] + anndata['nobs_satw'][indx_in] + anndata['nobs_scatw'][indx_in]
          anndata.close()

   ####################################################
   model=modelstreams[modct]
   #############
   font = {'serif' : 'normal','weight' : 'bold','size'   : 12}
   mpl.rc('font', **font)
   mpl.rc('axes',titlesize=18)
   mpl.rc('legend', fontsize=12)
   #############
   axdays = DayLocator()
   axweek = WeekdayLocator(byweekday=SU)
   axsemiweek = WeekdayLocator(byweekday=(SU,WE))
   axmonth =MonthLocator()
   axhours = HourLocator((6,12,18))
   hr6fmt= DateFormatter("%H:00")
   dayFmt = DateFormatter("%m.%d.%y")
   locator = AutoDateLocator(tz=None, minticks=5, maxticks=15, interval_multiples=False)
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
   fig, ax = plt.subplots(numvars, nummodel, figsize=(10*nummodel,6*numvars),sharey='row')

   for modct in range(nummodel):
      for ivar in range(numvars):
        if varnames[ivar] == "uv":
          ax[ivar,modct].plot( datetime_list, nobs_used[:,ivar,modct],'k', \
                       datetime_list, nobs_sond[:,ivar,modct],'b', \
                       datetime_list, nobs_acft[:,ivar,modct],'g', \
                       datetime_list, nobs_sfc[:,ivar,modct],'r',  \
                       datetime_list, nobs_satw[:,ivar,modct],'orange', \
                       datetime_list, nobs_scatw[:,ivar,modct], 'purple', \
                       datetime_list, nobs_prof[:,ivar,modct], 'cyan', \
                       datetime_list, nobs_other[:,ivar,modct], 'grey')
          if (modct == 1): 
             ax[ivar,modct].legend(('all used obs', 'sondes', 'aircrafts', 'surface', 'sat. winds', 'scat. winds', 'wind prof'),
                 loc='center left', bbox_to_anchor=(1.02, 0.5)) 
        else:
          ax[ivar,modct].plot( datetime_list, nobs_used[:,ivar,modct],'k', \
                       datetime_list, nobs_sond[:,ivar,modct],'b', \
                       datetime_list, nobs_acft[:,ivar,modct],'g', \
                       datetime_list, nobs_sfc[:,ivar,modct],'r',  \
                       datetime_list, nobs_other[:,ivar,modct], 'grey')
          if (modct == 1):
             ax[ivar,modct].legend(('all used obs', 'sondes', 'aircrafts', 'surface'),
                  loc='center left', bbox_to_anchor=(1.02,0.5))
        if (modct == 0):
          ax[ivar,modct].set_ylabel('number of obs')
        minval = 0
        maxval = nobs_used[:,ivar,:].max()
        rangey=maxval-minval
        minax = minval - .05*rangey
        maxax = maxval + .05*rangey
        ax[ivar,modct].set_ylim((minax,maxax))
        ax[ivar,modct].set_xlim((datetime_list[0], datetime_list[len(datetime_list)-1]))
        ax[ivar,modct].grid(True)
        ax[ivar,modct].set_title('Number of conventional '+varnames[ivar]+' observations used in '+modelstreamnames[modct], fontsize=14, fontweight='bold')

        ax[ivar,modct].xaxis.set_major_locator(locator)
        ax[ivar,modct].xaxis.set_major_formatter(tick_format)

   fig.tight_layout(rect=[0, 0.05, 0.9, 0.95],h_pad=5)
   plt.text(0.05, 0.02, "Generated "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"UTC", fontsize=12, color='grey',transform=fig.transFigure)
   plt.savefig(imagepath+"/"+stream+"_obscounts.png")
   plt.close()
   #########################
   #########################
   #########################
   #########################


