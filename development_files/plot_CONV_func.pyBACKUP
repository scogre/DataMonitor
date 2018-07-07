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


##############################
def plot_CONV_func(modelstreams,datapath,varb,plevel,region,begindate,enddate):
   nummodel=len(modelstreams)
   plotpath=datapath
   ##############################
   modelstream=modelstreams[1]
   beginyr=str(begindate)[0:4]
   endyr=str(enddate)[0:4]
   if beginyr==endyr:
      numyearfiles=1
      modelfile=['']*numyearfiles
      modelfile[0]=datapath+'CONV_'+varb+'_'+modelstream+'_'+str(beginyr)+'_'+region+'.nc'
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
      modelfile[0]=datapath+'CONV_'+varb+'_'+modelstream+'_'+str(beginyr)+'_'+region+'.nc'
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
      modelfile[1]=datapath+'CONV_'+varb+'_'+modelstream+'_'+str(endyr)+'_'+region+'.nc'
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
   
   
   ##variables=['t','u','v','q','gps']
   
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
   
   ##################################
   ##################################
   nobs_all_plev = nan*np.ones((numquerydates,nummodel))
   nobs_used_plev = nan*np.ones((numquerydates,nummodel))
   mean_obs_all_plev = nan*np.ones((numquerydates,nummodel))
   mean_obs_used_plev = nan*np.ones((numquerydates,nummodel))
   mean_omf_ctrl_plev = nan*np.ones((numquerydates,nummodel))
   mean_omf_ens_plev = nan*np.ones((numquerydates,nummodel))
   mean_oma_ctrl_plev = nan*np.ones((numquerydates,nummodel))
   mean_oma_ens_plev = nan*np.ones((numquerydates,nummodel))
   spread_f_plev = nan*np.ones((numquerydates,nummodel))
   std_omf_ens_plev = nan*np.ones((numquerydates,nummodel))
   std_omf_ctrl_plev = nan*np.ones((numquerydates,nummodel))
   spread_obserr_f_plev = nan*np.ones((numquerydates,nummodel))
   spread_a_plev = nan*np.ones((numquerydates,nummodel))
   std_oma_ens_plev = nan*np.ones((numquerydates,nummodel))
   std_oma_ctrl_plev = nan*np.ones((numquerydates,nummodel))
   spread_obserr_a_plev = nan*np.ones((numquerydates,nummodel))
   ##################################
   
   
   modct=0
   for modelstream in modelstreams:
      print('modelstream=',modelstream)
      modelfile=datapath+'CONV_'+varb+'_'+modelstream+'_'+str(beginyr)+'_'+region+'.nc'
      anndataA  = Dataset(modelfile, 'r')
      del modelfile
      #chans = anndataA['Channels'][:].tolist()
      #chanindx=chans.index(channel)
      plevs = anndataA['Plevels'][:].tolist()
      plevindex = plevs.index(plevel)
      ################
      nobs_all = anndataA['nobs_all'][:][:]
      nobs_used = anndataA['nobs_used'][:][:]
      mean_obs_all = anndataA['mean_obs_all'][:][:]
      mean_obs_used = anndataA['mean_obs_used'][:][:]
      mean_omf_ctrl = anndataA['mean_omf_ctrl'][:][:]
      mean_omf_ens = anndataA['mean_omf_ens'][:][:]
      mean_oma_ctrl = anndataA['mean_oma_ctrl'][:][:]
      mean_oma_ens = anndataA['mean_oma_ens'][:][:]
      spread_f = anndataA['spread_f'][:][:]
      std_omf_ens = anndataA['std_omf_ens'][:][:]
      std_omf_ctrl = anndataA['std_omf_ctrl'][:][:]
      spread_obserr_f = anndataA['spread_obserr_f'][:][:]
      spread_a = anndataA['spread_a'][:][:]
      std_oma_ens = anndataA['std_oma_ens'][:][:]
      std_oma_ctrl = anndataA['std_oma_ctrl'][:][:]
      spread_obserr_a = anndataA['spread_obserr_a'][:][:]
      if beginyr!=endyr:
         dateindcs=concatindcs
         modelfile=datapath+'CONV_'+varb+'_'+modelstream+'_'+str(beginyr)+'_'+region+'.nc'
         anndataB  = Dataset(modelfile, 'r')
         del modelfile
         nobs_all        = np.asarray(sum([nobs_all.tolist(),       (anndataB['nobs_all'][:][:]).tolist()],[]))
         nobs_used       = np.asarray(sum([nobs_used.tolist(),      (anndataB['nobs_used'][:][:]).tolist()],[]))
         mean_obs_all    = np.asarray(sum([mean_obs_all.tolist(),   (anndataB['mean_obs_all'][:][:]).tolist()],[]))
         mean_obs_used   = np.asarray(sum([mean_obs_used.tolist(),  (anndataB['mean_obs_used'][:][:]).tolist()],[]))
         mean_omf_ctrl   = np.asarray(sum([mean_omf_ctrl.tolist(),  (anndataB['mean_omf_ctrl'][:][:]).tolist()],[]))
         mean_omf_ens    = np.asarray(sum([mean_omf_ens.tolist(),   (anndataB['mean_omf_ens'][:][:]).tolist()],[]))
         mean_oma_ctrl   = np.asarray(sum([mean_oma_ctrl.tolist(),  (anndataB['mean_oma_ctrl'][:][:]).tolist()],[]))
         mean_oma_ens    = np.asarray(sum([mean_oma_ens.tolist(),   (anndataB['mean_oma_ens'][:][:]).tolist()],[]))
         spread_f        = np.asarray(sum([spread_f.tolist(),       (anndataB['spread_f'][:][:]).tolist()],[]))
         std_omf_ens     = np.asarray(sum([std_omf_ens.tolist(),    (anndataB['std_omf_ens'][:][:]).tolist()],[]))
         std_omf_ctrl    = np.asarray(sum([std_omf_ctrl.tolist(),   (anndataB['std_omf_ctrl'][:][:]).tolist()],[]))
         spread_obserr_f = np.asarray(sum([spread_obserr_f.tolist(),(anndataB['spread_obserr_f'][:][:]).tolist()],[]))
         spread_a        = np.asarray(sum([spread_a.tolist(),       (anndataB['spread_a'][:][:]).tolist()],[]))
         std_oma_ens     = np.asarray(sum([std_oma_ens.tolist(),    (anndataB['std_oma_ens'][:][:]).tolist()],[]))
         std_oma_ctrl    = np.asarray(sum([std_oma_ctrl.tolist(),   (anndataB['std_oma_ctrl'][:][:]).tolist()],[]))
         spread_obserr_a = np.asarray(sum([spread_obserr_a.tolist(),(anndataB['spread_obserr_a'][:][:]).tolist()],[]))
      nobs_all_plev[:,modct]        = nobs_all[dateindcs,plevindex]
      nobs_used_plev[:,modct]       = nobs_used[dateindcs,plevindex]
      mean_obs_all_plev[:,modct]    = mean_obs_all[dateindcs,plevindex]
      mean_obs_used_plev[:,modct]   = mean_obs_used[dateindcs,plevindex]
      mean_omf_ctrl_plev[:,modct]   = mean_omf_ctrl[dateindcs,plevindex]
      mean_omf_ens_plev[:,modct]    = mean_omf_ens[dateindcs,plevindex]
      mean_oma_ctrl_plev[:,modct]   = mean_oma_ctrl[dateindcs,plevindex]
      mean_oma_ens_plev[:,modct]    = mean_oma_ens[dateindcs,plevindex]
      spread_f_plev[:,modct]        = spread_f[dateindcs,plevindex]
      std_omf_ens_plev[:,modct]     = std_omf_ens[dateindcs,plevindex]
      std_omf_ctrl_plev[:,modct]    = std_omf_ctrl[dateindcs,plevindex]
      spread_obserr_f_plev[:,modct] = spread_obserr_f[dateindcs,plevindex]
      spread_a_plev[:,modct]        = spread_a[dateindcs,plevindex]
      std_oma_ens_plev[:,modct]     = std_oma_ens[dateindcs,plevindex]
      std_oma_ctrl_plev[:,modct]    = std_oma_ctrl[dateindcs,plevindex]
      spread_obserr_a_plev[:,modct] = spread_obserr_a[dateindcs,plevindex]
      modct += 1
   
   
   Ntotdiag=nobs_all_plev.astype(float)
   Nusediag=nobs_used_plev.astype(float)
   #Nbufr[Nbufr<0]=nan
   Ntotdiag[Ntotdiag<0]=nan
   Nusediag[Nusediag<0]=nan
   
   
   maxy=nan*np.ones(5)
   miny=nan*np.ones(5)
   
   
   ####################################################
   maxNt     = np.nanmax(Ntotdiag)
   maxNu     = np.nanmax(Nusediag)
   maxy[0]   = np.nanmax((maxNt,maxNu))
   
   maxdV     = np.nanmax(mean_obs_all_plev)
   maxuV     = np.nanmax(mean_obs_used_plev)
   maxy[1]   = np.nanmax((maxdV,maxuV))
   
   maxOF     = np.nanmax(mean_omf_ctrl_plev)
   maxOA     = np.nanmax(mean_oma_ctrl_plev)
   maxy[2]   = np.nanmax((maxOF,maxOA))
   
   maxFS     = np.nanmax(np.sqrt(spread_f_plev))
   maxFSE    = np.nanmax(spread_obserr_f_plev)
   maxOFEstd = np.nanmax(std_omf_ens_plev)
   maxOFstd  = np.nanmax(std_omf_ctrl_plev)
   maxy[3]   = np.nanmax((maxFS,maxOFEstd,maxOFstd))
   
   maxAS     = np.nanmax(np.sqrt(spread_a_plev))
   maxASE    = np.nanmax(spread_obserr_a_plev)
   maxOAEstd = np.nanmax(std_oma_ens_plev)
   maxOAstd  = np.nanmax(std_oma_ctrl_plev)
   maxy[4]   = maxOAstd
   ####################################################
   ####################################################
   minNt     = np.nanmin(Ntotdiag)
   minNu     = np.nanmin(Nusediag)
   miny[0]   = np.nanmin((minNt,minNu))
   
   mindV     = np.nanmin(mean_obs_all_plev)
   minuV     = np.nanmin(mean_obs_used_plev)
   miny[1]   = np.nanmin((mindV,minuV))
   
   minOF     = np.nanmin(mean_omf_ctrl_plev)
   minOA     = np.nanmin(mean_oma_ctrl_plev)
   miny[2]   = np.nanmin((minOF,minOA))
   
   minFS     = np.nanmin(np.sqrt(spread_f_plev))
   minFSE    = np.nanmin(spread_obserr_f_plev)
   minOFEstd = np.nanmin(std_omf_ens_plev)
   minOFstd  = np.nanmin(std_omf_ctrl_plev)
   miny[3]   = np.nanmin((minFS,minOFEstd,minOFstd))
   
   minAS     = np.nanmin(np.sqrt(spread_a_plev))
   minASE    = np.nanmin(spread_obserr_a_plev)
   minOAEstd = np.nanmin(std_oma_ens_plev)
   minOAstd  = np.nanmin(std_oma_ctrl_plev)
   miny[4]   = minOAstd
   ####################################################
   
   
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
   
   
      PLOTpath =plotpath
      os.system("mkdir -p "+PLOTpath)
      print 'plotpath=',PLOTpath
   
      figname=PLOTpath+'/'+model+'_CONV_'+varb+'_'+region+'_'+str(plevel)+'.png'
      ####
      zeroline=np.zeros(len(datetime_list))
      ####
   
      f, axarr = plt.subplots(5, sharex=True, figsize=(17, 17))#plt.subplots(figsize=(20, 10))
      ####
      diagmean= np.nanmean(Ntotdiag[:,modct])
      usemean= np.nanmean(Nusediag[:,modct])
   
      axarr[0].plot(datetime_list, Ntotdiag[:,modct],'c',datetime_list, Nusediag[:,modct],'r')
      if varb=='PS' or varb=='PW':
         f.suptitle(modelname+' CONVENTIONAL OBS '+varb+' '+geolabel+' ', fontsize=20, fontweight='bold')
      else:
         f.suptitle(modelname+' CONVENTIONAL OBS '+varb+' '+geolabel+' '+str(plevel)+'_mb to '+str(plevel+100)+'_mb', fontsize=20, fontweight='bold')
      axarr[0].set_ylabel('numobs')
   
      box = axarr[0].get_position()
      rangey=maxy[0]-miny[0]
      minax = miny[0] - .05*rangey
      maxax = maxy[0] + .05*rangey
      axarr[0].set_ylim((minax,maxax))
      del minax
      del maxax
      del rangey
      axarr[0].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[0].legend(( 'all DA obs, avg='+str(int(round(diagmean))), 'all DA use, avg='+str(int(round(usemean)))),loc='center left', bbox_to_anchor=(1.05, 0.5))
      axarr[0].grid(True)
      axarr[0].set_title('Number of Observations', fontsize=14, fontweight='bold')
      del diagmean
      del usemean
      ####            
      ax2 = axarr[0].twinx()
      ax2.plot(datetime_list, 100*Nusediag[:,modct]/Ntotdiag[:,modct],'g--', linewidth=3)
      ax2.set_ylabel('PERCENT', color='g')
      ax2.set_ylim((-5,105))
      for tl in ax2.get_yticklabels():
              tl.set_color('m')
   
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * 0.85, box.height])
      ax2.legend(('%DAuse/DAobs',), loc='lower left')
   
      ####
      ####
      diagmean= np.nanmean(mean_obs_all_plev[:,modct])
      usemean= np.nanmean(mean_obs_used_plev[:,modct])
   
      axarr[1].plot(datetime_list, mean_obs_all_plev[:,modct],'g', datetime_list, mean_obs_used_plev[:,modct],'m')
      axarr[1].set_ylabel('MEAN '+units)
      box = axarr[1].get_position()
      rangey=maxy[1]-miny[1]
      minax = miny[1] - .05*rangey
      maxax = maxy[1] + .05*rangey
      axarr[1].set_ylim((minax,maxax))
      del minax
      del maxax
      del rangey
      axarr[1].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[1].legend(('all DA obs, avg='+str(round(diagmean,2)), 'all DA used obs, avg='+str(round(usemean,2))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[1].grid(True)
      axarr[1].set_title('Mean '+varb+' observation', fontsize=14, fontweight='bold')
      del diagmean
      del usemean
      ####
      ####
      fcstmean= np.nanmean(mean_omf_ctrl_plev[:,modct])
      analmean= np.nanmean(mean_oma_ctrl_plev[:,modct])
   
      axarr[2].plot(datetime_list, mean_omf_ctrl_plev[:,modct],'r', datetime_list, mean_oma_ctrl_plev[:,modct],'g')
      axarr[2].set_ylabel('O-F, O-A mean '+units)
      box = axarr[2].get_position()
      rangey=maxy[2]-miny[2]
      minax = miny[2] - .05*rangey
      maxax = maxy[2] + .05*rangey
      axarr[2].set_ylim((minax,maxax))
      del minax
      del maxax
      del rangey
      axarr[2].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[2].legend(('O-F, avg='+str(round(fcstmean,2)), 'O-A, avg='+str(round(analmean,2))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[2].grid(True)
      axarr[2].plot(datetime_list, zeroline,'k--', linewidth=2)
      axarr[2].set_title('First Guess and Analysis Biases', fontsize=14, fontweight='bold')
      del fcstmean
      del analmean
      ####
      ####
      sprdmean= np.nanmean(spread_f_plev[:,modct])
      sprderrmean= np.nanmean(spread_obserr_f_plev[:,modct])
      ensstdmean= np.nanmean(std_omf_ens_plev[:,modct])
      fcststdmean= np.nanmean(std_omf_ctrl_plev[:,modct])
   
      axarr[3].plot( datetime_list, np.sqrt(spread_f_plev[:,modct]),'m',datetime_list, std_omf_ens_plev[:,modct],'k',datetime_list, std_omf_ctrl_plev[:,modct],'r')
      axarr[3].set_ylabel('O-F '+units)
      box = axarr[3].get_position()
      rangey=maxy[3]-miny[3]
      minax = miny[3] - .05*rangey
      maxax = maxy[3] + .05*rangey
      axarr[3].set_ylim((minax,maxax))
      del minax
      del maxax
      del rangey
      axarr[3].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[3].legend(('ensspread F, avg='+str(round(sprdmean,3)), 'ens O-F std, avg='+str(round(ensstdmean,3)),'control O-F std, avg='+str(round(fcststdmean,3))),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[3].grid(True)
      axarr[3].set_title('First Guess spread and errors', fontsize=14, fontweight='bold')
   
      del sprdmean
      del sprderrmean
      del ensstdmean
      del fcststdmean
      ####
      sprdmean= np.nanmean(spread_a_plev[:,modct])
      sprderrmean= np.nanmean(spread_obserr_a_plev[:,modct])
      ensstdmean= np.nanmean(std_oma_ens_plev[:,modct])
      analstdmean= np.nanmean(std_oma_ctrl_plev[:,modct])
   
      axarr[4].plot( datetime_list, std_oma_ctrl_plev[:,modct],'r')
      axarr[4].set_ylabel('O-A '+units)
      box = axarr[4].get_position()
      rangey=maxy[4]-miny[4]
      minax = miny[4] - .05*rangey
      maxax = maxy[4] + .05*rangey
      axarr[4].set_ylim((minax,maxax))
      del minax
      del maxax
      del rangey
      axarr[4].set_position([box.x0, box.y0, box.width * 0.85, box.height])
      axarr[4].legend(( 'control O-A std, avg='+str(round(analstdmean,3)),''),loc='center left', bbox_to_anchor=(1, 0.5))
      axarr[4].grid(True)
      axarr[4].set_title('Analysis spread and errors', fontsize=14, fontweight='bold')
      del sprdmean
      del sprderrmean
      del ensstdmean
      del analstdmean
      ####
      axarr[4].xaxis.set_major_locator(locator)
      axarr[4].xaxis.set_major_formatter(tick_format)
      for tick in axarr[4].get_xticklabels():
          tick.set_rotation(70)
   
      print('figname=',figname)
      plt.savefig(figname)
      del modelname
      del PLOTpath






