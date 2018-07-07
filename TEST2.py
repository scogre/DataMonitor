#!/usr/local/bin/python2.7
import numpy as np
from netCDF4 import Dataset
import datetime
#from datetime import date
import time
from datetime import datetime, date, time
from datetime import timedelta
import sys, os, os.path, cgi, re
import matplotlib as mpl
mpl.use('Agg') #for web 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter, DayLocator, HourLocator, AutoDateLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from matplotlib.ticker import LinearLocator
import sys
#from ncepbufr import satellite_names as code2sat_name
import string
import _tkinter

import subprocess

#### data path /Projects/gefsrr
############## make random directory name################
############## make random directory name################
import random, string
length=10
randdir=''.join(random.choice(string.lowercase) for i in range(length))
tmpdir='/httpd-test/psd/tmp/gefsrr_data_assim/'
#tmpdir='/psd/tmp/gefsrr_data_assim/'
writedir=tmpdir+randdir+'/'
imagedir=writedir+'images/'
os.system("mkdir -p "+writedir)
os.system("mkdir -p "+imagedir)
########################################################

docroot = sys.path[0]
form = cgi.FieldStorage()

enddate_nohr = form['fcstdate'].value
enddate=str(enddate_nohr)+'00'
windowlen = form['windowlen'].value
geo = form['geo'].value
channel = form['channel'].value
#modelstream = form['stream'].value
#modelstream = 'FV3s1999'
####################
tempdates_filename = writedir+'/temp_dates.txt'
plotpath = imagedir

accumdatapath = plotpath
######################
######################
#######################################################################################
nan=float('nan')
##################
##################


imgname1= '/psd/tmp/gefsrr_data_assim/nljmygtfod/images/FV3s2003_AMSUA_NOAA15_ch6_2003030606_2003040300_GLOBL.png'
imgname2= '/psd/tmp/gefsrr_data_assim/nljmygtfod/images/CFSR_AMSUA_NOAA15_ch6_2003030606_2003040300_GLOBL.png'


#------ Create web page -----------------------------------
print "Content-Type: text/html\n\n"
print "<center>"
print "<table><tr>"
print "<tr>"
print "<td><a href=\"" +imgname1+ "\" target=\"new\"><IMG src="+imgname1+"></a></td>"
print "<td><a href=\"" +imgname2+ "\" target=\"new\"><IMG src="+imgname2+"></a></td>"
print "</tr>"
print "</tr></table>"
print "</center>"


#########################
#########################
#########################
#########################
#########################
#########################
#########################





