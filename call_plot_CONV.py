#!/usr/local/bin/python2.7
from plot_CONV_func import plot_CONV_func


imagedir='/lustre/f1/unswept/Anna.V.Shlyaeva/images/'
datapath='/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/'
intr_sat='amsua_n15'

modelstreams=('1999','CFSR')

region='GLOBL'

begindate='1999010100'
enddate='1999093018'

varnames=['t'] #,'u','v','q','ps']
plevels=range(0,1000,100)

for var in varnames:
   for plev in plevels:
     IMAGES=[]
     IMAGES.append(imagedir+modelstreams[0]+'_'+var+'_'+str(plev)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
     IMAGES.append(imagedir+modelstreams[1]+'_'+var+'_'+str(plev)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
     plot_CONV_func(modelstreams,datapath,var,plev,region,begindate,enddate,IMAGES)

