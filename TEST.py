#!/usr/local/bin/python2.7
import numpy as np
from netCDF4 import Dataset
import datetime
#from datetime import date
import time
from datetime import datetime, date, time
from datetime import timedelta
import sys, os, os.path, cgi, re
import matplotlib as mpl
mpl.use('Agg') #for web 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter, DayLocator, HourLocator, AutoDateLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from matplotlib.ticker import LinearLocator
import sys
#from ncepbufr import satellite_names as code2sat_name
import string
import _tkinter

import subprocess

#### data path /Projects/gefsrr
############## make random directory name################
############## make random directory name################
import random, string
length=10
randdir=''.join(random.choice(string.lowercase) for i in range(length))
tmpdir='/httpd-test/psd/tmp/gefsrr_data_assim/'
#tmpdir='/psd/tmp/gefsrr_data_assim/'
writedir=tmpdir+randdir+'/'
imagedir=writedir+'images/'
os.system("mkdir -p "+writedir)
os.system("mkdir -p "+imagedir)
########################################################

docroot = sys.path[0]
form = cgi.FieldStorage()

enddate_nohr = form['fcstdate'].value
enddate=str(enddate_nohr)+'00'
windowlen = form['windowlen'].value
geo = form['geo'].value
channel = form['channel'].value
#modelstream = form['stream'].value
#modelstream = 'FV3s1999'
####################
tempdates_filename = writedir+'/temp_dates.txt'
plotpath = imagedir

accumdatapath = plotpath
######################
######################
#######################################################################################
nan=float('nan')
##################
##################

streamy1 = form['streamy1'].value
streamy2 = form['streamy2'].value
####################

#models = [('FV3s'+str(streamy1)), ('FV3s'+str(streamy2))]
models = [(str(streamy1)), (str(streamy2))]
listjunk_filename=writedir+models[0]+'_models'
text_file = open(listjunk_filename, "w")
text_file.write(models[0]+' models \n')
text_file.close()

listjunk_filename=writedir+'stream'
text_file = open(listjunk_filename, "w")
text_file.write(str(streamy1)+' streamy1 \n')
text_file.close()

nummodel=len(models)
###########################

listjunk_filename=tempdates_filename + '_junklistA'
text_file = open(listjunk_filename, "w")
text_file.write(str(channel)+' channel \n')
text_file.close()


tperday=4
hourincrmnt=24/tperday

ndates= int(tperday)*int(windowlen)

date_list=[]

yrend=enddate[0:4]
moend=enddate[4:6]
daend=enddate[6:8]
hrend=enddate[8:10]
endtime=datetime(int(yrend), int(moend), int(daend), int(hrend),0,0)
delta=timedelta(hours=int(hourincrmnt))

dayspan=timedelta(days=int(windowlen))
starttime=endtime-dayspan

tempdate=starttime

for n in range(ndates):
    tempdate = tempdate + delta
    date_list.append(tempdate.strftime('%Y%m%d%H'))
del tempdate

###########################################################
startdate=date_list[0]
###########################################################
temp_accumdatafile= accumdatapath+'AMSUA_ACCUM_'+geo+'_'+startdate+'_'+enddate+'.nc'
###########################################################

startdate_nohour = startdate[0:8]
startdate_hour = startdate[8:10]
startdate_year = startdate[0:4]
startdate_mo = startdate[4:6]
startdate_da = startdate[6:8]
startdate_yrmoda = startdate_year+'-'+startdate_mo+'-'+startdate_da

yeardiff= int(yrend)-int(startdate_year)
total_nummonths = int(moend) + 12 * yeardiff - int(startdate_mo)+1
###########################################################



listjunk_filename=tempdates_filename + '_junklistB'
text_file = open(listjunk_filename, "w")
text_file.write(str(channel)+' channel \n')
text_file.close()








