#!/usr/local/bin/python2.7
from plot_RAD_func import plot_RAD_func
import sys, os, os.path, cgi, re

form = cgi.FieldStorage()


##############################
channel= form['channel'].value
modelstreams=(form['streamy1'].value,form['streamy2'].value)
datapath='/Projects/gefsrr/ANNUAL/'
inst_sat=form['instrument_satellite'].value
undscore='_'
undscore_indx=inst_sat.index(undscore)
instrmnt=inst_sat[0:undscore_indx]
satlite=inst_sat[undscore_indx+1:len(inst_sat)]

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


listjunk_filename=writedir+'makeradtest.txt'
text_file = open(listjunk_filename, "w")
text_file.write(str(channel)+' channel \n')
text_file.write(modelstreams[0]+' models \n')
text_file.write(modelstreams[1]+' models \n')
text_file.write(inst_sat+' inst_sat \n')
text_file.write(instrmnt+' instrmnt \n')
text_file.write(instrmnt+'_'+satlite+'\n')
text_file.write(region+' region \n')
text_file.write(str(enddate_nohr)+' end \n')
text_file.write(str(begindate)+' begin \n')
text_file.write(str(enddate)+' end \n')
#text_file.write(beginndate+'_'+enddate+' \n')
text_file.close()



plot_RAD_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate)




