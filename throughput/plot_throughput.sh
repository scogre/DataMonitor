#!/bin/sh
ndates=30

cd /lustre/f2/dev/esrl/Anna.V.Shlyaeva/DataMonitor/throughput/

for stream in '1999' '2003' '2007' '2011' '2015'
do
  echo "Processing " $stream
  grep "all done"  /lustre/f2/dev/esrl/Oar.Esrl.Nggps_psd/scripts/${stream}stream/${stream}stream.out | awk '{print $1,$5,$6,$9}' > ${stream}stream_time
  date2=`date -I`
  date1=$(date -I -d "$d -$ndates day")
  d=$date1
  rm ${stream}_out
  while [ "$d" != "$date2" ]; do 
    grep "`date -d $d +"%b %-d %Y"`" ${stream}stream_time | wc -l >> ${stream}_out
    d=$(date -I -d "$d + 1 day")
  done
  curdate=`tail -1 ${stream}stream_time |  awk '{print $1}'`
  echo $curdate >> ${stream}_out
  rm ${stream}stream_time
done

#python plot_throughput.py  ${ndates}