numobs_tot=nan*np.ones((ndates,nummodel))
numobs_diag=nan*np.ones((ndates,nummodel))
numobs_use=nan*np.ones((ndates,nummodel))
numobs_qc=nan*np.ones((ndates,nummodel))
Tmean_allbufr=nan*np.ones((ndates,nummodel))
Tmean_alldiag=nan*np.ones((ndates,nummodel))
Tmean_use=nan*np.ones((ndates,nummodel))
Tmean_qc=nan*np.ones((ndates,nummodel))
Biascorr_mean=nan*np.ones((ndates,nummodel))
Biascorr_std=nan*np.ones((ndates,nummodel))
OmF_noBC_mean=nan*np.ones((ndates,nummodel))
OmF_wBC_mean=nan*np.ones((ndates,nummodel))
OmF_noBC_std=nan*np.ones((ndates,nummodel))
OmF_wBC_std=nan*np.ones((ndates,nummodel))

OmA_noBC_mean=nan*np.ones((ndates,nummodel))
OmA_wBC_mean=nan*np.ones((ndates,nummodel))
OmA_noBC_std=nan*np.ones((ndates,nummodel))
OmA_wBC_std=nan*np.ones((ndates,nummodel))

ENS_OmA_wBC_std=nan*np.ones((ndates,nummodel))
ENSspredA_mean=nan*np.ones((ndates,nummodel))
ENSsprederrA_mean=nan*np.ones((ndates,nummodel))
ENS_OmF_wBC_std=nan*np.ones((ndates,nummodel))
ENSspredF_mean=nan*np.ones((ndates,nummodel))
ENSsprederrF_mean=nan*np.ones((ndates,nummodel))




listjunk_filename=tempdates_filename + '_junklistC'
text_file = open(listjunk_filename, "w")
text_file.write(str(channel)+' channel \n')
text_file.close()







chanindx=int(channel)-1

countline=0





listjunk_filename=tempdates_filename + '_junklistD'
text_file = open(listjunk_filename, "w")
text_file.write(str(channel)+' channel \n')
text_file.close()


for modct in range(nummodel):
        model=models[modct]

#        listjunk_filename=tempdates_filename + '_junklist_'+model
#        text_file = open(listjunk_filename, "w")
#        text_file.write(str(nummodel)+' nummodel \n')
#        text_file.write( model+' model \n')
#        text_file.close()



        path2data='/Projects/gefsrr/amsu_plotdata_'+model+'/'
        #path2data='/Users/sgregory/Documents/NOAA/Data_Assimilation/Git_clone/py-ncepbufr-SG/moveSGmerge/amsu_plotdata/'+model+'sample/'

        monfiles=[]

        currmo = startdate_mo
        currmonum = int(currmo)
        curryr = startdate_year
        curryrnum = int(curryr)
        for n in range(total_nummonths):
                tempdate= curryr + currmo + '01'
                currmonum2DIG = currmo
                monfiles.append(path2data + 'AMSU_'+curryr+'_'+currmonum2DIG+'_'+geo+'.nc')
                #monACCUM_file= path2data + 'AMSU_'+curryr+'_'+currmonum2DIG+'_'+geo+'.nc'
                currmonum = currmonum+1
                if currmonum>12:
                        curryrnum = curryrnum+1
                        curryr = str(curryrnum)
                        currmonum = currmonum-12
                currmo = str(currmonum)
                if currmonum<10:
                        currmo='0'+currmo
        ######################################################################################################################
        georegion = '_'+geo
        accumplotdata_nc = temp_accumdatafile
        ######################################################################################################################
        ######################################################################################################################
        querydates = date_list
        numquerydates=len(querydates)
        querydatesnum=np.empty(numquerydates)
        for m in range(numquerydates):
            querydatesnum[m]=int(querydates[m])

        ####################################
        accum_date =  np.empty(numquerydates)
        ####################################

