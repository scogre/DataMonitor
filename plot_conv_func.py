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

def plot_conv_func(modelstreams,datapath,varb,plevel,region,begindate,enddate,figname):
   nummodel=len(modelstreams)
   enddate=str(enddate)
   begindate=str(begindate)

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

   
   if varb=='t':
      units='degC'
   elif varb=='u':
      units='m/s'
   elif varb=='v':
      units='m/s'
   elif varb=='q':
      units='mg/kg'
   elif varb=='gps':
      units='--'
   elif varb=='ps':
      units=''
   
   ##################################
   ##################################
   nobs_all  = ma.zeros((len(dates), nummodel));      nobs_all.mask  = True
   nobs_used = ma.zeros((len(dates), nummodel));      nobs_used.mask = True
   mean_obs_all  = ma.zeros((len(dates), nummodel));  mean_obs_all.mask  = True
   mean_obs_used = ma.zeros((len(dates), nummodel));  mean_obs_used.mask = True
   mean_omf_ctrl = ma.zeros((len(dates), nummodel));  mean_omf_ctrl.mask = True
   mean_oma_ctrl = ma.zeros((len(dates), nummodel));  mean_oma_ctrl.mask = True
   std_omf_ctrl  = ma.zeros((len(dates), nummodel));  std_omf_ctrl.mask  = True
   std_oma_ctrl  = ma.zeros((len(dates), nummodel));  std_oma_ctrl.mask  = True
   mean_omf_ens  = ma.zeros((len(dates), nummodel));  mean_omf_ens.mask  = True
   spread_f      = ma.zeros((len(dates), nummodel));  spread_f.mask      = True
   spread_obserr_f = ma.zeros((len(dates), nummodel));  spread_obserr_f.mask = True
   std_omf_ens   = ma.zeros((len(dates), nummodel));  std_omf_ens.mask   = True

   ##################################
   
   for modct in range(nummodel):
      for year in years:
        #print('modelstream=',modelstream)
        modelfile=datapath+'CONV_'+modelstreams[modct]+'_'+str(year)+'_'+varb+'_'+region+'.nc'
        anndata  = Dataset(modelfile, 'r')
        plevs = anndata['Plevels'][:].tolist()
        plevindex = plevs.index(int(plevel))
        thisdates = anndata['All_Dates'][:]
        indx_in = np.where(np.in1d(thisdates, dates)) [0]
        indx_out = np.where(np.in1d(dates, thisdates)) [0]
        ################
        nobs_all[indx_out,modct]  = anndata['nobs_all'][indx_in,plevindex]
        nobs_used[indx_out,modct] = anndata['nobs_used'][indx_in,plevindex]
        mean_obs_all[indx_out,modct]  = anndata['mean_obs_all'][indx_in,plevindex]
        mean_obs_used[indx_out,modct] = anndata['mean_obs_used'][indx_in,plevindex]
        mean_omf_ctrl[indx_out,modct] = anndata['mean_omf_ctrl'][indx_in,plevindex]
        mean_omf_ens[indx_out,modct]  = anndata['mean_omf_ens'][indx_in,plevindex]
        mean_oma_ctrl[indx_out,modct] = anndata['mean_oma_ctrl'][indx_in,plevindex]
        spread_f[indx_out,modct]      = anndata['spread_f'][indx_in,plevindex]
        std_omf_ens[indx_out,modct]   = anndata['std_omf_ens'][indx_in,plevindex]
        std_omf_ctrl[indx_out,modct]  = anndata['std_omf_ctrl'][indx_in,plevindex]
        spread_obserr_f[indx_out,modct] = anndata['spread_obserr_f'][indx_in,plevindex]
        std_oma_ctrl[indx_out,modct]  = anndata['std_oma_ctrl'][indx_in,plevindex]
        anndata.close()

   ####################################################
   if region=='SOUTH':
      geolabel='Southern Hemisphere'
   elif region=='TROPI':
      geolabel='Tropical +/-20deg'
   elif region=='NORTH':
      geolabel='Northern Hemisphere'
   elif region=='GLOBL':
      geolabel='Global'
   else:
      geolabel=''
   #############
   font = {'serif' : 'normal','weight' : 'bold','size'   : 12}
   mpl.rc('font', **font)
   mpl.rc('axes',titlesize=16)
   mpl.rc('legend', fontsize=10)
   #############
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

   ####
   zeroline=np.zeros(len(datetime_list))
   ####

   f, axarr = plt.subplots(5, 2, sharex='col', figsize=(20,15))
   if varb=='PS' or varb=='PW':
      f.suptitle('Conventional obs '+varb+' '+geolabel+' ', fontsize=16, fontweight='bold')
   else:
      f.suptitle('Conventional obs  '+varb+' '+geolabel+' '+str(plevel)+'_mb to '+str(int(plevel)+100)+'_mb', fontsize=16, fontweight='bold')


   for modct in range(nummodel):
      ######### PLOTTING
      modelname = modelstreams[modct]
      ####
      diagmean= nobs_all[:,modct].mean()
      usemean=  nobs_used[:,modct].mean()
   
      axarr[0,modct].plot(datetime_list, nobs_all[:,modct],'c',datetime_list, nobs_used[:,modct],'r')
      axarr[0,modct].set_ylabel('numobs')
   
      minval = min(nobs_all.min(), nobs_used.min())
      maxval = max(nobs_all.max(), nobs_used.max())
      axarr[0,modct].set_ylim((minval, maxval))
      axarr[0,modct].legend(( 'all DA obs, avg='+str(int(round(diagmean))), 'all DA use, avg='+str(int(round(usemean)))),loc='center left', bbox_to_anchor=(1.1, 0.5))
      axarr[0,modct].grid(True)
      axarr[0,modct].set_title('Number of Observations', fontsize=14, fontweight='bold')
      ####            
      ax2 = axarr[0,modct].twinx()
      ax2.plot(datetime_list, 100*nobs_used[:,modct]/nobs_all[:,modct],'g--', linewidth=3)
      ax2.set_ylabel('PERCENT', color='g')
      ax2.set_ylim((-5,105))
      for tl in ax2.get_yticklabels():
              tl.set_color('m')
      ax2.legend(('%DAuse/DAobs',), loc='lower left')
   
      ####
      diagmean= mean_obs_all[:,modct].mean()
      usemean=  mean_obs_used[:,modct].mean()
   
      axarr[1,modct].plot(datetime_list, mean_obs_all[:,modct],'g', datetime_list, mean_obs_used[:,modct],'m')
      axarr[1,modct].set_ylabel('MEAN '+units)
      minval = min(mean_obs_all.min(), mean_obs_used.min())
      maxval = max(mean_obs_all.max(), mean_obs_used.max())
      axarr[1,modct].set_ylim((minval,maxval))
      axarr[1,modct].legend(('all DA obs, avg='+str(round(diagmean,2)), 'all DA used obs, avg='+str(round(usemean,2))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[1,modct].grid(True)
      axarr[1,modct].set_title('Mean '+varb+' observation', fontsize=14, fontweight='bold')
      ####
      fcstmean= mean_omf_ctrl[:,modct].mean()
      analmean= mean_oma_ctrl[:,modct].mean()
      axarr[2,modct].plot(datetime_list, mean_omf_ctrl[:,modct],'r', datetime_list, mean_oma_ctrl[:,modct],'g')
      axarr[2,modct].set_ylabel('O-F, O-A mean '+units)
      minval = min(mean_omf_ctrl.min(), mean_oma_ctrl.min())
      maxval = max(mean_omf_ctrl.max(), mean_oma_ctrl.max())
      axarr[2,modct].set_ylim((minval,maxval))
      axarr[2,modct].legend(('O-F, avg='+str(round(fcstmean,2)), 'O-A, avg='+str(round(analmean,2))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[2,modct].grid(True)
      axarr[2,modct].plot(datetime_list, zeroline,'k--', linewidth=2)
      axarr[2,modct].set_title('First Guess and Analysis Biases', fontsize=14, fontweight='bold')
      ####
      sprdmean=    spread_f[:,modct].mean()
      sprderrmean= spread_obserr_f[:,modct].mean()
      ensstdmean=  std_omf_ens[:,modct].mean()
      fcststdmean= std_omf_ctrl[:,modct].mean()
      axarr[3,modct].plot( datetime_list, spread_f[:,modct],'m',datetime_list, spread_obserr_f[:,modct],'b',datetime_list,std_omf_ens[:,modct],'k',datetime_list, std_omf_ctrl[:,modct],'r')
      axarr[3,modct].set_ylabel('O-F '+units)
      minval = min(spread_f.min(), spread_obserr_f.min(), std_omf_ens.min(), std_omf_ctrl.min())
      maxval = max(spread_f.max(), spread_obserr_f.max(), std_omf_ens.max(), std_omf_ctrl.max())
      axarr[3,modct].set_ylim((minval,maxval))
      axarr[3,modct].legend(('ensemble spread, avg='+str(round(sprdmean,3)), 'spread + obs.err, avg='+str(round(sprderrmean,3)), 'O-F stddev (mean), avg='+str(round(ensstdmean,3)),'O-F stdev (control), avg='+str(round(fcststdmean,3))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[3,modct].grid(True)
      axarr[3,modct].set_title('First Guess spread and errors', fontsize=14, fontweight='bold')
      ####
      analstdmean= std_oma_ctrl[:,modct].mean()
      axarr[4,modct].plot( datetime_list, std_oma_ctrl[:,modct],'r')
      axarr[4,modct].set_ylabel('O-A '+units)
      minval = std_oma_ctrl.min()
      maxval = std_oma_ctrl.max()
      axarr[4,modct].set_ylim((minval,maxval))
      axarr[4,modct].legend(( 'control O-A std, avg='+str(round(analstdmean,3)),''),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[4,modct].grid(True)
      axarr[4,modct].set_title('Analysis spread and errors', fontsize=14, fontweight='bold')
      ####
      axarr[4,modct].xaxis.set_major_locator(locator)
      axarr[4,modct].xaxis.set_major_formatter(tick_format)
      for tick in axarr[4,modct].get_xticklabels():
          tick.set_rotation(70)

   f.tight_layout(rect=[0, 0.04, 0.88, 0.96], w_pad=14)
   plt.savefig(figname)
   plt.close()
   #########################
   #########################
   #########################
   #########################





