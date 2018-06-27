from plot_RAD_func import plot_RAD_func

##############################
channel=6
modelstreams=('FV3s2003','FV3s2003')
datapath='/Projects/gefsrr/ANNUAL/'
instrmnt='amsua'
satlite='n16'
region='GLOBL'
begindate=2003030300
enddate=2003040900


plot_RAD_func(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate)

