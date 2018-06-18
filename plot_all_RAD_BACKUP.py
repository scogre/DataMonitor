import numpy as np
from netCDF4 import Dataset
nan=float('nan')
### begindate and enddate are 10 digits
#def plot_all_RAD( modelstreams, begindate, enddate, instrmnt, satlite, channel, region):
##modelfile='/Projects/gefsrr/ANNUAL/RAD_FV3s2003_2003_amsua_n16_GLOBL.nc'
channel=6
#modelstreams=('FV3s2003','CFSR')
#modelstreams=('FV3s2003')
modelstreams=('FV3s2003','FV3s2003')
nummodel=len(modelstreams)
########
datapath='/Projects/gefsrr/ANNUAL/'
#modelstream='FV3s2003'
instrmnt='amsua'
satlite='n16'
region='GLOBL'
#begindate=2003122500
#enddate=2004010500
begindate=2003040500
enddate=2003040900
##############################
modelstream=modelstreams[1]
beginyr=str(begindate)[0:4]
endyr=str(enddate)[0:4]
if beginyr==endyr:
   numyearfiles=1
   modelfile=['']*numyearfiles
   modelfile[0]=datapath+'RAD_'+modelstream+'_'+str(beginyr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
   print('model=',modelfile[0])
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
      modelfile==datapath+'RAD_'+modelstream+'_'+str(endyr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
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
maxNqc  =np.nanmax(nobs_qcd_chan);      minNqc   =np.nanmin(nobs_qcd_chan);      rangeNqc = maxNqc-minNqc
maxNuse =np.nanmax(nobs_used_chan);     minNuse  =np.nanmin(nobs_used_chan);         rangeNuse = maxNuse-minNuse

maxTd=np.nanmax(mean_obs_all_chan);     minTd=np.nanmin(mean_obs_all_chan);
maxTu=np.nanmax(mean_obs_used_chan);    minTu=np.nanmin(mean_obs_used_chan);
maxTq=maxTu;                            minTq=minTu;

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




