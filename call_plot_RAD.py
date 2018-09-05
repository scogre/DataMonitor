#!/usr/local/bin/python2.7
from plot_RAD_func import plot_RAD_func
import sys, os, os.path, cgi, re


imagedir='/lustre/f1/unswept/Anna.V.Shlyaeva/images/'
datapath='/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/'

modelstreams=('1999','CFSR')

region='GLOBL'

begindate='1999120100'
enddate='2000020500'

instrmnts=['amsua']
satlites=[ 'n15']

numinst=len(instrmnts)
#for instrmnt in instrmnts:
for nn in range(numinst):
   instrmnt=instrmnts[nn]
   satlite=satlites[nn]

   channelsname=instrmnt+'_channels'
   chanimport='from channel_dictionary import '+channelsname
   exec(chanimport)
   channels=eval(channelsname)

   print 'channels_name,channels=', channelsname,channels
   year = 1999
   for channel in channels:
     IMAGES=[]
     IMAGES.append(imagedir+modelstreams[0]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
     IMAGES.append(imagedir+modelstreams[1]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
     plot_RAD_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate,IMAGES)

