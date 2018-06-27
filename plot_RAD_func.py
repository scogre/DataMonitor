import numpy as np
from netCDF4 import Dataset
import datetime
import time
from datetime import datetime, date, time
from datetime import timedelta
import matplotlib as mpl
mpl.use('Agg') #for web 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter, DayLocator, HourLocator, AutoDateLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from matplotlib.ticker import LinearLocator
import sys, os, os.path, cgi, re

nan=float('nan')

def plot_RAD_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate):
   nummodel=len(modelstreams)
   plotpath=datapath
   ##############################
   ##############################
   modelstream=modelstreams[1]
   beginyr=str(begindate)[0:4]
   endyr=str(enddate)[0:4]
   if beginyr==endyr:
      numyearfiles=1
      modelfile=['']*numyearfiles
      modelfile[0]=datapath+'RAD_'+modelstream+'_'+str(beginyr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      anndataA  = Dataset(modelfile[0], 'r')
      alldatesA = anndataA['All_Dates'][:].tolist()
      startindx=alldatesA.index(begindate)
      endindx=alldatesA.index(enddate)
      dateindcsA=np.arange(startindx,endindx+1,1).tolist()
      dateindcs = dateindcsA
      querydates=[]
      for di in dateindcsA:
         querydates.append(alldatesA[di])
      #querydates=alldatesA[startindx:endindx+1]
      numquerydates=len(querydates)
      del anndataA
      del modelfile
   else:
      numyearfiles=2
      modelfile=['']*numyearfiles
      modelfile[0]=datapath+'RAD_'+modelstream+'_'+str(beginyr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      anndataA  = Dataset(modelfile[0], 'r')
      alldatesA = anndataA['All_Dates'][:].tolist()
      startindx=alldatesA.index(begindate)
      dateindcsA=np.arange(startindx,len(alldatesA),1).tolist()
      querydatesA=[]
      for diA in dateindcsA:
         querydatesA.append(alldatesA[diA])
      #querydatesA=alldatesA[startindx:len(alldatesA)]
      numquerydatesA = len(querydatesA)
      ######################################################
      modelfile[1]=datapath+'RAD_'+modelstream+'_'+str(endyr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      anndataB  = Dataset(modelfile[1], 'r')
      alldatesB = anndataB['All_Dates'][:].tolist()
      endindx=alldatesB.index(enddate)
      dateindcsB=np.arange(0,endindx+1,1).tolist()
      querydatesB=[]
      for diB in dateindcsB:
         querydatesB.append(alldatesB[diB])
      #querydatesB=alldatesB[0:endindx+1]
      numquerydatesB = len(querydatesB)
      combo_dateindcs = sum([dateindcsA,dateindcsB],[])
      querydates = sum([querydatesA, querydatesB],[])
      numquerydates = len(querydates)
      ############
      dateindcs=sum([dateindcsA,(np.max(dateindcsA)+np.asarray(dateindcsB)+1).tolist() ],[])
      del anndataA
      del anndataB
      del modelfile
   channum_str=str(channel)
   nobs_all_chan = nan*np.ones((numquerydates,nummodel))
   nobs_qcd_chan = nan*np.ones((numquerydates,nummodel))
   nobs_used_chan = nan*np.ones((numquerydates,nummodel))
   mean_obs_all_chan = nan*np.ones((numquerydates,nummodel))
   mean_obs_used_chan = nan*np.ones((numquerydates,nummodel))
   mean_obs_qcd_chan = nan*np.ones((numquerydates,nummodel))
   mean_omf_ctrl_chan = nan*np.ones((numquerydates,nummodel))
   mean_oma_ctrl_chan = nan*np.ones((numquerydates,nummodel))
   std_omf_ctrl_chan = nan*np.ones((numquerydates,nummodel))
   std_oma_ctrl_chan = nan*np.ones((numquerydates,nummodel))
   mean_omf_ens_chan = nan*np.ones((numquerydates,nummodel))
   spread_f_chan = nan*np.ones((numquerydates,nummodel))
   spread_obserr_f_chan = nan*np.ones((numquerydates,nummodel))
   std_omf_ens_chan = nan*np.ones((numquerydates,nummodel))
   mean_biascor_chan = nan*np.ones((numquerydates,nummodel))
   std_biascor_chan = nan*np.ones((numquerydates,nummodel))
   
   modct=0
   for modelstream in modelstreams:
      print('modelstream=',modelstream)
      modelfile=datapath+'/RAD_'+modelstream+'_'+str(beginyr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      anndataA  = Dataset(modelfile, 'r')
      del modelfile
      chans = anndataA['Channels'][:].tolist()
      chanindx=chans.index(channel)
   ################
      nobs_all = anndataA['nobs_all'][:][:]
      nobs_qcd = anndataA['nobs_qcd'][:][:]
      nobs_used = anndataA['nobs_used'][:][:]
      mean_obs_all = anndataA['mean_obs_all'][:][:]
      mean_obs_used = anndataA['mean_obs_used'][:][:]
      mean_obs_qcd = anndataA['mean_obs_qcd'][:][:]
      mean_omf_ctrl = anndataA['mean_omf_ctrl'][:][:]
      mean_oma_ctrl = anndataA['mean_oma_ctrl'][:][:]
      std_omf_ctrl = anndataA['std_omf_ctrl'][:][:]
      std_oma_ctrl = anndataA['std_oma_ctrl'][:][:]
      mean_omf_ens = anndataA['mean_omf_ens'][:][:]
      spread_f = anndataA['spread_f'][:][:]
      spread_obserr_f = anndataA['spread_obserr_f'][:][:]
      std_omf_ens = anndataA['std_omf_ens'][:][:]
      mean_biascor = anndataA['mean_biascor'][:][:]
      std_biascor = anndataA['std_biascor'][:][:]
      if beginyr!=endyr:
         dateindcs=concatindcs
         modelfile=datapath+'RAD_'+modelstream+'_'+str(endyr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
         anndataB  = Dataset(modelfile, 'r')
         del modelfile
         nobs_all = np.asarray(sum([nobs_all.tolist(), (anndataB['nobs_all'][:][:]).tolist()],[]))
         nobs_qcd = np.asarray(sum([nobs_qcd.tolist(), (anndataB['nobs_qcd'][:][:]).tolist()],[]))
         nobs_used = np.asarray(sum([nobs_used.tolist(), (anndataB['nobs_used'][:][:]).tolist()],[]))
         mean_obs_all = np.asarray(sum([mean_obs_all.tolist(), (anndataB['mean_obs_all'][:][:]).tolist()],[]))
         mean_obs_used = np.asarray(sum([mean_obs_used.tolist(), (anndataB['mean_obs_used'][:][:]).tolist()],[]))
         mean_obs_qcd = np.asarray(sum([mean_obs_qcd.tolist(), (anndataB['mean_obs_qcd'][:][:]).tolist()],[]))
         mean_omf_ctrl = np.asarray(sum([mean_omf_ctrl.tolist(), (anndataB['mean_omf_ctrl'][:][:]).tolist()],[]))
         mean_oma_ctrl = np.asarray(sum([mean_oma_ctrl.tolist(), (anndataB['mean_oma_ctrl'][:][:]).tolist()],[]))
         std_omf_ctrl = np.asarray(sum([std_omf_ctrl.tolist(), (anndataB['std_omf_ctrl'][:][:]).tolist()],[]))
         std_oma_ctrl = np.asarray(sum([std_oma_ctrl.tolist(), (anndataB['std_oma_ctrl'][:][:]).tolist()],[]))
         mean_omf_ens = np.asarray(sum([mean_omf_ens.tolist(), (anndataB['mean_omf_ens'][:][:]).tolist()],[]))
         spread_f = np.asarray(sum([spread_f.tolist(), (anndataB['spread_f'][:][:]).tolist()],[]))
         spread_obserr_f = np.asarray(sum([spread_obserr_f.tolist(), (anndataB['spread_obserr_f'][:][:]).tolist()],[]))
         std_omf_ens = np.asarray(sum([std_omf_ens.tolist(), (anndataB['std_omf_ens'][:][:]).tolist()],[]))
         mean_biascor = np.asarray(sum([mean_biascor.tolist(), (anndataB['mean_biascor'][:][:]).tolist()],[]))
         std_biascor = np.asarray(sum([std_biascor.tolist(), (anndataB['std_biascor'][:][:]).tolist()],[]))
      nobs_all_chan[:,modct]        = nobs_all[dateindcs,chanindx]
      print('nobs_all_chan=',nobs_all_chan)
      nobs_qcd_chan[:,modct]        = nobs_qcd[dateindcs,chanindx]
      nobs_used_chan[:,modct]       = nobs_used[dateindcs,chanindx]
      mean_obs_all_chan[:,modct]    = mean_obs_all[dateindcs,chanindx]
      mean_obs_used_chan[:,modct]   = mean_obs_used[dateindcs,chanindx]
      mean_obs_qcd_chan[:,modct]    = mean_obs_qcd[dateindcs,chanindx]
      mean_omf_ctrl_chan[:,modct]   = mean_omf_ctrl[dateindcs,chanindx]
      mean_oma_ctrl_chan[:,modct]   = mean_oma_ctrl[dateindcs,chanindx]
      std_omf_ctrl_chan[:,modct]    = std_omf_ctrl[dateindcs,chanindx]
      std_oma_ctrl_chan[:,modct]    = std_oma_ctrl[dateindcs,chanindx]
      mean_omf_ens_chan[:,modct]    = mean_omf_ens[dateindcs,chanindx]
      spread_f_chan[:,modct]        = spread_f[dateindcs,chanindx]
      spread_obserr_f_chan[:,modct] = spread_obserr_f[dateindcs,chanindx]
      std_omf_ens_chan[:,modct]     = std_omf_ens[dateindcs,chanindx]
      mean_biascor_chan[:,modct]    = mean_biascor[dateindcs,chanindx]
      std_biascor_chan[:,modct]     = std_biascor[dateindcs,chanindx]
      modct=modct+1
   maxNdiag=np.nanmax(nobs_all_chan);      minNdiag =np.nanmin(nobs_all_chan);      rangeNdiag = maxNdiag-minNdiag
   maxNuse =np.nanmax(nobs_used_chan);     minNuse  =np.nanmin(nobs_used_chan);     rangeNuse = maxNuse-minNuse
   maxNqc  =np.nanmax(nobs_qcd_chan);      minNqc   =np.nanmin(nobs_qcd_chan);      rangeNqc = maxNqc-minNqc
   
   maxTd=np.nanmax(mean_obs_all_chan);     minTd=np.nanmin(mean_obs_all_chan);
   maxTu=np.nanmax(mean_obs_used_chan);    minTu=np.nanmin(mean_obs_used_chan);
   maxTq=np.nanmax(mean_obs_qcd_chan);     minTq=np.nanmin(mean_obs_qcd_chan);
   
   maxBCavg=np.nanmax(mean_biascor_chan);  minBCavg=np.nanmin(mean_biascor_chan);
   maxBCstd=np.nanmax(std_biascor_chan);   minBCstd=np.nanmin(std_biascor_chan);
   
   maxOmF_wBCmean=np.nanmax(mean_omf_ctrl_chan);         minOmF_wBCmean=np.nanmin(mean_omf_ctrl_chan);
   maxOmF_wBCstd =np.nanmax(std_omf_ctrl_chan);          minOmF_wBCstd =np.nanmin(std_omf_ctrl_chan);
   maxOmA_wBCmean=np.nanmax(mean_oma_ctrl_chan);         minOmA_wBCmean=np.nanmin(mean_oma_ctrl_chan);
   maxOmA_wBCstd =np.nanmax(std_oma_ctrl_chan);          minOmA_wBCstd =np.nanmin(std_oma_ctrl_chan);
   
   maxENS_OmF_wBC_std   =np.nanmax(std_omf_ens_chan);         minENS_OmF_wBC_std  =np.nanmin(std_omf_ens_chan);
   maxENSspredF_mean    =np.nanmax(spread_f_chan);            minENSspredF_mean   =np.nanmin(spread_f_chan);
   maxENSsprederrF_mean =np.nanmax(spread_obserr_f_chan);     minENSsprederrF_mean=np.nanmin(spread_obserr_f_chan);
   
   print('querydates=',querydates)
   print('mean_omf_ctrl_chan.shape=',mean_omf_ctrl_chan.shape)
   print('FINISHED')
   
   
   for modct in range(nummodel):
      model=modelstreams[modct]
      ######### PLOTTING
      modelname = model
      if region=='SOUTH':
         geolabelfilename='SOUTH'
         geolabel='Southern Hemisphere'
      elif region=='TROPI':
         geolabelfilename='TROPI'
         geolabel='Tropical +/-20deg'
      elif region=='NORTH':
         geolabelfilename='NORTH'
         geolabel='Northern Hemisphere'
      elif region=='GLOBL':
         geolabelfilename='GLOBL'
         geolabel='Global'
      else:
         geolabelfilename=''
         geolabel=''
      yr=np.empty(numquerydates)
      mo=np.empty(numquerydates)
      da=np.empty(numquerydates)
      hr=np.empty(numquerydates)
      datetime_list=[]
      date_list_4plot=[]
      ##############
   
      #############
      for n in range(numquerydates):
         DATEstring=str(querydates[n])
         yr[n]=DATEstring[0:4]
         mo[n]=DATEstring[4:6]
         da[n]=DATEstring[6:8]
         hr[n]=DATEstring[8:10]
         time_dum = "%4d/%02d/%02d %02d:00:00" %(yr[n], mo[n], da[n], hr[n])
         if n==0:
            time_start=time_dum
         timestrp=datetime.strptime(time_dum,"%Y/%m/%d %H:%M:%S")
         datetime_list.append(timestrp)
         temp= timestrp.strftime("%d/%m/%Y %H:%M")
         date_list_4plot.append(temp)
      timestart_strp=datetime.strptime(time_start,"%Y/%m/%d %H:%M:%S")
      timediff=timestrp - timestart_strp
      #############
   
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
      PLOTpath = plotpath
      os.system("mkdir -p "+PLOTpath)
      print 'plotpath=',PLOTpath
   
      figname=PLOTpath+model+'_'+instrmnt+'_'+satlite+'_ch'+channum_str+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png'
      print('figname=',figname)
      #############
      f, axarr = plt.subplots(6, sharex=True, figsize=(17, 17))#plt.subplots(figsize=(20, 10))
      #############
   
      #############
      zeroline=np.zeros(len(datetime_list))
      #############
   
      #############
      Ndiagmean= np.nanmean(nobs_all_chan[:,modct])
      Nqcmean= np.nanmean(nobs_qcd_chan[:,modct])
   
      axarr[0].plot(datetime_list, nobs_all_chan[:,modct],'k', datetime_list, nobs_qcd_chan[:,modct],'r')
      f.suptitle(model+' '+instrmnt+' '+satlite+' '+region+' chan '+channum_str, fontsize=20, fontweight='bold')
      axarr[0].set_ylabel('numobs')
      box = axarr[0].get_position()
      #####################################
      maxA = np.nanmax((maxNdiag,maxNqc))
      minA = np.nanmin((minNdiag,minNqc))
      rangey=maxA-minA
      maxy= maxA + .05*rangey
      miny= minA - .05*rangey
      axarr[0].set_ylim((miny,maxy))
      del maxy
      del miny
      #####################################
      axarr[0].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[0].legend(('all DA obs, avg='+str(int(round(Ndiagmean))), 'QCd DA obs, avg='+str(int(round(Nqcmean)))),loc='center left', bbox_to_anchor=(1.05, 0.5))
      axarr[0].grid(True)
      axarr[0].set_title('Number of Observations', fontsize=14, fontweight='bold')
      del Nqcmean
      del Ndiagmean
      #############
      #############
      ax2 = axarr[0].twinx()
      ax2.plot(datetime_list, 100*nobs_qcd_chan[:,modct]/nobs_all_chan[:,modct],'g--', linewidth=3)
   
      print('numobstot(bufr)=',nobs_all_chan[:,modct])
   
      ax2.set_ylabel('PERCENT', color='g')
      ax2.set_ylim((-5,105))
      for tl in ax2.get_yticklabels():
         tl.set_color('m')
   
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * 0.85, box.height])
      #ax2.legend(('%DAobs/bufr', '%qc/DAobs'), loc='lower left')
      ax2.legend(('%qc/DAobs',), loc='lower left')
      #############
   
   
      #############
      diagmean= np.nanmean(mean_obs_all_chan[:,modct])
      qcmean= np.nanmean(mean_obs_qcd_chan[:,modct])
   
      axarr[1].plot(datetime_list, mean_obs_all_chan[:,modct],'g', datetime_list, mean_obs_qcd_chan[:,modct],'m')
      axarr[1].set_ylabel('Tmean')
      box = axarr[1].get_position()
      #####################################
      maxA = np.nanmax((maxTd,maxTq))
      minA = np.nanmin((minTd,minTq))
      rangey=maxA-minA
      maxy= maxA + .05*rangey
      miny= minA - .05*rangey
      axarr[1].set_ylim((miny,maxy))
      del maxy
      del miny
      #####################################
      axarr[1].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[1].legend(( 'all DA obs, avg='+str(round(diagmean,2)), 'QCd DA obs, avg='+str(round(qcmean,2))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[1].grid(True)
      axarr[1].set_title('Mean Observation', fontsize=14, fontweight='bold')
      del diagmean
      del qcmean
      ##################
   
   
      ##################
      biascorravgmean= np.nanmean(mean_biascor_chan[:,modct])
      biascorrstdmean= np.nanmean(std_biascor_chan[:,modct])
      axarr[2].plot(datetime_list, mean_biascor_chan[:,modct],'g', datetime_list, std_biascor_chan[:,modct],'m')
      axarr[2].set_ylabel('biascorxn')
      box = axarr[2].get_position()
      #####################################
      maxA = np.nanmax((maxBCavg,maxBCstd))
      minA = np.nanmin((minBCavg,minBCstd))
      rangey=maxA-minA
      maxy= maxA + .05*rangey
      miny= minA - .05*rangey
      axarr[2].set_ylim((miny,maxy))
      del maxy
      del miny
      #####################################
      axarr[2].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[2].legend(('mean, avg='+str(round(biascorravgmean,3)), 'std, avg='+str(round(biascorrstdmean,3))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[2].grid(True)
      axarr[2].plot(datetime_list, zeroline,'k--', linewidth=2)
      axarr[2].set_title('Bias Correction Statistics', fontsize=14, fontweight='bold')
      del biascorravgmean
      del biascorrstdmean
      ##################
   
   
      ##################
      OmFmean= np.nanmean(mean_omf_ctrl_chan[:,modct])
      OmAmean= np.nanmean(mean_oma_ctrl_chan[:,modct])
   
      axarr[3].plot(datetime_list, mean_omf_ctrl_chan[:,modct],'r', datetime_list, mean_oma_ctrl_chan[:,modct],'g')
      axarr[3].set_ylabel('O-F,  O-A mean')
      box = axarr[3].get_position()
      #####################################
      maxA = np.nanmax((maxOmF_wBCmean,maxOmA_wBCmean))
      minA = np.nanmin((minOmF_wBCmean,minOmA_wBCmean))
      rangey=maxA-minA
      maxy= maxA + .05*rangey
      miny= minA - .05*rangey
      axarr[3].set_ylim((miny,maxy))
      del maxy
      del miny
      #####################################
      axarr[3].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[3].legend(('O-F, avg='+str(round(OmFmean,3)), 'O-A, avg='+str(round(OmAmean,3))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[3].grid(True)
      axarr[3].plot(datetime_list, zeroline,'k--', linewidth=2)
      axarr[3].set_title('First Guess and Analysis Bias', fontsize=14, fontweight='bold')
      del OmFmean
      del OmAmean
      #################
   
   
      #################
      ENSsprdmean= np.nanmean(spread_f_chan[:,modct])
      ENSsprderrmean= np.nanmean(spread_obserr_f_chan[:,modct])
      ENSOmFstdmean= np.nanmean(std_omf_ens_chan[:,modct])
      OmFstdmean= np.nanmean(std_omf_ctrl_chan[:,modct])
      axarr[4].plot(  datetime_list, spread_f_chan[:,modct],'m', datetime_list, spread_obserr_f_chan[:,modct],'b',datetime_list, std_omf_ens_chan[:,modct],'k',datetime_list, std_omf_ctrl_chan[:,modct],'r',)
      axarr[4].set_ylabel('O-F')
      box = axarr[4].get_position()
      #####################################
      maxA = np.nanmax((maxENSspredF_mean ,maxENSsprederrF_mean, maxENS_OmF_wBC_std, maxOmF_wBCstd))
      minA = np.nanmin((minENSspredF_mean ,minENSsprederrF_mean, minENS_OmF_wBC_std, minOmF_wBCstd))
      rangey=maxA-minA
      maxy= maxA + .05*rangey
      miny= minA - .05*rangey
      axarr[4].set_ylim((miny,maxy))
      del maxy
      del miny
      #####################################
      axarr[4].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[4].legend(( 'ensemble spread, avg='+str(round(ENSsprdmean,3)), 'spread + obs.err, avg='+str(round(ENSsprderrmean,3)), 'O-F stdev (mean), avg='+str(round(ENSOmFstdmean,3)),'O-F stdev (control), avg='+str(round(OmFstdmean,3))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[4].grid(True)
      axarr[4].set_title('First Guess Spread and Errors', fontsize=14, fontweight='bold')
      del ENSsprdmean
      del ENSsprderrmean
      del ENSOmFstdmean
      del OmFstdmean
      ################        
   
   
      ################        
      OmAstdmean= np.nanmean(std_oma_ctrl_chan[:,modct])
      axarr[5].plot(datetime_list, std_oma_ctrl_chan[:,modct],'r')
      axarr[5].set_ylabel('O-A std')
      box = axarr[5].get_position()
      #####################################
      maxA =  maxOmA_wBCstd
      minA =  minOmA_wBCstd
      rangey=maxA-minA
      maxy= maxA + .05*rangey
      miny= minA - .05*rangey
      axarr[5].set_ylim((miny,maxy))
      del maxy
      del miny
      #####################################
      axarr[5].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[5].legend(( 'O-A stdev (control), avg='+str(round(OmAstdmean,3)),' '),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[5].grid(True)
      axarr[5].set_title('Analysis Spread and Errors', fontsize=14, fontweight='bold')
      del OmAstdmean
   
      axarr[5].xaxis.set_major_locator(locator)
      axarr[5].xaxis.set_major_formatter(tick_format)
   
      for tick in axarr[5].get_xticklabels():
         tick.set_rotation(70)
      os.system("rm "+figname)
      plt.savefig(figname)
      del model
      del PLOTpath
   ##############################