#        listjunk_filename=tempdates_filename + '_junklist_'+model
#        text_file = open(listjunk_filename, "w")
#        text_file.write(str(nummodel)+' nummodel \n')
#        text_file.write( model+' model \n')
#        text_file.close()

       
        listmonths=monfiles
        for mm in range(len(listmonths)):
                filename=listmonths[mm]
                #print 'filename=', filename
                listjunk_filename=tempdates_filename + '_junklist_AAAA_'+model
                text_file = open(listjunk_filename, "w")
                text_file.write(str(nummodel)+' nummodel \n')
                text_file.write(filename+' filename \n')
                text_file.write( model+' model \n')
                text_file.close()


                countline=countline+1
                month_nc = Dataset(filename,'r')
                


		listjunk_filename=tempdates_filename + '_junklist_CCCC_'+model
                text_file = open(listjunk_filename, "w")
                text_file.write(str(nummodel)+' nummodel \n')
                text_file.write(filename+' filename \n')
                text_file.write( model+' model \n')
                text_file.close()

                month_DATES           = month_nc.variables['DATES'][:]
                listjunk_filename=tempdates_filename + '_junklist_DDDD_'+model
                text_file = open(listjunk_filename, "w")
                text_file.write(str(nummodel)+' nummodel \n')
                text_file.write(filename+' filename \n')
                text_file.write( model+' model \n')
                text_file.close()

                nummondates=len(month_DATES)
                month_IDsat           = month_nc.variables['IDsat'][:]
                month_CHANnum         = month_nc.variables['CHANnum'][:][:]
                month_dumdata         = month_nc.variables['numobs_tot'][:][:]
                chans=np.unique(month_CHANnum)
                nchan=len(chans)
                sats=np.unique(month_IDsat)
                nsats=len(sats)


                if countline==1:
        #               ## initialize the array shapes
                        accum_numobs_tot         = nan*np.ones((numquerydates,nummodel))
                        accum_numobs_diag        = nan*np.ones((numquerydates,nummodel))
                        accum_numobs_use         = nan*np.ones((numquerydates,nummodel))
                        accum_numobs_qc          = nan*np.ones((numquerydates,nummodel))
                        accum_Tmean_allbufr      = nan*np.ones((numquerydates,nummodel))
                        accum_Tmean_alldiag      = nan*np.ones((numquerydates,nummodel))
                        accum_Tmean_use          = nan*np.ones((numquerydates,nummodel))
                        accum_Tmean_qc           = nan*np.ones((numquerydates,nummodel))
                        accum_Biascorr_mean      = nan*np.ones((numquerydates,nummodel))
                        accum_Biascorr_std       = nan*np.ones((numquerydates,nummodel))
                        accum_OmF_noBC_mean      = nan*np.ones((numquerydates,nummodel))
                        accum_OmF_wBC_mean       = nan*np.ones((numquerydates,nummodel))
                        accum_OmF_noBC_std       = nan*np.ones((numquerydates,nummodel))
                        accum_OmF_wBC_std        = nan*np.ones((numquerydates,nummodel))

                        accum_OmA_noBC_mean      = nan*np.ones((numquerydates,nummodel))
                        accum_OmA_wBC_mean       = nan*np.ones((numquerydates,nummodel))
                        accum_OmA_noBC_std       = nan*np.ones((numquerydates,nummodel))
                        accum_OmA_wBC_std        = nan*np.ones((numquerydates,nummodel))

                        accum_ENS_OmA_wBC_std    = nan*np.ones((numquerydates,nummodel))
                        accum_ENSspredA_mean     = nan*np.ones((numquerydates,nummodel))
                        accum_ENSsprederrA_mean  = nan*np.ones((numquerydates,nummodel))
                        accum_ENS_OmF_wBC_std    = nan*np.ones((numquerydates,nummodel))
                        accum_ENSspredF_mean     = nan*np.ones((numquerydates,nummodel))
                        accum_ENSsprederrF_mean  = nan*np.ones((numquerydates,nummodel))

                        accum_IDsat              = nan*np.ones((numquerydates,nsats))
                        accum_CHANnum            = nan*np.ones((numquerydates,nummodel))
                        accum_date               = nan*np.ones(numquerydates)
                ############
                for m in range(numquerydates):
                        querydate=int(querydatesnum[m])
                        dateindx = np.nonzero(querydate == month_DATES)[0]
                        accum_date[m]                   =  querydatesnum[m]
                        if len(dateindx)>0:
                                accum_numobs_tot[m][modct]          = month_nc.variables['numobs_tot'][dateindx[0]][chanindx]
                                accum_numobs_diag[m][modct]         = month_nc.variables['numobs_diag'][dateindx[0]][chanindx]
                                accum_numobs_use[m][modct]          = month_nc.variables['numobs_use'][dateindx[0]][chanindx]
                                accum_numobs_qc[m][modct]           = month_nc.variables['numobs_qc'][dateindx[0]][chanindx]
                                accum_Tmean_allbufr[m][modct]       = month_nc.variables['Tmean_allbufr'][dateindx[0]][chanindx]
                                accum_Tmean_alldiag[m][modct]       = month_nc.variables['Tmean_alldiag'][dateindx[0]][chanindx]
                                accum_Tmean_use[m][modct]           = month_nc.variables['Tmean_use'][dateindx[0]][chanindx]
                                accum_Tmean_qc[m][modct]            = month_nc.variables['Tmean_qc'][dateindx[0]][chanindx]
                                accum_Biascorr_mean[m][modct]       = month_nc.variables['Biascorr_mean'][dateindx[0]][chanindx]
                                accum_Biascorr_std[m][modct]        = month_nc.variables['Biascorr_std'][dateindx[0]][chanindx]
                                accum_OmF_noBC_mean[m][modct]       = month_nc.variables['OmF_noBC_mean'][dateindx[0]][chanindx]
                                accum_OmF_wBC_mean[m][modct]        = month_nc.variables['OmF_wBC_mean'][dateindx[0]][chanindx]
                                accum_OmF_noBC_std[m][modct]        = month_nc.variables['OmF_noBC_std'][dateindx[0]][chanindx]
                                accum_OmF_wBC_std[m][modct]         = month_nc.variables['OmF_wBC_std'][dateindx[0]][chanindx]

                                accum_OmA_noBC_mean[m][modct]       = month_nc.variables['OmA_noBC_mean'][dateindx[0]][chanindx]
                                accum_OmA_wBC_mean[m][modct]        = month_nc.variables['OmA_wBC_mean'][dateindx[0]][chanindx]
                                accum_OmA_noBC_std[m][modct]        = month_nc.variables['OmA_noBC_std'][dateindx[0]][chanindx]
                                accum_OmA_wBC_std[m][modct]         = month_nc.variables['OmA_wBC_std'][dateindx[0]][chanindx]

                                accum_ENS_OmA_wBC_std[m][modct]     = month_nc.variables['ENS_OmA_wBC_std'][dateindx[0]][chanindx]
                                accum_ENSspredA_mean[m][modct]      = month_nc.variables['ENSspredA_mean'][dateindx[0]][chanindx]
                                accum_ENSsprederrA_mean[m][modct]   = month_nc.variables['ENSsprederrA_mean'][dateindx[0]][chanindx]
                                accum_ENS_OmF_wBC_std[m][modct]     = month_nc.variables['ENS_OmF_wBC_std'][dateindx[0]][chanindx]
                                accum_ENSspredF_mean[m][modct]      = month_nc.variables['ENSspredF_mean'][dateindx[0]][chanindx]
                                accum_ENSsprederrF_mean[m][modct]   = month_nc.variables['ENSsprederrF_mean'][dateindx[0]][chanindx]

                                accum_IDsat[m][:]                   = month_nc.variables['IDsat'][dateindx[0]][0]
                                accum_CHANnum[m][modct]             = month_nc.variables['CHANnum'][dateindx[0]][chanindx]

                        del dateindx
        month_nc.close()
