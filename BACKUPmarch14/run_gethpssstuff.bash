#!/bin/bash

startdir=${PWD}
cd /lustre/f2/dev/Scott.Gregory/forgary
MSUB='msub /ncrc/home1/Scott.Gregory/reanalproject/py-ncepbufr-SG/SGmergeNEW/DataMonitor/get_hpssstuff.sh'
echo $MSUB
$MSUB
cd $startdir

