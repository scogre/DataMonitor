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

### begindate and enddate are 10 digits
##modelfile='/Projects/gefsrr/ANNUAL/CONV_t_FV3s2007_2007_GLOBL.nc'
#### plev=0 means between zero and 100
## def plot_all_CONV( modelstreams, begindate, enddate, varb, plevel, region):
#modelstreams=('FV3s2003','CFSR')
modelstreams=('FV3s2003','FV3s2003')
nummodel=len(modelstreams)
########
datapath='/Projects/gefsrr/ANNUAL/'
plotpath=datapath
varb='t'
plevel=800
region='GLOBL'
begindate=2003030300
enddate=2003040900
##############################
#/Projects/gefsrr/ANNUAL/CONV_t_FV3s2003_2003_GLOBL.nc
##############################


##############################
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
#All_Dates(Ncycles) ;
#Full_Dates(Ncycles) ;
#Plevels(Nlevs) ;

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











Ntotdiag=Ntotdiag.astype(float)
Nusediag=Nusediag.astype(float)
#Nbufr[Nbufr<0]=nan
Ntotdiag[Ntotdiag<0]=nan
Nusediag[Nusediag<0]=nan

maxy=nan*np.ones(5)
miny=nan*np.ones(5)

####################################################
#maxNb     = np.nanmax(Nbufr)
maxNt     = np.nanmax(Ntotdiag)
maxNu     = np.nanmax(Nusediag)
#maxy[0]   = np.nanmax((maxNb,maxNt,maxNu))
maxy[0]   = np.nanmax((maxNt,maxNu))

#maxbV     = np.nanmax(bufr_avg)
maxdV     = np.nanmax(diagavg_obs)
maxuV     = np.nanmax(diagavg_use_obs)
#maxy[1]   = np.nanmax((maxbV,maxdV,maxuV))
maxy[1]   = np.nanmax((maxdV,maxuV))

maxOF     = np.nanmax(OmF_avg)
maxOA     = np.nanmax(OmA_avg)
maxy[2]   = np.nanmax((maxOF,maxOA))

maxFS     = np.nanmax(np.sqrt(Fsprd_avg))
maxFSE    = np.nanmax(Fsprderr_avg)
maxOFEstd = np.nanmax(OmFens_std)
maxOFstd  = np.nanmax(OmF_std)
#maxy[3]   = np.nanmax((maxFS,maxFSE,maxOFEstd,maxOFstd))
maxy[3]   = np.nanmax((maxFS,maxOFEstd,maxOFstd))

maxAS     = np.nanmax(np.sqrt(Asprd_avg))
maxASE    = np.nanmax(Asprderr_avg)
maxOAEstd = np.nanmax(OmAens_std)
maxOAstd  = np.nanmax(OmA_std)
#maxy[4]   = np.nanmax((maxAS,maxASE,maxOAEstd,maxOAstd))
maxy[4]   = maxOAstd
####################################################
####################################################
#minNb     = np.nanmin(Nbufr)
minNt     = np.nanmin(Ntotdiag)
minNu     = np.nanmin(Nusediag)
#miny[0]   = np.nanmin((minNb,minNt,minNu))
miny[0]   = np.nanmin((minNt,minNu))

#minbV     = np.nanmin(bufr_avg)
mindV     = np.nanmin(diagavg_obs)
minuV     = np.nanmin(diagavg_use_obs)
#miny[1]   = np.nanmin((minbV,mindV,minuV))
miny[1]   = np.nanmin((mindV,minuV))

minOF     = np.nanmin(OmF_avg)
minOA     = np.nanmin(OmA_avg)
miny[2]   = np.nanmin((minOF,minOA))

minFS     = np.nanmin(np.sqrt(Fsprd_avg))
minFSE    = np.nanmin(Fsprderr_avg)
minOFEstd = np.nanmin(OmFens_std)
minOFstd  = np.nanmin(OmF_std)
#miny[3]   = np.nanmin((minFS,minFSE,minOFEstd,minOFstd))
miny[3]   = np.nanmin((minFS,minOFEstd,minOFstd))

minAS     = np.nanmin(np.sqrt(Asprd_avg))
minASE    = np.nanmin(Asprderr_avg)
minOAEstd = np.nanmin(OmAens_std)
minOAstd  = np.nanmin(OmA_std)
#miny[4]   = np.nanmin((minAS,minASE,minOAEstd,minOAstd))
miny[4]   = minOAstd
####################################################





