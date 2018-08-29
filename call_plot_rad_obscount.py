#!/usr/local/bin/python2.7
from plot_rad_obscount_func import plot_rad_obscount_func
import sys

imagedir='/lustre/f1/unswept/Anna.V.Shlyaeva/images/'
datapath='/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/'

if len(sys.argv) < 1:
    raise SystemExit('python call_plot.py <modelstream> ')
modelstream = sys.argv[1]

modelstreams=('CFSR', modelstream)

begindate=modelstream+'010100'
enddate=str(int(modelstream)+1)+'123118'

instrmntnames=['amsua']

for instrmnt in instrmntnames:
  IMAGES=[]
  IMAGES.append(imagedir+modelstreams[0]+'_'+modelstream+'_'+instrmnt+'_obscount.png')
  IMAGES.append(imagedir+modelstreams[1]+'_'+instrmnt+'_obscount.png')
  plot_rad_obscount_func(modelstreams,datapath,instrmnt,begindate,enddate,IMAGES)

