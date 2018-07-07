from plot_RAD_func_TEST import plot_RAD_func_TEST
#from plot_RAD_func import plot_RAD_func

##############################
channel=6
modelstreams=('FV3s2003','CFSR')
datapath='/Projects/gefsrr/ANNUAL/'
instrmnt='amsua'
satlite='n15'
region='GLOBL'
begindate=2003030300
enddate=2003040900


plot_RAD_func_TEST(modelstreams,datapath,instrmnt,satlite,channel,region,begindate,enddate)