#####################
datajunk_filename=tempdates_filename + '_DATA'
data_file = open(datajunk_filename, "w")
data_file.write(str(accum_Tmean_alldiag))
data_file.close()
#####################
numobs_tot        = accum_numobs_tot;
numobs_diag       = accum_numobs_diag;
numobs_use        = accum_numobs_use;
numobs_qc         = accum_numobs_qc;
Tmean_allbufr     = accum_Tmean_allbufr;
Tmean_alldiag     = accum_Tmean_alldiag;
Tmean_use         = accum_Tmean_use;
Tmean_qc          = accum_Tmean_qc;
Biascorr_mean     = accum_Biascorr_mean;
Biascorr_std      = accum_Biascorr_std;
OmF_noBC_mean     = accum_OmF_noBC_mean;
OmF_wBC_mean      = accum_OmF_wBC_mean;
OmF_noBC_std      = accum_OmF_noBC_std;
OmF_wBC_std       = accum_OmF_wBC_std;

OmA_noBC_mean     = accum_OmA_noBC_mean;
OmA_wBC_mean      = accum_OmA_wBC_mean;
OmA_noBC_std      = accum_OmA_noBC_std;
OmA_wBC_std       = accum_OmA_wBC_std;

ENS_OmA_wBC_std   = accum_ENS_OmA_wBC_std;
ENSspredA_mean    = accum_ENSspredA_mean;
ENSsprederrA_mean = accum_ENSsprederrA_mean;
ENS_OmF_wBC_std   = accum_ENS_OmF_wBC_std;
ENSspredF_mean    = accum_ENSspredF_mean;
ENSsprederrF_mean = accum_ENSsprederrF_mean;

