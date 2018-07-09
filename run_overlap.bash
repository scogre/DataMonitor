#!/bin/bash
#models[1]=CFSR
models[0]=FV3s1999
models[1]=FV3s2003
models[2]=FV3s2007
models[3]=FV3s2011
models[4]=FV3s2015
models[5]=CFSR


obtype=CONV_t
bash /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/ANNUAL/DataMonitor/make_OVERLAP_ALL.bash ${models[*]} $obtype
obtype=RAD
bash /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/ANNUAL/DataMonitor/make_OVERLAP_ALL.bash ${models[*]} $obtype


