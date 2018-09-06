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

def plot_rad_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate,figname):
   channel=int(channel)
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

   channum_str=str(channel)
   nobs_all  = ma.zeros((len(dates), nummodel));      nobs_all.mask  = True
   nobs_qcd  = ma.zeros((len(dates), nummodel));      nobs_qcd.mask  = True
   nobs_used = ma.zeros((len(dates), nummodel));      nobs_used.mask = True
   mean_obs_all  = ma.zeros((len(dates), nummodel));  mean_obs_all.mask  = True
   mean_obs_used = ma.zeros((len(dates), nummodel));  mean_obs_used.mask = True
   mean_obs_qcd  = ma.zeros((len(dates), nummodel));  mean_obs_qcd.mask  = True
   mean_omf_ctrl = ma.zeros((len(dates), nummodel));  mean_omf_ctrl.mask = True
   mean_oma_ctrl = ma.zeros((len(dates), nummodel));  mean_oma_ctrl.mask = True
   std_omf_ctrl  = ma.zeros((len(dates), nummodel));  std_omf_ctrl.mask  = True
   std_oma_ctrl  = ma.zeros((len(dates), nummodel));  std_oma_ctrl.mask  = True
   mean_omf_ens  = ma.zeros((len(dates), nummodel));  mean_omf_ens.mask  = True
   spread_f      = ma.zeros((len(dates), nummodel));  spread_f.mask      = True
   spread_obserr_f = ma.zeros((len(dates), nummodel));  spread_obserr_f.mask = True
   std_omf_ens   = ma.zeros((len(dates), nummodel));  std_omf_ens.mask   = True
   mean_biascor  = ma.zeros((len(dates), nummodel));  mean_biascor.mask  = True
   std_biascor   = ma.zeros((len(dates), nummodel));  std_biascor.mask   = True

   for modct in range(nummodel):
      for year in years:
        #print('modelstream=',modelstream)
        modelfile=datapath+'/RAD_'+modelstreams[modct]+'_'+str(year)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
        anndata  = Dataset(modelfile, 'r')
        chans = anndata['Channels'][:].tolist()
        chanindx=chans.index(channel)
        thisdates = anndata['All_Dates'][:]
        indx_in = np.where(np.in1d(thisdates, dates)) [0]
        indx_out = np.where(np.in1d(dates, thisdates)) [0]
        ################
        nobs_all[indx_out,modct]  = anndata['nobs_all'][indx_in,chanindx]
        nobs_qcd[indx_out,modct]  = anndata['nobs_qcd'][indx_in,chanindx]
        nobs_used[indx_out,modct] = anndata['nobs_used'][indx_in,chanindx]
        mean_obs_all[indx_out,modct]  = anndata['mean_obs_all'][indx_in,chanindx]
        mean_obs_used[indx_out,modct] = anndata['mean_obs_used'][indx_in,chanindx]
        mean_obs_qcd[indx_out,modct]  = anndata['mean_obs_qcd'][indx_in,chanindx]
        mean_omf_ctrl[indx_out,modct] = anndata['mean_omf_ctrl'][indx_in,chanindx]
        mean_oma_ctrl[indx_out,modct] = anndata['mean_oma_ctrl'][indx_in,chanindx]
        std_omf_ctrl[indx_out,modct]  = anndata['std_omf_ctrl'][indx_in,chanindx]
        std_oma_ctrl[indx_out,modct]  = anndata['std_oma_ctrl'][indx_in,chanindx]
        mean_omf_ens[indx_out,modct]  = anndata['mean_omf_ens'][indx_in,chanindx]
        spread_f[indx_out,modct]      = anndata['spread_f'][indx_in,chanindx]
        spread_obserr_f[indx_out,modct] = anndata['spread_obserr_f'][indx_in,chanindx]
        std_omf_ens[indx_out,modct]   = anndata['std_omf_ens'][indx_in,chanindx]
        mean_biascor[indx_out,modct]  = anndata['mean_biascor'][indx_in,chanindx]
        std_biascor[indx_out,modct]   = anndata['std_biascor'][indx_in,chanindx]
        anndata.close()

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
   f, axarr = plt.subplots(6,2, sharex='col', figsize=(20, 17))#plt.subplots(figsize=(20, 10))

   for modct in range(nummodel):
      model=modelstreams[modct]
      ######### PLOTTING
      zeroline=np.zeros(len(datetime_list))
   
      #############
      axarr[0,modct].plot(datetime_list, nobs_all[:,modct],'k', datetime_list, nobs_qcd[:,modct],'r')
      f.suptitle(model+' '+instrmnt+' '+satlite+' '+region+' chan '+channum_str, fontsize=20, fontweight='bold')
      axarr[0,modct].set_ylabel('numobs')
      maxA = max(nobs_all.max(),nobs_qcd.max())
      minA = min(nobs_all.min(),nobs_qcd.min())
      axarr[0,modct].set_ylim((minA,maxA))
      axarr[0,modct].legend(('all DA obs, avg='+str(int(round(nobs_all[:,modct].mean()))), 'QCd DA obs, avg='+str(int(round(nobs_qcd[:,modct].mean())))),loc='center left', bbox_to_anchor=(1.1, 0.5))
      axarr[0,modct].grid(True)
      axarr[0,modct].set_title('Number of Observations', fontsize=14, fontweight='bold')
      #############
      ax2 = axarr[0,modct].twinx()
      ax2.plot(datetime_list, 100*nobs_qcd[:,modct]/nobs_all[:,modct],'g--', linewidth=3)
      ax2.set_ylabel('PERCENT', color='g')
      ax2.set_ylim((-5,105))
      for tl in ax2.get_yticklabels():
         tl.set_color('m')
      ax2.legend(('%qc/DAobs',), loc='lower left')
   
      #############
      diagmean= mean_obs_all[:,modct].mean()
      qcmean= mean_obs_qcd[:,modct].mean()
   
      axarr[1,modct].plot(datetime_list, mean_obs_all[:,modct],'g', datetime_list, mean_obs_qcd[:,modct],'m')
      axarr[1,modct].set_ylabel('Tmean')
      maxA = max(mean_obs_all.max(),mean_obs_qcd.max())
      minA = min(mean_obs_all.min(),mean_obs_qcd.min())
      axarr[1,modct].set_ylim((minA,maxA))
      axarr[1,modct].legend(( 'all DA obs, avg='+str(round(diagmean,2)), 'QCd DA obs, avg='+str(round(qcmean,2))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[1,modct].grid(True)
      axarr[1,modct].set_title('Mean Observation', fontsize=14, fontweight='bold')
      ##################
      biascorravgmean= mean_biascor[:,modct].mean()
      biascorrstdmean= std_biascor[:,modct].mean()
      axarr[2,modct].plot(datetime_list, mean_biascor[:,modct],'g', datetime_list, std_biascor[:,modct],'m')
      axarr[2,modct].set_ylabel('biascorxn')
      maxA = max(mean_biascor.max(),std_biascor.max())
      minA = min(mean_biascor.min(),std_biascor.min())
      axarr[2,modct].set_ylim((minA,maxA))
      axarr[2,modct].legend(('mean, avg='+str(round(biascorravgmean,3)), 'std, avg='+str(round(biascorrstdmean,3))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[2,modct].grid(True)
      axarr[2,modct].plot(datetime_list, zeroline,'k--', linewidth=2)
      axarr[2,modct].set_title('Bias Correction Statistics', fontsize=14, fontweight='bold')
      ##################
      OmFmean= mean_omf_ctrl[:,modct].mean()
      OmAmean= mean_oma_ctrl[:,modct].mean()
      axarr[3,modct].plot(datetime_list, mean_omf_ctrl[:,modct],'r', datetime_list, mean_oma_ctrl[:,modct],'g')
      axarr[3,modct].set_ylabel('O-F,  O-A mean')
      maxA = max(mean_omf_ctrl.max(),mean_oma_ctrl.max())
      minA = min(mean_omf_ctrl.min(),mean_oma_ctrl.min())
      axarr[3,modct].set_ylim((minA,maxA))
      axarr[3,modct].legend(('O-F, avg='+str(round(OmFmean,3)), 'O-A, avg='+str(round(OmAmean,3))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[3,modct].grid(True)
      axarr[3,modct].plot(datetime_list, zeroline,'k--', linewidth=2)
      axarr[3,modct].set_title('First Guess and Analysis Bias', fontsize=14, fontweight='bold')
      #################
      ENSsprdmean= spread_f[:,modct].mean()
      ENSsprderrmean= spread_obserr_f[:,modct].mean()
      ENSOmFstdmean= std_omf_ens[:,modct].mean()
      OmFstdmean= std_omf_ctrl[:,modct].mean()
      axarr[4,modct].plot(  datetime_list, spread_f[:,modct],'m', datetime_list, spread_obserr_f[:,modct],'b',datetime_list, std_omf_ens[:,modct],'k',datetime_list, std_omf_ctrl[:,modct],'r',)
      axarr[4,modct].set_ylabel('O-F')
      maxA = max(spread_f.max() ,spread_obserr_f.max(), std_omf_ens.max(), std_omf_ctrl.max())
      minA = min(spread_f.min() ,spread_obserr_f.min(), std_omf_ens.min(), std_omf_ctrl.min())
      axarr[4,modct].set_ylim((minA,maxA))
      axarr[4,modct].legend(( 'ensemble spread, avg='+str(round(ENSsprdmean,3)), 'spread + obs.err, avg='+str(round(ENSsprderrmean,3)), 'O-F stdev (mean), avg='+str(round(ENSOmFstdmean,3)),'O-F stdev (control), avg='+str(round(OmFstdmean,3))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[4,modct].grid(True)
      axarr[4,modct].set_title('First Guess Spread and Errors', fontsize=14, fontweight='bold')
      ################        
      OmAstdmean= std_oma_ctrl[:,modct].mean()
      axarr[5,modct].plot(datetime_list, std_oma_ctrl[:,modct],'r')
      axarr[5,modct].set_ylabel('O-A std')
      maxA =  std_oma_ctrl.max()
      minA =  std_oma_ctrl.min()
      axarr[5,modct].set_ylim((minA,maxA))
      #####################################
      axarr[5,modct].legend(( 'O-A stdev (control), avg='+str(round(OmAstdmean,3)),' '),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[5,modct].grid(True)
      axarr[5,modct].set_title('Analysis Spread and Errors', fontsize=14, fontweight='bold')
   
      axarr[5,modct].xaxis.set_major_locator(locator)
      axarr[5,modct].xaxis.set_major_formatter(tick_format)
   
      for tick in axarr[5,modct].get_xticklabels():
         tick.set_rotation(70)
   f.tight_layout(rect=[0, 0.04, 0.88, 0.96], w_pad=14)
   plt.savefig(figname)
   plt.close()
   ##############################




