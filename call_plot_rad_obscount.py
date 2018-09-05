#!/usr/local/bin/python2.7
from plot_rad_obscount_func import plot_rad_obscount_func
import sys

imagedir='/lustre/f1/unswept/Anna.V.Shlyaeva/images/obscounts/'
datapath='/lustre/f1/unswept/Anna.V.Shlyaeva/monitor/'

if len(sys.argv) < 3:
    raise SystemExit('python call_plot.py <modelstream> <date1> <date2>')
modelstream = sys.argv[1]
begindate = sys.argv[2]
enddate = sys.argv[3]

plot_rad_obscount_func(modelstream,datapath,begindate,enddate, imagedir)