IDsat = accum_IDsat
CHANnum = accum_CHANnum
DATES = accum_date


        ######### PLOTTING
maxNtot =np.nanmax(numobs_tot);     minNtot  =np.nanmin(numobs_tot);      rangeNtot = maxNtot-minNtot
maxNdiag=np.nanmax(numobs_diag);    minNdiag =np.nanmin(numobs_diag);     rangeNdiag = maxNdiag-minNdiag
maxNuse =np.nanmax(numobs_use);     minNuse  =np.nanmin(numobs_use);      rangeNuse = maxNuse-minNuse
maxNqc  =np.nanmax(numobs_qc);      minNqc   =np.nanmin(numobs_qc);       rangeNqc = maxNqc-minNqc

#maxTb=np.nanmax(Tmean_allbufr);     minTb=np.nanmin(Tmean_allbufr);
maxTd=np.nanmax(Tmean_alldiag);     minTd=np.nanmin(Tmean_alldiag);
maxTu=np.nanmax(Tmean_use);         minTu=np.nanmin(Tmean_use);
maxTq=np.nanmax(Tmean_qc);          minTq=np.nanmin(Tmean_qc); 

maxBCavg=np.nanmax(Biascorr_mean);  minBCavg=np.nanmin(Biascorr_mean); 
maxBCstd=np.nanmax(Biascorr_std);   minBCstd=np.nanmin(Biascorr_std);   

maxOmFnoBCmean=np.nanmax(OmF_noBC_mean);        minOmFnoBCmean=np.nanmin(OmF_noBC_mean);   
maxOmF_wBCmean=np.nanmax(OmF_wBC_mean);         minOmF_wBCmean=np.nanmin(OmF_wBC_mean);     
maxOmFnoBCstd =np.nanmax(OmF_noBC_std);         minOmFnoBCstd =np.nanmin(OmF_noBC_std);     
maxOmF_wBCstd =np.nanmax(OmF_wBC_std);          minOmF_wBCstd =np.nanmin(OmF_wBC_std);        

maxOmAnoBCmean=np.nanmax(OmA_noBC_mean);        minOmAnoBCmean=np.nanmin(OmA_noBC_mean);   
maxOmA_wBCmean=np.nanmax(OmA_wBC_mean);         minOmA_wBCmean=np.nanmin(OmA_wBC_mean);     
maxOmAnoBCstd =np.nanmax(OmA_noBC_std);         minOmAnoBCstd =np.nanmin(OmA_noBC_std);     
maxOmA_wBCstd =np.nanmax(OmA_wBC_std);          minOmA_wBCstd =np.nanmin(OmA_wBC_std);        

maxENS_OmA_wBC_std   =np.nanmax(ENS_OmA_wBC_std);       minENS_OmA_wBC_std  =np.nanmin(ENS_OmA_wBC_std); 
maxENSspredA_mean    =np.nanmax(ENSspredA_mean);        minENSspredA_mean   =np.nanmin(ENSspredA_mean);   
maxENSsprederrA_mean =np.nanmax(ENSsprederrA_mean);     minENSsprederrA_mean=np.nanmin(ENSsprederrA_mean);  
maxENS_OmF_wBC_std   =np.nanmax(ENS_OmF_wBC_std);       minENS_OmF_wBC_std  =np.nanmin(ENS_OmF_wBC_std);  
maxENSspredF_mean    =np.nanmax(ENSspredF_mean);        minENSspredF_mean   =np.nanmin(ENSspredF_mean);    
maxENSsprederrF_mean =np.nanmax(ENSsprederrF_mean);     minENSsprederrF_mean=np.nanmin(ENSsprederrF_mean); 



