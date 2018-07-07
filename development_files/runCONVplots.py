from plot_CONV_func import plot_CONV_func

##############################
modelstreams=('FV3s2003','FV3s2003')
datapath='/Projects/gefsrr/ANNUAL/'
varb='t'
plevel=800
region='GLOBL'
begindate=2003030300
enddate=2003040900
##############################

plot_CONV_func(modelstreams,datapath,varb,plevel,region,begindate,enddate)

