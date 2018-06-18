import numpy as np
from netCDF4 import Dataset

nan=float('nan')


### begindate and enddate are 10 digits

#def plot_all_RAD( modelstreams, begindate, enddate, instrmnt, satlite, channel, region):
##modelfile='/Projects/gefsrr/ANNUAL/RAD_FV3s2003_2003_amsua_n16_GLOBL.nc'

channel=6
modelstreams=('FV3s2003','CFSR')
nummodel=len(modelstreams)
########

datapath='/Projects/gefsrr/ANNUAL/'
modelstream='FV3s2003'
instrmnt='amsua'
satlite='n16'
region='GLOBL'
begindate=2003040500
enddate=2003040900
#enddate=2004040900
#################################
#################################
#file_yrs[0]=str(begindate)[0:4]
#file_yrs[1]=str(enddate)[0:4]
##############################
## consider re-writing this to make all of the 
##############################

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
   dateindcs=np.arange(startindx,endindx+1,1).tolist()
   querydates=[]
   for di in dateindcs:
      querydates.append(alldatesA[di])
   #querydates=alldatesA[startindx:endindx+1]
   numquerydates=len(querydates)
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
   dateindcs = sum([dateindcsA,dateindcsB],[])
   querydates = sum([querydatesA, querydatesB],[])
   numquerydates = len(querydates)










for yy in range(numyearfiles):
   modelfile[yy]=datapath+'RAD_'+modelstream+'_'+str(beginyr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'







chans = anndataA.variables['Channels'][:].tolist()
#chanindx=np.nonzero(np.abs(chans)==channel)[0].tolist()
chanindx=chans.index(channel)
dateindcs=list(range(300))
dateindcs=dateindcs+200*np.ones(len(dateindcs))
dateindcs=map(int,dateindcs.tolist()[:])
modct=0
numquerydates=len(dateindcs)
nummodel=2







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
   for m in range(numyearfiles):
   modelfile=datapath+'/RAD_'+modelstream+'_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'

   anndata = Dataset(modelfile, 'a')
   chans = anndata['Channels'][:].tolist()
   chanindx=chans.index(channel)


   nobs_all = anndata['nobs_all'][:][:]
   nobs_qcd = anndata['nobs_qcd'][:][:]
   nobs_used = anndata['nobs_used'][:][:]
   mean_obs_all = anndata['mean_obs_all'][:][:]
   mean_obs_used = anndata['mean_obs_used'][:][:]
   mean_obs_qcd = anndata['mean_obs_qcd'][:][:]
   mean_omf_ctrl = anndata['mean_omf_ctrl'][:][:]
   mean_oma_ctrl = anndata['mean_oma_ctrl'][:][:]
   std_omf_ctrl = anndata['std_omf_ctrl'][:][:]
   std_oma_ctrl = anndata['std_oma_ctrl'][:][:]
   mean_omf_ens = anndata['mean_omf_ens'][:][:]
   spread_f = anndata['spread_f'][:][:]
   spread_obserr_f = anndata['spread_obserr_f'][:][:]
   std_omf_ens = anndata['std_omf_ens'][:][:]
   mean_biascor = anndata['mean_biascor'][:][:]
   std_biascor = anndata['std_biascor'][:][:]


   nobs_all_chan[:,modct]        = nobs_all[dateindcs,chanindx]
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
maxNuse =np.nanmax(numobs_use);         minNuse  =np.nanmin(numobs_use);         rangeNuse = maxNuse-minNuse

maxTd=np.nanmax(mean_obs_all_chan);     minTd=np.nanmin(mean_obs_all_chan);
maxTu=np.nanmax(mean_obs_used_chan);    minTu=np.nanmin(mean_obs_used_chan);
maxTq=maxTu;                            minTq=minTu;

maxBCavg=np.nanmax(mean_biascor_chan);  minBCavg=np.nanmin(mean_biascor_chan);
maxBCstd=np.nanmax(std_biascor_chan);   minBCstd=np.nanmin(std_biascor_chan);

#maxOmFnoBCmean=np.nanmax(OmF_noBC_mean);        minOmFnoBCmean=np.nanmin(OmF_noBC_mean);
maxOmF_wBCmean=np.nanmax(mean_omf_ctrl_chan);         minOmF_wBCmean=np.nanmin(mean_omf_ctrl_chan);
#maxOmFnoBCstd =np.nanmax(OmF_noBC_std);         minOmFnoBCstd =np.nanmin(OmF_noBC_std);
maxOmF_wBCstd =np.nanmax(std_omf_ctrl_chan);          minOmF_wBCstd =np.nanmin(std_omf_ctrl_chan);
#maxOmAnoBCmean=np.nanmax(OmA_noBC_mean);        minOmAnoBCmean=np.nanmin(OmA_noBC_mean);
maxOmA_wBCmean=np.nanmax(mean_oma_ctrl_chan);         minOmA_wBCmean=np.nanmin(mean_oma_ctrl_chan);
#maxOmAnoBCstd =np.nanmax(OmA_noBC_std);         minOmAnoBCstd =np.nanmin(OmA_noBC_std);
maxOmA_wBCstd =np.nanmax(std_oma_ctrl_chan);          minOmA_wBCstd =np.nanmin(std_oma_ctrl_chan);

#maxENS_OmA_wBC_std   =np.nanmax(ENS_OmA_wBC_std);       minENS_OmA_wBC_std  =np.nanmin(ENS_OmA_wBC_std);
#maxENSspredA_mean    =np.nanmax(ENSspredA_mean);        minENSspredA_mean   =np.nanmin(ENSspredA_mean);
#maxENSsprederrA_mean =np.nanmax(ENSsprederrA_mean);     minENSsprederrA_mean=np.nanmin(ENSsprederrA_mean);
maxENS_OmF_wBC_std   =np.nanmax(std_omf_ens_chan);         minENS_OmF_wBC_std  =np.nanmin(std_omf_ens_chan);
maxENSspredF_mean    =np.nanmax(spread_f_chan);            minENSspredF_mean   =np.nanmin(spread_f_chan);
maxENSsprederrF_mean =np.nanmax(spread_obserr_f_chan);     minENSsprederrF_mean=np.nanmin(spread_obserr_f_chan);