for modct in range(nummodel):
        model=models[modct]

        ######### PLOTTING

        listjunk_filename=tempdates_filename + '_junklistNEW'
        text_file = open(listjunk_filename, "w")
        text_file.write(str(nummodel)+' nummodel \n')
        text_file.write( model+' model \n')
        text_file.close()



        punct=string.punctuation
        space=' '
        hyphen='-'
        digits=string.digits


        accumplotdata_nc = accumplotdata_nc
        modelname = model

        accumDATEbounds = re.findall(r'_(\d{10})', accumplotdata_nc) #finds ten digit number in the string preceded by underscore
        if accumplotdata_nc.find('SOUTH')>=0:
                geolabelfilename='SOUTH'
                geolabel='Southern Hemisphere'
        elif accumplotdata_nc.find('TROPI')>=0:
                geolabelfilename='TROPI'
                geolabel='Tropical +/-20deg'
        elif accumplotdata_nc.find('NORTH')>=0:
                geolabelfilename='NORTH'
                geolabel='Northern Hemisphere'
        elif accumplotdata_nc.find('GLOBL')>=0:
                geolabelfilename='GLOBL'
                geolabel='Global'
        else:
                geolabelfilename=''
                geolabel=''

        #ndates = len(DATES)
        nrows = numobs_tot.shape[0]
        nsats = nrows/ndates
        nchan = numobs_tot.shape[1]

        yr=np.empty(ndates)
        mo=np.empty(ndates)
        da=np.empty(ndates)
        hr=np.empty(ndates)
        datetime_list=[]
        date_list_4plot=[]


        ##############
        for n in range(ndates):
                DATEstring=str(DATES[n])
                #print 'datestring=', DATEstring
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



        font = {'serif' : 'normal','weight' : 'bold','size'   : 12}
        mpl.rc('font', **font)
        mpl.rc('axes',titlesize=18)
        mpl.rc('legend', fontsize=12)


        #print('mo da hr=', mo, da, hr)
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


        PLOTpath = accumplotdata_nc[0:accumplotdata_nc.rindex('/')+1] #rindex finds the LAST time the '/' is found, adding 1 includes the slash
        #print 'plotpath=',PLOTpath


        #m=chanindx
        m=modct

        for mm in range(nsats):
                rowindx=np.arange(0,nrows,nsats)+mm
                satcode=int(IDsat[0,mm]) # IF THERE ARE MIXUPS IN THE satellite IDs, may need to add code to accum.py to make sure the sat ids are parsed properly
                #print 'satcode=', satcode
                try:
                        satname = code2sat_name[satcode]
                except:
                        satname = 'xxx'
                satname='NOAA15'
                #print 'satname=', satname
                satname="".join(c for c in satname if c not in space)
                satname="".join(c for c in satname if c not in punct)
                satname="".join(c for c in satname if c not in hyphen)

                channum_str=str(channel)
                figname=PLOTpath+model+'_AMSUA_'+satname+'_ch'+channum_str+'_'+accumDATEbounds[0]+'_'+accumDATEbounds[1]+'_'+geolabelfilename+'.png'

                zeroline=np.zeros(len(datetime_list))

                f, axarr = plt.subplots(6, sharex=True, figsize=(17, 17))#plt.subplots(figsize=(20, 10))

                Ndiagmean= np.nanmean(numobs_diag[rowindx,m])
                Nqcmean= np.nanmean(numobs_qc[rowindx,m])

                axarr[0].plot(datetime_list, numobs_diag[rowindx,m],'k', datetime_list, numobs_qc[rowindx,m],'r')
                #axarr[0].set_title('AMSUA '+satname+' chan '+channum_str)
                f.suptitle(modelname+' AMSUA '+satname+' '+geolabel+' chan '+channum_str, fontsize=20, fontweight='bold')
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
                #axarr[0].text(0.95, 0.5,'NUMOBS',verticalalignment='baseline', horizontalalignment='right',transform=axarr[0].transAxes,color='black', weight='bold', fontsize=18)
                del Nqcmean
                del Ndiagmean


                ax2 = axarr[0].twinx()
                #ax2.plot(datetime_list, 100*numobs_diag[rowindx,m]/numobs_tot[rowindx,m],'m',label = '%bufr in diag')
                #ax2.set_ylabel('%Ndiag/Nbufr', color='m')
                #ax2.plot(datetime_list, 100*numobs_use[rowindx,m]/numobs_diag[rowindx,m],'m--',datetime_list, 100*numobs_qc[rowindx,m]/numobs_use[rowindx,m],'g--', linewidth=3)
                #ax2.plot(datetime_list, 100*numobs_diag[rowindx,m]/numobs_tot[rowindx,m],'m--',datetime_list, 100*numobs_qc[rowindx,m]/numobs_diag[rowindx,m],'g--', linewidth=3)
                ax2.plot(datetime_list, 100*numobs_qc[rowindx,m]/numobs_diag[rowindx,m],'g--', linewidth=3)
                ax2.set_ylabel('PERCENT', color='g')
                #ax2.set_ylim((0,100))
                ax2.set_ylim((-5,105))
                #ax2.legend( loc='lower left')
                for tl in ax2.get_yticklabels():
                        tl.set_color('m')

                box = ax2.get_position()
                ax2.set_position([box.x0, box.y0, box.width * 0.85, box.height])
                #ax2.legend( loc='lower left')
                #ax2.legend(('%use in diag', '%qc in use'), loc='lower left')
                #ax2.legend(('%DAobs/bufr', '%qc/DAobs'), loc='lower left')
                ax2.legend(('%qc/DAobs'), loc='lower left')
