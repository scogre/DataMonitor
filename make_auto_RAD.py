#!/usr/local/bin/python2.7
from plot_RAD_func import plot_RAD_func
import numpy as np
import sys, os, os.path, cgi, re
import sys
import _tkinter
import random, string
import time
from datetime import datetime, date, time
from datetime import timedelta


imagedir='/Projects/gefsrr/AUTOPLOTS/'

########################################################
lastdate_filename = sys.argv[1]
modelstream = sys.argv[2]
print 'modelstream=', modelstream
########################################################]
text_file = open(lastdate_filename, "r")
enddate=text_file.read()[0:10]
text_file.close()

windowlen = 30

#######################################################################################
nan=float('nan')
##################
##################

tperday=4
hourincrmnt=24/tperday

ndates= int(tperday)*int(windowlen)

date_list=[]

yrend=enddate[0:4]
moend=enddate[4:6]
daend=enddate[6:8]
hrend=enddate[8:10]
endtime=datetime(int(yrend), int(moend), int(daend), int(hrend),0,0)
delta=timedelta(hours=int(hourincrmnt))

dayspan=timedelta(days=int(windowlen))
starttime=endtime-dayspan

tempdate=starttime

for n in range(ndates):
    tempdate = tempdate + delta
    date_list.append(tempdate.strftime('%Y%m%d%H'))
del tempdate

###########################################################
begindate=date_list[0]
print 'enddate=',enddate
print 'begindate=',begindate
###########################################################

#
#
#
#
modelstreams=(modelstream,'CFSR')
datapath='/Projects/gefsrr/ANNUAL/'
#instrmnt
#satlite
#channel
#region='GLOBL'
#begindate
#enddate
#IMAGES
regions=['GLOBL','TROPI','NORTH','SOUTH']





if modelstream=='FV3s1999':
   instrmnts=['amsua', 'avhrr', 'hirs2', 'msu', 'sndr']
   satlites=[ 'n15'  , 'n15'  , 'n14'  , 'n14', 'g08' ]
elif modelstream=='FV3s2003':
   instrmnts=['amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'avhrr', 'avhrr', 'hirs2', 'hirs3', 'hirs3', 'msu', 'sndr']
   satlites=[ 'n15'  , 'n16'  , 'n15'  , 'n16'  , 'n17'  , 'n16'  , 'n17'  , 'n14'  , 'n16'  , 'n17'  , 'n14', 'g08']
elif modelstream=='FV3s2007':
   instrmnts=['airs', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'hirs3', 'mhs', 'sndr']
   satlites=[ 'aqua', 'aqua' , 'n15'  , 'n18'  , 'n15'  , 'n16'  , 'n17'  , 'n17'  , 'n18', 'g11']
elif modelstream=='FV3s2011':
   instrmnts=['airs', 'amsua',  'amsua', 'amsua', 'amsua', 'amsua', 'avhrr'    , 'avhrr', 'hirs3', 'hirs4'   ,'hirs4', 'iasi'   , 'mhs'    ,'mhs', 'mhs' ]
   satlites=[ 'aqua', 'aqua' ,'metop-a', 'n15'  , 'n18'  , 'n19'  , 'metop-a'  , 'n18'  , 'n17'  , 'metop-a' , 'n19' , 'metop-a', 'metop-a','n18', 'n19' ]
elif modelstream=='FV3s2015':
   instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'atms' , 'avhrr'    , 'avhrr', 'cris', 'hirs4'   , 'iasi'   ,     'mhs',     'mhs', 'mhs' , 'mhs','seviri' ]
   satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n18'  , 'npp'  , 'metop-a'  , 'n18'  , 'npp' , 'metop-a' , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'm10' ]
else:
   instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'atms' , 'avhrr'  , 'avhrr', 'avhrr', 'avhrr', 'avhrr', 'cris', 'hirs2' , 'hirs3', 'hirs3', 'hirs4'   , 'hirs4' , 'iasi'   ,    'mhs',     'mhs', 'mhs' , 'mhs', 'msu', 'seviri', 'sndr', 'sndr']
   satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n16'  , 'n18'  , 'n19'  , 'n15'  , 'n16'  , 'n17'  , 'npp'  , 'metop-a', 'n15'  , 'n16'  , 'n17'  , 'n18'  , 'npp' , 'n14'   , 'n16'  , 'n17'  , 'metop-a' , 'n19'   , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'n14',  'm10'  , 'g08' , 'g11' ]



hirs2_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
msu_channels    = [ 1, 2, 3, 4]
avhrr_channels = [ 3, 4, 5]
hirs3_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
amsua_channels  = [ 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 15]
amsub_channels  = [ 1, 2, 3, 4, 5]
hirs4_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
sndr_channels   = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
mhs_channels    = [ 1, 2, 3, 4, 5]
ssmis_channels  = [ 1, 2, 3, 4, 5, 6, 7, 24]
airs_channels   = [   7,  15,  20,  21,  22,  27,  28,  40,  52,  69, \
                     72,  92,  93,  98,  99, 104, 105, 110, 111, 116, \
                    117, 123, 128, 129, 138, 139, 144, 145, 150, 151, \
                    156, 157, 162, 168, 169, 172, 173, 174, 175, 179, \
                    180, 185, 186, 190, 192, 198, 201, 204, 207, 210, \
                    215, 216, 221, 226, 227, 232, 252, 253, 256, 257, \
                    261, 262, 267, 272, 295, 299, 305, 310, 321, 325, \
                    333, 338, 355, 362, 375, 453, 475, 497, 528, 587, \
                    672, 787, 791, 870, 914, 950,1301,1304,1329,1371, \
                   1382,1415,1424,1449,1455,1477,1500,1519,1565,1574, \
                   1627,1669,1694,1766,1800,1826,1865,1866,1868,1869, \
                   1872,1873,1876,1881,1882,1911,1917,1918,1924,1928 ]
