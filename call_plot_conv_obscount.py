#!/usr/local/bin/python2.7
from plot_conv_obscount_func import plot_conv_obscount_func

imagedir='/lustre/f1/unswept/Anna.V.Shlyaeva/images/'
datapath='/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/'

modelstreams=('2015', '2015')


begindate='2015010100'
enddate='2016123118'

varnames=['t','uv','ps']

for var in varnames:
  IMAGES=[]
  IMAGES.append(imagedir+modelstreams[0]+'_'+var+'_obscount.png')
  IMAGES.append(imagedir+modelstreams[1]+'_'+var+'_obscount.png')
  plot_conv_obscount_func(modelstreams,datapath,var,begindate,enddate,IMAGES)