#############

                #bufrmean= np.nanmean(Tmean_allbufr[rowindx,m])
                diagmean= np.nanmean(Tmean_alldiag[rowindx,m])
                qcmean= np.nanmean(Tmean_qc[rowindx,m])

#                axarr[1].plot(datetime_list,Tmean_allbufr[rowindx,m],'k',datetime_list, Tmean_alldiag[rowindx,m],'g', datetime_list, Tmean_qc[rowindx,m],'m')
#                axarr[1].plot(datetime_list,Tmean_allbufr[rowindx,m],'k',datetime_list, Tmean_alldiag[rowindx,m],'g', datetime_list, Tmean_qc[rowindx,m],'m')
                axarr[1].plot(datetime_list, Tmean_alldiag[rowindx,m],'g', datetime_list, Tmean_qc[rowindx,m],'m')
                axarr[1].set_ylabel('Tmean')
                box = axarr[1].get_position()
                #####################################
#                maxA = np.nanmax((maxTb,maxTd,maxTq))
                maxA = np.nanmax((maxTd,maxTq))
#                minA = np.nanmin((minTb,minTd,minTq))
                minA = np.nanmin((minTd,minTq))
                rangey=maxA-minA
                maxy= maxA + .05*rangey
                miny= minA - .05*rangey
                axarr[1].set_ylim((miny,maxy))
                del maxy
                del miny
                #####################################
                axarr[1].set_position([box.x0, box.y0, box.width * 0.85, box.height])
                #axarr[1].legend(('all bufr, avg='+str(round(bufrmean,2)), 'all DA obs, avg='+str(round(diagmean,2)), 'QCd DA obs, avg='+str(round(qcmean,2))),loc='center left', bbox_to_anchor=(1, 0.5))
                axarr[1].legend(('all DA obs, avg='+str(round(diagmean,2)), 'QCd DA obs, avg='+str(round(qcmean,2))),loc='center left', bbox_to_anchor=(1, 0.5))
                axarr[1].grid(True)
                axarr[1].set_title('Mean Observation', fontsize=14, fontweight='bold')
                #axarr[1].text(0.95, 0.5,'Mean T',verticalalignment='baseline', horizontalalignment='right',transform=axarr[1].transAxes,color='black', weight='bold', fontsize=18)
                #del bufrmean
                del diagmean
                del qcmean
##################
                biascorravgmean= np.nanmean(Biascorr_mean[rowindx,m])
                biascorrstdmean= np.nanmean(Biascorr_std[rowindx,m])

                axarr[2].plot(datetime_list, Biascorr_mean[rowindx,m],'g', datetime_list, Biascorr_std[rowindx,m],'m')
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
                #axarr[2].text(0.95, 0.5,'Bias Correction',verticalalignment='baseline', horizontalalignment='right',transform=axarr[2].transAxes,color='black', weight='bold', fontsize=18)            
                del biascorravgmean
                del biascorrstdmean
