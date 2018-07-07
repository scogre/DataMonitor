#!/usr/local/bin/python2.7
from plot_CONV_func import plot_CONV_func
import sys, os, os.path, cgi, re

form = cgi.FieldStorage()


##############################
varb= form['plotvarb'].value
modelstreams=(form['streamy1'].value,form['streamy2'].value)
datapath='/Projects/gefsrr/ANNUAL/'
plevel=form['level'].value
region=form['geo'].value


#fcst-start-date
begindate_nohr = form['fcst-start-date'].value
begindate = str(begindate_nohr)+'00'

enddate_nohr = form['fcstdate'].value
enddate=str(enddate_nohr)+'00'
###############################

import random, string
length=10
tmpdir='/httpd-test/psd/tmp/gefsrr_data_assim/'
randdir=''.join(random.choice(string.lowercase) for i in range(length))
writedir=tmpdir+randdir+'/'
os.system("mkdir -p "+writedir)
#
#
listjunk_filename=writedir+'makeCONVtest.txt'
text_file = open(listjunk_filename, "w")
text_file.write(modelstreams[0]+' models \n')
text_file.write(modelstreams[1]+' models \n')
text_file.write(varb+' varb \n')
text_file.write(plevel+' level \n')
text_file.write(region+' region \n')
text_file.write(str(begindate)+' begin \n')
text_file.write(str(enddate)+' end \n')
text_file.write(begindate+'_'+enddate+' \n')
text_file.close()



plot_CONV_func(modelstreams,datapath,varb,plevel,region,begindate,enddate)


