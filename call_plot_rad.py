#!/usr/local/bin/python2.7
from plot_rad_func import plot_rad_func
import sys, os, os.path, cgi, re

imagedir='/lustre/f2/dev/esrl/Anna.V.Shlyaeva/images/latest/'
datapath='/lustre/f2/dev/esrl/Anna.V.Shlyaeva/monitor/'

if len(sys.argv) < 3:
    raise SystemExit('python call_plot.py <modelstream> <begindate> <enddate>')
modelstream = sys.argv[1]
begindate=sys.argv[2]
enddate=sys.argv[3]

modelstreams = [modelstream, 'CFSR']

region='GLOBL'

instrmnts=['amsua','amsua']
satlites=[ 'n15','metop-a']

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
   for channel in channels:
     imagefile = imagedir+modelstream+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'.png'
     plot_rad_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate,imagefile)

