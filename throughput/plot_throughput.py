import numpy as np
import datetime as dt
import matplotlib as mpl
mpl.use('Agg') #for web 
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from time import gmtime, strftime
import sys

if len(sys.argv) < 1:
    raise SystemExit('python plot_avgperday_all.py <number of days looking back>')
numdays  = int(sys.argv[1])

date1 = dt.datetime.today()
datelist = [date1 - dt.timedelta(days=x) for x in range(0, numdays)]
dateplot = dates.date2num(datelist)

streams = ('1999', '2003', '2007', '2011', '2015')

fig, axes = plt.subplots(2,3, figsize=(5*3, 4*2), sharey=True)

for i, ax in enumerate(axes.flat):
  if (i < 5):
    stream = streams[i]

    infile = stream+"_out"
    rate = np.loadtxt(infile)
    curdate = str(int(rate[-1]))
    rate = rate[:-2] / 4.

    curdate = dt.date(int(curdate[0:4]), int(curdate[4:6]), int(curdate[6:8]))
    if stream=='2015':
      enddate = dt.date(2019, 6, 1)
    else:
      enddate = dt.date(int(stream)+4,12,31)

    willtake = (enddate-curdate).days / rate.mean()

    today = dt.date.today()
    willend = today + dt.timedelta(days = willtake)

    for j in range(len(rate)):
      ax.bar(left=dateplot[j],height=rate[len(rate)-j-1],color='blue', alpha=0.4)
    ax.axhline(rate.mean(), color='b', ls='--')

    ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(dates.WeekdayLocator())
#    ax.autofmt_xdate()
    ax.set_title(stream+' stream throughput \n Current reanalysis date: '+curdate.strftime('%m/%d/%Y')+'\n Projected production end date '+willend.strftime('%m/%d/%Y'))
  else:
    ax.axis('off')
fig.tight_layout(rect=[0, 0.05, 1, 0.95],pad=2)
plt.text(0.05, 0.02, "Generated "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"UTC", fontsize=12, color='grey',transform=fig.transFigure)
plt.savefig('/lustre/f2/dev/esrl/Anna.V.Shlyaeva/images/throughput/reanl_throughput.png')
plt.close()
