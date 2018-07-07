#!/usr/local/bin/python2.7
from plot_RAD_func import plot_RAD_func
import sys, os, os.path, cgi, re

form = cgi.FieldStorage()

import random, string
length=10
tmpdir='/httpd-test/psd/tmp/gefsrr_data_assim/'
randdir=''.join(random.choice(string.lowercase) for i in range(length))
writedir=tmpdir+randdir+'/'
os.system("mkdir -p "+writedir)


listjunk_filename=writedir+'listtest.txt'
text_file = open(listjunk_filename, "w")
text_file.write('test test \n')
text_file.close()





