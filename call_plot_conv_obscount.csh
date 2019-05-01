#!/bin/csh

foreach streamyr (1999 2003 2007 2011 2015)
  set analdate_start=${streamyr}010100
  set datapath=/lustre/f2/scratch/Oar.Esrl.Nggps_psd/${streamyr}stream/
  set analdate_end=`cat "${datapath}/analdate.csh" | awk 'NR==1{print $3}'`

  echo 'Processing dates from ' $analdate_start ' to ' $analdate_end ' in stream ' $streamyr

  python /lustre/f2/dev/esrl/Anna.V.Shlyaeva/DataMonitor/call_plot_conv_obscount.py ${streamyr} ${analdate_start} ${analdate_end}
end