##################
                OmFmean= np.nanmean(OmF_wBC_mean[rowindx,m])
                OmAmean= np.nanmean(OmA_wBC_mean[rowindx,m])

                axarr[3].plot(datetime_list, OmF_wBC_mean[rowindx,m],'r', datetime_list, OmA_wBC_mean[rowindx,m],'g')
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
                #axarr[3].text(0.95, 0.5,'O-F, O-A',verticalalignment='baseline', horizontalalignment='right',transform=axarr[3].transAxes,color='black', weight='bold', fontsize=18)           
                del OmFmean
                del OmAmean
#################
#################
                ENSsprdmean= np.nanmean(ENSspredF_mean[rowindx,m])
                ENSsprderrmean= np.nanmean(ENSsprederrF_mean[rowindx,m])
                ENSOmFstdmean= np.nanmean(ENS_OmF_wBC_std[rowindx,m])
                OmFstdmean= np.nanmean(OmF_wBC_std[rowindx,m])

                axarr[4].plot(  datetime_list, ENSspredF_mean[rowindx,m],'m', datetime_list, ENSsprederrF_mean[rowindx,m],'b',datetime_list, ENS_OmF_wBC_std[rowindx,m],'k',datetime_list, OmF_wBC_std[rowindx,m],'r',)
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
                #axarr[4].text(0.95, 0.5,'GES stats',verticalalignment='baseline', horizontalalignment='right',transform=axarr[4].transAxes,color='black', weight='bold', fontsize=18)
                del ENSsprdmean
                del ENSsprderrmean
                del ENSOmFstdmean
                del OmFstdmean
################        
                ENSsprdmean= np.nanmean(ENSspredA_mean[:,m])
                ENSsprderrmean= np.nanmean(ENSsprederrA_mean[:,m])
                ENSOmAstdmean= np.nanmean(ENS_OmA_wBC_std[:,m])
                OmAstdmean= np.nanmean(OmA_wBC_std[:,m])


###############################
                axarr[5].plot(datetime_list, OmA_wBC_std[rowindx,m],'r')
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
                axarr[5].legend(( 'O-A stdev (control), avg='+str(round(OmAstdmean,3)),' '),loc='enter left', bbox_to_anchor=(1, 0.5))
                axarr[5].grid(True)
                axarr[5].set_title('Analysis Spread and Errors', fontsize=14, fontweight='bold')
###############################

                del ENSsprdmean
                del ENSsprderrmean
                del ENSOmAstdmean
                del OmAstdmean

                #axarr[5].xaxis.set_major_locator(axweek)
                #axarr[5].xaxis.set_major_formatter(dayFmt)
                axarr[5].xaxis.set_major_locator(locator)
                axarr[5].xaxis.set_major_formatter(tick_format)

                for tick in axarr[5].get_xticklabels():
                        tick.set_rotation(70)
                plt.savefig(figname)
        del model





alldates = date_list
numdates=len(alldates)
startdate=alldates[0]
#### call bash script /home/sgregory/plotting_amsu/make_accumPREP_AND_PLOT.bash modified to accept these inputs

submit_type = form['Submit'].value  

#########################
webpathstringindx=imagedir.find("/psd")
web_imagepath=imagedir[webpathstringindx:len(imagedir)]
#########################


imgname1= web_imagepath+models[0]+'_AMSUA_NOAA15_ch'+str(channel)+'_'+str(startdate)+'_'+str(enddate)+'_'+str(geo)+'.png'
imgname2= web_imagepath+models[1]+'_AMSUA_NOAA15_ch'+str(channel)+'_'+str(startdate)+'_'+str(enddate)+'_'+str(geo)+'.png'



listjunk_filename=tempdates_filename + '_junklist3'
text_file = open(listjunk_filename, "w")
text_file.write(str(nummodel)+' nummodel \n')
text_file.write( imgname1+' image \n')
text_file.write( imgname2+' image \n')
text_file.close()





#------ Create web page -----------------------------------
print "Content-Type: text/html\n\n"
print "<center>"
print "<table><tr>"
print "<tr>"
print "<td><a href=\"" +imgname1+ "\" target=\"new\"><IMG src="+imgname1+"></a></td>"
print "<td><a href=\"" +imgname2+ "\" target=\"new\"><IMG src="+imgname2+"></a></td>"
print "</tr>"
print "</tr></table>"
print "</center>"


#########################
#########################
#########################
#########################
#########################
#########################
#########################