atms_channels   = [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, \
                   11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22]
cris_channels   = [  37,  49,  51,  53,  59,  61,  63,  64,  65,  67, \
                     69,  71,  73,  75,  79,  80,  81,  83,  85,  87, \
                     88,  89,  93,  95,  96,  99, 104, 106, 107, 116, \
                    120, 123, 124, 125, 126, 130, 132, 133, 136, 137, \
                    138, 142, 143, 144, 145, 147, 148, 150, 151, 153, \
                    154, 155, 157, 158, 159, 160, 161, 162, 163, 164, \
                    165, 166, 168, 170, 171, 173, 175, 198, 211, 224, \
                    279, 311, 342, 392, 404, 427, 464, 482, 501, 529, \
                    710, 713 ]
seviri_channels = [ 5, 6]
iasi_channels   = [  16,  38,  49,  51,  55,  57,  59,  61,  63,  66, \
                     70,  72,  74,  79,  81,  83,  85,  87, 104, 106, \
                    109, 111, 113, 116, 119, 122, 125, 128, 131, 133, \
                    135, 138, 141, 144, 146, 148, 151, 154, 157, 159, \
                    161, 163, 167, 170, 173, 176, 180, 185, 187, 193, \
                    199, 205, 207, 210, 212, 214, 217, 219, 222, 224, \
                    226, 230, 232, 236, 239, 243, 246, 249, 252, 254, \
                    260, 262, 265, 267, 269, 275, 282, 294, 296, 299, \
                    303, 306, 323, 327, 329, 335, 345, 347, 350, 354, \
                    356, 360, 366, 371, 373, 375, 377, 379, 381, 383, \
                    386, 389, 398, 401, 404, 407, 410, 414, 416, 426, \
                    428, 432, 434, 439, 445, 457, 515, 546, 552, 559, \
                    566, 571, 573, 646, 662, 668, 756, 867, 906, 921, \
                   1027,1046,1121,1133,1191,1194,1271,1479,1509,1513, \
                   1521,1536,1574,1579,1585,1587,1626,1639,1643,1652, \
                   1658,1671,1786,1805,1884,1991,2019,2094,2119,2213, \
                   2239,2271,2321,2398,2701]

numinst=len(instrmnts)




for nn in range(numinst):
   instrmnt=instrmnts[nn]
   satlite=satlites[nn]
   channelsname=instrmnt+'_channels'
   channels=eval(channelsname)
   print 'channels_name,channels=', channelsname,channels
   for region in regions:
      for channel in channels:
         print 'intrmnt,sat,chan=',instrmnt,satlite,channel
         IMAGES=[]
#         IMAGES.append(imagedir+'/'+modelstreams[0]+'/RAD_'+modelstreams[0]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
#         IMAGES.append(imagedir+'/'+modelstreams[0]+'/RAD_'+modelstreams[1]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
         IMAGES.append(imagedir+'/'+modelstreams[0]+'/RAD_'+modelstreams[0]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'.png')
         IMAGES.append(imagedir+'/'+modelstreams[0]+'/RAD_'+modelstreams[1]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'.png')
         plot_RAD_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate,IMAGES)
   del channels









#!/usr/local/bin/python2.7
#from plot_RAD_func import plot_RAD_func
#import sys, os, os.path, cgi, re
#
#form = cgi.FieldStorage()
#
#
###############################
#channel= form['channel'].value
#modelstreams=(form['streamy1'].value,form['streamy2'].value)
#datapath='/Projects/gefsrr/ANNUAL/'
#inst_sat=form['instrument_satellite'].value
#undscore='_'
#undscore_indx=inst_sat.index(undscore)
#instrmnt=inst_sat[0:undscore_indx]
#satlite=inst_sat[undscore_indx+1:len(inst_sat)]
#
#region=form['geo'].value
#
#
##fcst-start-date
#begindate_nohr = form['fcst-start-date'].value
#begindate = str(begindate_nohr)+'00'
#
#enddate_nohr = form['fcstdate'].value
#enddate=str(enddate_nohr)+'00'
###############################
#
#
#IMAGES=[]
#IMAGES.append(imagedir+modelstreams[0]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
#IMAGES.append(imagedir+modelstreams[1]+'_'+instrmnt+'_'+satlite+'_ch'+str(channel)+'_'+region+'_'+str(begindate)+'_'+str(enddate)+'.png')
#
#
#plot_RAD_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate,IMAGES)
#
#
#
##########################
#webpathstringindx = IMAGES[0].find("/psd")
#web_image1 = IMAGES[0][webpathstringindx:len(IMAGES[0])]
#webpathstringindx = IMAGES[1].find("/psd")
#web_image2 = IMAGES[1][webpathstringindx:len(IMAGES[1])]
##########################
#
##------ Create web page -----------------------------------
#print "Content-Type: text/html\n\n"
#print "<center>"
#print "<table><tr>"
#print "<tr>"
#print "<td><a href=\"" +web_image1+ "\" target=\"new\"><IMG src="+web_image1+"></a></td>"
#print "<td><a href=\"" +web_image2+ "\" target=\"new\"><IMG src="+web_image2+"></a></td>"
#print "</tr>"
#print "</tr></table>"
#print "</center>"
#
#
#
#
#



















