#!/usr/local/bin/python2.7
from plot_conv_obscount_splitwind_func import plot_conv_obscount_splitwind_func
import sys

imagepath='/lustre/f1/unswept/Anna.V.Shlyaeva/images/'
datapath='/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/'

if len(sys.argv) < 3:
    raise SystemExit('python call_plot.py <modelstream> <begindate> <enddate>')
modelstream = sys.argv[1]
begindate=sys.argv[2]
enddate=sys.argv[3]

plot_conv_obscount_func(modelstream,datapath,begindate,enddate,imagepath)

