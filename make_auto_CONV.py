#!/usr/local/bin/python2.7
from plot_CONV_func import plot_CONV_func
import numpy as np
import sys, os, os.path, cgi, re
import sys
import _tkinter
import random, string
import time
from datetime import datetime, date, time
from datetime import timedelta


imagedir='/Projects/gefsrr/AUTOPLOTS/'

########################################################
lastdate_filename = sys.argv[1]
modelstream = sys.argv[2]
print 'modelstream=', modelstream
########################################################]
text_file = open(lastdate_filename, "r")
enddate=text_file.read()[0:10]
text_file.close()

windowlen = 30

#######################################################################################
nan=float('nan')
##################
##################

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
begindate=date_list[0]
print 'enddate=',enddate
print 'begindate=',begindate
###########################################################



modelstreams=(modelstream,'CFSR')
datapath='/Projects/gefsrr/ANNUAL/'
pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
regions=['GLOBL','TROPI','NORTH','SOUTH']
variables=['t','u','v','q','gps']

for region in regions:
   for varb in variables:
      for plevel in pcutoffs:
         IMAGES=[]
#         IMAGES.append(imagedir+'/'+modelstreams[0]+'/'+modelstreams[0]+'_'+varb+'_'+str(plevel)+'to'+str(plevel+100)+'mb_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
#         IMAGES.append(imagedir+'/'+modelstreams[0]+'/'+modelstreams[1]+'_'+varb+'_'+str(plevel)+'to'+str(plevel+100)+'mb_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
#         IMAGES.append(imagedir+'/'+modelstreams[0]+'/'+modelstreams[0]+'_'+varb+'_'+str(plevel)+'to'+str(plevel+100)+'mb_'+region+'.png')
#         IMAGES.append(imagedir+'/'+modelstreams[0]+'/'+modelstreams[1]+'_'+varb+'_'+str(plevel)+'to'+str(plevel+100)+'mb_'+region+'.png')
         IMAGES.append(imagedir+'/'+modelstreams[0]+'/CONV_'+modelstreams[0]+'_'+varb+'_'+str(plevel)+'_'+str(plevel+100)+'_'+region+'.png')
         IMAGES.append(imagedir+'/'+modelstreams[0]+'/CONV_'+modelstreams[1]+'_'+varb+'_'+str(plevel)+'_'+str(plevel+100)+'_'+region+'.png')
         plot_CONV_func(modelstreams,datapath,varb,plevel,region,begindate,enddate,IMAGES)  

   del IMAGES
   varb = 'ps'
   plevel=0
   IMAGES=[]
#   IMAGES.append(imagedir+'/'+modelstreams[0]+'/CONV_'+modelstreams[0]+'_'+varb+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
#   IMAGES.append(imagedir+'/'+modelstreams[0]+'/CONV_'+modelstreams[1]+'_'+varb+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
   IMAGES.append(imagedir+'/'+modelstreams[0]+'/CONV_'+modelstreams[0]+'_'+varb+'_'+region+'.png')
   IMAGES.append(imagedir+'/'+modelstreams[0]+'/CONV_'+modelstreams[1]+'_'+varb+'_'+region+'.png')

   plot_CONV_func(modelstreams,datapath,varb,plevel,region,begindate,enddate,IMAGES)  









