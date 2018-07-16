#!/usr/local/bin/python2.7
from plot_RAD_func import plot_RAD_func
import sys, os, os.path, cgi, re


imagedir='/lustre/f1/unswept/Anna.V.Shlyaeva/images/'
datapath='/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/'
intr_sat='amsua_n15'

modelstreams=('1999','CFSR')
instrmnt='amsua'
satlite='n15'
channel=9

region='GLOBL'

begindate='1999080100'
enddate='1999083118'


IMAGES=[]
IMAGES.append(imagedir+modelstreams[0]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
IMAGES.append(imagedir+modelstreams[1]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')


plot_RAD_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate,IMAGES)

