#!/usr/local/bin/python2.7
from plot_conv_func import plot_conv_func
import sys

imagedir='/lustre/f1/unswept/Anna.V.Shlyaeva/images/latest/'
datapath='/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/'

if len(sys.argv) < 3:
    raise SystemExit('python call_plot.py <modelstream> <begindate> <enddate>')
modelstream = sys.argv[1]
begindate=sys.argv[2]
enddate=sys.argv[3]

modelstreams = [modelstream, 'CFSR']

region='GLOBL'

print 'processing from ', begindate, ' to ', enddate

varnames=['t','u','v','q']
plevels=range(0,1000,100)
for var in varnames:
   for plev in plevels:
     figname = imagedir+modelstreams[0]+'_'+var+'_'+str(plev)+'.png'
     plot_conv_func(modelstreams,datapath,var,plev,region,begindate,enddate,figname)

var='ps'
plev=0
figname = imagedir+modelstreams[0]+'_'+var+'_'+str(plev)+'.png'
plot_conv_func(modelstreams,datapath,var,plev,region,begindate,enddate,figname)

