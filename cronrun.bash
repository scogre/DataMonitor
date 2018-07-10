#!/bin/bash

startdir=${PWD}
cd /Projects/gefsrr/ANNUAL/
scp Scott.Gregory@jetscp.rdhpcs.noaa.gov:/mnt/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/RADannuals.tar.gz .
tar -xvf RADannuals.tar.gz
scp Scott.Gregory@jetscp.rdhpcs.noaa.gov:/mnt/lfs3/projects/gfsenkf/Scott.Gregory/GAEAtransfer/CONVannuals.tar.gz .
tar -xvf CONVannuals.tar.gz

cd $startdir
/bin/bash /httpd-test/external/cgi-bin/forecast-modeling/gefsrr/data_assim/ANNUAL/DataMonitor/AUTO_ALL.bash


