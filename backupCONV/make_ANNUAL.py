from time import clock
import numpy as np
from netCDF4 import Dataset
import sys, os
import math
###'/Users/sgregory/Documents/NOAA/Data_Assimilation/Git_clone/py-ncepbufr-SG/moveSGmerge/bufr2nc'$date'/'
#diag_nc_filename = '/Users/sgregory/Documents/NOAA/Data_Assimilation/Git_clone/py-ncepbufr-SG/moveSGmerge/bufr2nc2000062718/prep2000062718.nc'
#nc_diagdata = Dataset(diag_nc_filename,'a')
##########################################################################################
#ncplotdata_filename = '/Users/sgregory/Documents/NOAA/Data_Assimilation/Git_clone/py-ncepbufr-SG/moveSGmerge/bufr2nc2000062718/prep_plotdata2000062718.nc'
##########################################################################################

if len(sys.argv) < 3:
    raise SystemExit('python make_prepplotdata.py <merged nc prepbufr filename> <output plotdata file>')
# file names from command line args.
diag_nc_filename = sys.argv[1]
ncplotdata_filename = sys.argv[2]

##########################################################################################
nc_diagdata = Dataset(diag_nc_filename,'r')
full_gsiobs=nc_diagdata['gsiobs'][:]
lendata=full_gsiobs.shape[0]
print 'lendata=',lendata
indcs_master=np.arange(lendata)

full_gsilat = nc_diagdata['gsilat'][:]
#print 'shapelat=', full_gsilat.shape
#print 'lat1to10=', full_gsilat

###################
###################
###################
nan=float('nan')
emptyval=nan	
#emptyval = -99999

##########################################################################################
##########################################################################################
print 'plotdatafile=', ncplotdata_filename
print 'merge datafile=', diag_nc_filename
lenfilename=len(ncplotdata_filename)


for mm in range(4):
	print 'mm=', mm
	if mm==0:
		boundaries=(-90,-20)
		suffix='_SOUTH'
	elif mm==1:
		boundaries=(-20,20)
		suffix='_TROPI'
	elif mm==2:
		boundaries=(20,90)
		suffix='_NORTH'
	elif mm==3:
		boundaries=(-90,90)
		suffix='_GLOBL'
	minlat=min(boundaries)
	maxlat=max(boundaries)
	latindcs=(indcs_master[(full_gsilat[:]>=minlat) & (full_gsilat[:]<=maxlat)] )
	print 'lenlat=', len(latindcs)
        print 'region=', suffix
	
	dummy = nc_diagdata['gsi_hx_A'][:]
	gsi_hx_A=dummy[latindcs,:]; del dummy
	dummy = nc_diagdata['gsi_hx_F'][:]
	gsi_hx_F=dummy[latindcs,:]; del dummy
	dummy = nc_diagdata['gsiuse'][:]
	gsiuse=dummy[latindcs,:]; del dummy
        print 'sum_gsiuse(0)=',np.sum(gsiuse, axis=0)
        print 'np.nanmax(gsiuse)=',np.nanmax(gsiuse)
        print 'gsiuse=',gsiuse
	dummy = nc_diagdata['gsiobs'][:]
	gsiobs=dummy[latindcs,:]; del dummy
	dummy = nc_diagdata['gsierr'][:]
	gsierr=dummy[latindcs,:]; del dummy
	dummy = nc_diagdata['gsipress'][:]
	gsipress=dummy[latindcs,:]; del dummy
	dummy = nc_diagdata['gsilat'][:]
	gsilat=dummy[latindcs]; del dummy
	dummy = nc_diagdata['gsilon'][:]
	gsilon=dummy[latindcs]; del dummy
	OmA = gsiobs-gsi_hx_A
	OmF = gsiobs-gsi_hx_F

        print 'FOUND ENSdata'
        dummy = nc_diagdata['gsi_hx_Aens'][:]
        gsi_hx_Aens=dummy[latindcs,:]; del dummy
        dummy = nc_diagdata['gsi_hx_Fens'][:]
        gsi_hx_Fens=dummy[latindcs,:]; del dummy
        dummy = nc_diagdata['gsi_hx_Asprd'][:]
        gsi_hx_Asprd=dummy[latindcs,:]; del dummy
        dummy = nc_diagdata['gsi_hx_Fsprd'][:]
        gsi_hx_Fsprd=dummy[latindcs,:]; del dummy
        dummy = nc_diagdata['gsiENSuse'][:]
        gsiENSuse=dummy[latindcs,:]; del dummy

        OmAens = gsiobs-gsi_hx_Aens
        OmFens = gsiobs-gsi_hx_Fens
        print 'gsi_hx_Fsprd + gsierr=',gsi_hx_Fsprd + gsierr
        print 'np.sqrt(gsi_hx_Fsprd)=', np.sqrt(gsi_hx_Fsprd)
        print 'np.sqrt(gsierr)=', np.sqrt(gsierr)
        #sumA=(abs(gsi_hx_Asprd) + abs(gsierr))
        sumA=(abs(gsierr)) ## analysis- spread is zero or -9999
        sumF=(abs(gsi_hx_Fsprd) + abs(gsierr))
        #ENSsprederrA = np.sqrt(gsi_hx_Asprd + gsierr)
        #ENSsprederrF = np.sqrt(gsi_hx_Fsprd + gsierr)
        ENSsprederrA = np.sqrt(sumA)
        ENSsprederrF = np.sqrt(sumF)
        del sumA
        del sumF
        lendata=gsi_hx_Aens.shape[0]
        ENSindcs=np.arange(lendata)
	
#	try:
#		print 'FOUND ENSdata'
#		dummy = nc_diagdata['gsi_hx_Aens'][:]
#		gsi_hx_Aens=dummy[latindcs,:]; del dummy
#		dummy = nc_diagdata['gsi_hx_Fens'][:]
#		gsi_hx_Fens=dummy[latindcs,:]; del dummy
#		dummy = nc_diagdata['gsi_hx_Asprd'][:]
#		gsi_hx_Asprd=dummy[latindcs,:]; del dummy
#		dummy = nc_diagdata['gsi_hx_Fsprd'][:]
#		gsi_hx_Fsprd=dummy[latindcs,:]; del dummy
#		dummy = nc_diagdata['gsiENSuse'][:]
#		gsiENSuse=dummy[latindcs,:]; del dummy
#		
#		OmAens = gsiobs-gsi_hx_Aens
#		OmFens = gsiobs-gsi_hx_Fens
#                print 'gsi_hx_Fsprd + gsierr=',gsi_hx_Fsprd + gsierr
#                print 'np.sqrt(gsi_hx_Fsprd)=', np.sqrt(gsi_hx_Fsprd)
#                print 'np.sqrt(gsierr)=', np.sqrt(gsierr)
#                #sumA=(abs(gsi_hx_Asprd) + abs(gsierr))
#                sumA=(abs(gsierr)) ## analysis- spread is zero or -9999
#                sumF=(abs(gsi_hx_Fsprd) + abs(gsierr))
#                #ENSsprederrA = np.sqrt(gsi_hx_Asprd + gsierr)
#  		#ENSsprederrF = np.sqrt(gsi_hx_Fsprd + gsierr)
#                ENSsprederrA = sqrt(sumA)
#		ENSsprederrF = sqrt(sumF)
#                del sumA
#                del sumF
#		lendata=gsi_hx_Aens.shape[0]
#		ENSindcs=np.arange(lendata)
#	except:
#                print 'region=',suffix
#		print 'NO ENSdata'
#		gsi_hx_Aens = emptyval* np.ones(gsiobs.shape)
#		gsi_hx_Fens = emptyval* np.ones(gsiobs.shape)
#		gsi_hx_Asprd = emptyval* np.ones(gsiobs.shape)
#		gsi_hx_Fsprd = emptyval* np.ones(gsiobs.shape)
#		gsiENSuse = emptyval* np.ones(gsiobs.shape)
#		OmAens = emptyval* np.ones(gsiobs.shape)
#		OmFens = emptyval* np.ones(gsiobs.shape)
#		ENSsprederrA = emptyval* np.ones(gsiobs.shape)
#		ENSsprederrF = emptyval* np.ones(gsiobs.shape)
#		lendata=gsi_hx_Aens.shape[0]
#		ENSindcs=np.arange(lendata)
#	###################
	
	GEOncplotdata_filename= ncplotdata_filename[0:lenfilename-3] + suffix +'.nc'
	print 'geoname=',GEOncplotdata_filename
	plotdata_nc = Dataset(GEOncplotdata_filename,'w',format='NETCDF4')
		
	
	pcutoffs=range(0,1000,100) ##=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
	nlevs=len(pcutoffs)
	nlevd = plotdata_nc.createDimension('nlevs',None)
	##########################################################################################
	plotdata_nc.createVariable('Plevels',np.float32,('nlevs',),zlib=False)
	##########################################################################################
	
        plotdata_nc.createVariable('Q_bufr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_bufr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_bufr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_bufr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_bufr_avg',np.float32)
#       plotdata_nc.createVariable('PW_bufr_avg',np.float32)

        plotdata_nc.createVariable('Q_Nbufr',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Nbufr',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Nbufr',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Nbufr',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Nbufr',np.int)
#       plotdata_nc.createVariable('PW_Nbufr',np.int) 
        ##########################################################################################

        plotdata_nc.createVariable('Q_diagavg_obs',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_diagavg_obs',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_diagavg_obs',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_diagavg_obs',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_diagavg_obs',np.float32)
#       plotdata_nc.createVariable('PW_diagavg_obs',np.float32)

        plotdata_nc.createVariable('Q_diagavg_use_obs',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_diagavg_use_obs',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_diagavg_use_obs',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_diagavg_use_obs',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_diagavg_use_obs',np.float32)
#       plotdata_nc.createVariable('PW_diagavg_use_obs',np.float32)


        plotdata_nc.createVariable('Q_Ntotdiag',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Ntotdiag',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Ntotdiag',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Ntotdiag',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Ntotdiag',np.int)
#       plotdata_nc.createVariable('PW_Ntotdiag',np.int)

        plotdata_nc.createVariable('Q_Nusediag',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Nusediag',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Nusediag',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Nusediag',np.int,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Nusediag',np.int)
#       plotdata_nc.createVariable('PW_Nusediag',np.int)
        ###################
        plotdata_nc.createVariable('Q_A_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_A_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_A_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_A_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_A_avg',np.float32)
#       plotdata_nc.createVariable('PW_A_avg',np.float32)

        plotdata_nc.createVariable('Q_F_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_F_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_F_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_F_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_F_avg',np.float32)
#       plotdata_nc.createVariable('PW_F_avg',np.float32)
        ######
        plotdata_nc.createVariable('Q_OmA_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_OmA_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_OmA_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_OmA_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_OmA_avg',np.float32)
#       plotdata_nc.createVariable('PW_OmA_avg',np.float32)

        plotdata_nc.createVariable('Q_OmF_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_OmF_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_OmF_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_OmF_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_OmF_avg',np.float32)
#       plotdata_nc.createVariable('PW_OmF_avg',np.float32)
        ####################
        plotdata_nc.createVariable('Q_OmA_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_OmA_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_OmA_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_OmA_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_OmA_std',np.float32)
#       plotdata_nc.createVariable('PW_OmA_std',np.float32)

        plotdata_nc.createVariable('Q_OmF_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_OmF_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_OmF_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_OmF_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_OmF_std',np.float32)
#       plotdata_nc.createVariable('PW_OmF_std',np.float32)
        ######################################
        ######################################
        #####  ENSEMBLE INFO   ###############
        ######################################
        ######################################
        plotdata_nc.createVariable('Q_Asprd_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Asprd_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Asprd_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Asprd_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Asprd_avg',np.float32)
#       plotdata_nc.createVariable('PW_Asprd_avg',np.float32)

        plotdata_nc.createVariable('Q_Fsprd_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Fsprd_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Fsprd_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Fsprd_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Fsprd_avg',np.float32)
#       plotdata_nc.createVariable('PW_Fsprd_avg',np.float32)

        ####################
        plotdata_nc.createVariable('Q_Asprd_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Asprd_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Asprd_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Asprd_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Asprd_std',np.float32)
#       plotdata_nc.createVariable('PW_Asprd_std',np.float32)

        plotdata_nc.createVariable('Q_Fsprd_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Fsprd_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Fsprd_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Fsprd_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Fsprd_std',np.float32)
#       plotdata_nc.createVariable('PW_Fsprd_std',np.float32)

        ####################
        plotdata_nc.createVariable('Q_Asprderr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Asprderr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Asprderr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Asprderr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Asprderr_avg',np.float32)
#       plotdata_nc.createVariable('PW_Asprderr_avg',np.float32)

        plotdata_nc.createVariable('Q_Fsprderr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_Fsprderr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_Fsprderr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_Fsprderr_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_Fsprderr_avg',np.float32)
#       plotdata_nc.createVariable('PW_Fsprderr_avg',np.float32)

        ####################
        plotdata_nc.createVariable('Q_OmAens_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_OmAens_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_OmAens_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_OmAens_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_OmAens_avg',np.float32)
#       plotdata_nc.createVariable('PW_OmAens_avg',np.float32)

        plotdata_nc.createVariable('Q_OmFens_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_OmFens_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_OmFens_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_OmFens_avg',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_OmFens_avg',np.float32)
#       plotdata_nc.createVariable('PW_OmFens_avg',np.float32)
        #####
        plotdata_nc.createVariable('Q_OmAens_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_OmAens_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_OmAens_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_OmAens_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_OmAens_std',np.float32)
#       plotdata_nc.createVariable('PW_OmAens_std',np.float32)

        plotdata_nc.createVariable('Q_OmFens_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('T_OmFens_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('U_OmFens_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('V_OmFens_std',np.float32,('nlevs',),zlib=False)
        plotdata_nc.createVariable('PS_OmFens_std',np.float32)
#       plotdata_nc.createVariable('PW_OmFens_std',np.float32)

        ##########################################################################################

        Q_bufr_avg =  nan * np.ones(nlevs)
        T_bufr_avg =  nan * np.ones(nlevs)
        U_bufr_avg =  nan * np.ones(nlevs)
        V_bufr_avg =  nan * np.ones(nlevs)

        Q_Nbufr = nan * np.ones(nlevs)
        T_Nbufr = nan * np.ones(nlevs)
        U_Nbufr = nan * np.ones(nlevs)
        V_Nbufr = nan * np.ones(nlevs)
        ##########################################################################################

        Q_diagavg_obs =  nan * np.ones(nlevs)
        T_diagavg_obs =  nan * np.ones(nlevs)
        U_diagavg_obs =  nan * np.ones(nlevs)
        V_diagavg_obs =  nan * np.ones(nlevs)

        Q_diagavg_use_obs =  nan * np.ones(nlevs)
        T_diagavg_use_obs =  nan * np.ones(nlevs)
        U_diagavg_use_obs =  nan * np.ones(nlevs)
        V_diagavg_use_obs =  nan * np.ones(nlevs)
 
        Q_Ntotdiag =  nan * np.ones(nlevs)
        T_Ntotdiag =  nan * np.ones(nlevs)
        U_Ntotdiag =  nan * np.ones(nlevs)
        V_Ntotdiag =  nan * np.ones(nlevs)

        Q_Nusediag =  nan * np.ones(nlevs)
        T_Nusediag =  nan * np.ones(nlevs)
        U_Nusediag =  nan * np.ones(nlevs)
        V_Nusediag =  nan * np.ones(nlevs)
        ###################
        Q_A_avg =  nan * np.ones(nlevs)
        T_A_avg =  nan * np.ones(nlevs)
        U_A_avg =  nan * np.ones(nlevs)
        V_A_avg =  nan * np.ones(nlevs)

        Q_F_avg =  nan * np.ones(nlevs)
        T_F_avg =  nan * np.ones(nlevs)
        U_F_avg =  nan * np.ones(nlevs)
        V_F_avg =  nan * np.ones(nlevs)
        ###################
        Q_OmA_avg =  nan * np.ones(nlevs)
        T_OmA_avg =  nan * np.ones(nlevs)
        U_OmA_avg =  nan * np.ones(nlevs)
        V_OmA_avg =  nan * np.ones(nlevs)

        Q_OmF_avg =  nan * np.ones(nlevs)
        T_OmF_avg =  nan * np.ones(nlevs)
        U_OmF_avg =  nan * np.ones(nlevs)
        V_OmF_avg =  nan * np.ones(nlevs)
        ####################
        Q_OmA_std =  nan * np.ones(nlevs)
        T_OmA_std =  nan * np.ones(nlevs)
        U_OmA_std =  nan * np.ones(nlevs)
        V_OmA_std =  nan * np.ones(nlevs)

        Q_OmF_std =  nan * np.ones(nlevs)
        T_OmF_std =  nan * np.ones(nlevs)
        U_OmF_std =  nan * np.ones(nlevs)
        V_OmF_std =  nan * np.ones(nlevs)
        ####################
        ####################
        ####################
        ####################
        ####################
        ####################
        ####################
        Q_Asprd_avg =  nan * np.ones(nlevs)
        T_Asprd_avg =  nan * np.ones(nlevs)
        U_Asprd_avg =  nan * np.ones(nlevs)
        V_Asprd_avg =  nan * np.ones(nlevs)

        Q_Fsprd_avg =  nan * np.ones(nlevs)
        T_Fsprd_avg =  nan * np.ones(nlevs)
        U_Fsprd_avg =  nan * np.ones(nlevs)
        V_Fsprd_avg =  nan * np.ones(nlevs)

        ####################
        Q_Asprd_std =  nan * np.ones(nlevs)
        T_Asprd_std =  nan * np.ones(nlevs)
        U_Asprd_std =  nan * np.ones(nlevs)
        V_Asprd_std =  nan * np.ones(nlevs)

        Q_Fsprd_std =  nan * np.ones(nlevs)
        T_Fsprd_std =  nan * np.ones(nlevs)
        U_Fsprd_std =  nan * np.ones(nlevs)
        V_Fsprd_std =  nan * np.ones(nlevs)

        ####################
        Q_Asprderr_avg =  nan * np.ones(nlevs)
        T_Asprderr_avg =  nan * np.ones(nlevs)
        U_Asprderr_avg =  nan * np.ones(nlevs)
        V_Asprderr_avg =  nan * np.ones(nlevs)

        Q_Fsprderr_avg =  nan * np.ones(nlevs)
        T_Fsprderr_avg =  nan * np.ones(nlevs)
        U_Fsprderr_avg =  nan * np.ones(nlevs)
        V_Fsprderr_avg =  nan * np.ones(nlevs)

        ####################
        Q_OmAens_avg  =nan * np.ones(nlevs)
        T_OmAens_avg  =nan * np.ones(nlevs)
        U_OmAens_avg  =nan * np.ones(nlevs)
        V_OmAens_avg  =nan * np.ones(nlevs)

        Q_OmFens_avg  =nan * np.ones(nlevs)
        T_OmFens_avg  =nan * np.ones(nlevs)
        U_OmFens_avg  =nan * np.ones(nlevs)
        V_OmFens_avg  =nan * np.ones(nlevs)
        ####################
        Q_OmAens_std  =nan * np.ones(nlevs)
        T_OmAens_std  =nan * np.ones(nlevs)
        U_OmAens_std  =nan * np.ones(nlevs)
        V_OmAens_std  =nan * np.ones(nlevs)

        Q_OmFens_std  =nan * np.ones(nlevs)
        T_OmFens_std  =nan * np.ones(nlevs)
        U_OmFens_std  =nan * np.ones(nlevs)
        V_OmFens_std  =nan * np.ones(nlevs)


	
	##########################################################################################
        dummy = nc_diagdata['gsipress'][:]
        diag_pressure=dummy[latindcs,:]; del dummy	



	##############################################################
	
	 
	for pcount in range(nlevs):
	
		##########################
                #print 'pcount=',pcount
                print 'pcutoffs[pcount]=', pcutoffs[pcount]
                print 'region=',suffix	
		ptemp=np.zeros(gsipress.shape)
                #print 'ptemp=',ptemp
                #print 'gsipress,pcutoffs[pcount]=',gsipress,pcutoffs[pcount]
                #print 'isnan(gsipress)=',np.isnan(gsipress)
                #print 'gsipress>=pcutoffs[pcount] ',gsipress>=pcutoffs[pcount]
		if pcount+1<nlevs:
                        print 'pcutoffs[pcount]=', pcutoffs[pcount]
                        print 'pcutoffs[pcount+1]=', pcutoffs[pcount+1]
                        #print 'gsipress<=pcutoffs[pcount+1] ',gsipress<=pcutoffs[pcount+1]
                        #print '[(gsipress>=pcutoffs[pcount]) & (gsipress<=pcutoffs[pcount+1])] =',[(gsipress>=pcutoffs[pcount]) & (gsipress<=pcutoffs[pcount+1])]
			ptemp[(gsipress>=pcutoffs[pcount]) & (gsipress<=pcutoffs[pcount+1])]=1
                        print 'sum(ptemp(0))=',np.sum(ptemp, axis=0)
                #        print 'ptemp=',ptemp
		else:
                        print 'pcutoffs[pcount]=', pcutoffs[pcount]
			ptemp[(gsipress>=pcutoffs[pcount])]=1
                        print 'sum(ptemp(0))=',np.sum(ptemp, axis=0)
                #        print 'ptemp=',ptemp
		################### DIAG data
		
		lendata=gsiobs.shape[0]
		indcs=np.arange(lendata)
		
		################
		
	
		Q_diag_indcs =( indcs[(gsiobs[:,0] != emptyval) & (ptemp[:,0]==1)] )
		T_diag_indcs =( indcs[(gsiobs[:,1] != emptyval) & (ptemp[:,1]==1)] )
		U_diag_indcs =( indcs[(gsiobs[:,2] != emptyval) & (ptemp[:,2]==1)] )
		V_diag_indcs =( indcs[(gsiobs[:,3] != emptyval) & (ptemp[:,3]==1)] )
	
		
		Q_Ntotdiag[pcount]  = len(Q_diag_indcs)
		T_Ntotdiag[pcount]  = len(T_diag_indcs)
		U_Ntotdiag[pcount]  = len(U_diag_indcs)
		V_Ntotdiag[pcount]  = len(V_diag_indcs)
		
		Q_diagavg_obs[pcount]  =  np.nanmean(gsiobs[Q_diag_indcs,0])
                #print 'Q_diagavg_obs=',Q_diagavg_obs
		T_diagavg_obs[pcount]  =  np.nanmean(gsiobs[T_diag_indcs,1])
		U_diagavg_obs[pcount]  =  np.nanmean(gsiobs[U_diag_indcs,2])
		V_diagavg_obs[pcount]  =  np.nanmean(gsiobs[V_diag_indcs,3])
		################
		
                print 'indcs[(gsiobs[:,0] != emptyval)]=',indcs[(gsiobs[:,0] != emptyval)]
                print 'indcs[(gsiuse[:,0]==1)]=',indcs[(gsiuse[:,0]==1)]
                print 'indcs[(ptemp[:,0]==1)]=',indcs[(ptemp[:,0]==1)]
                print 'len(indcs[(gsiobs[:,0] != emptyval)])=',len(indcs[(gsiobs[:,0] != emptyval)])
                print 'len(indcs[(gsiuse[:,0]==1)])=',len(indcs[(gsiuse[:,0]==1)])
                print 'len(indcs[(ptemp[:,0]==1)])=',len(indcs[(ptemp[:,0]==1)])

                print 'sum_gsiuse(0)=',np.sum(gsiuse, axis=0)
                print 'np.nanmax(gsiuse)=',np.nanmax(gsiuse)
                print 'gsiuse=',gsiuse


                Qusediag_indcs =( indcs[((gsiobs[:,0] != emptyval) & (gsiuse[:,0]==1)) & (ptemp[:,0]==1)] )
                print 'Qusediag_indcs=',Qusediag_indcs
		Tusediag_indcs =( indcs[((gsiobs[:,1] != emptyval) & (gsiuse[:,1]==1)) & (ptemp[:,1]==1)] )
                print 'Tusediag_indcs=',Tusediag_indcs
		Uusediag_indcs =( indcs[((gsiobs[:,2] != emptyval) & (gsiuse[:,2]==1)) & (ptemp[:,2]==1)] )
		Vusediag_indcs =( indcs[((gsiobs[:,3] != emptyval) & (gsiuse[:,3]==1)) & (ptemp[:,3]==1)] )
                print 'Vusediag_indcs=',Vusediag_indcs
		
		Q_Nusediag[pcount]  = len(Qusediag_indcs)
		T_Nusediag[pcount]  = len(Tusediag_indcs)
		U_Nusediag[pcount]  = len(Uusediag_indcs)
		V_Nusediag[pcount]  = len(Vusediag_indcs)
		
		Q_diagavg_use_obs[pcount]  =  np.nanmean(gsiobs[Qusediag_indcs,0])
		T_diagavg_use_obs[pcount]  =  np.nanmean(gsiobs[Tusediag_indcs,1])
		U_diagavg_use_obs[pcount]  =  np.nanmean(gsiobs[Uusediag_indcs,2])
		V_diagavg_use_obs[pcount]  =  np.nanmean(gsiobs[Vusediag_indcs,3])
		
		################
		Q_A_avg[pcount] = np.nanmean(gsi_hx_A[Qusediag_indcs,0])
                print 'Q_A_avg=',Q_A_avg[pcount]
		T_A_avg[pcount] = np.nanmean(gsi_hx_A[Tusediag_indcs,1])
		U_A_avg[pcount] = np.nanmean(gsi_hx_A[Uusediag_indcs,2])
		V_A_avg[pcount] = np.nanmean(gsi_hx_A[Vusediag_indcs,3])
		
		Q_F_avg[pcount] = np.nanmean(gsi_hx_F[Qusediag_indcs,0])
		T_F_avg[pcount] = np.nanmean(gsi_hx_F[Tusediag_indcs,1])
		U_F_avg[pcount] = np.nanmean(gsi_hx_F[Uusediag_indcs,2])
		V_F_avg[pcount] = np.nanmean(gsi_hx_F[Vusediag_indcs,3])
		################
		################
		Q_OmA_avg[pcount] = np.nanmean(gsiobs[Qusediag_indcs,0]-gsi_hx_A[Qusediag_indcs,0])
		T_OmA_avg[pcount] = np.nanmean(gsiobs[Tusediag_indcs,1]-gsi_hx_A[Tusediag_indcs,1])
		U_OmA_avg[pcount] = np.nanmean(gsiobs[Uusediag_indcs,2]-gsi_hx_A[Uusediag_indcs,2])
		V_OmA_avg[pcount] = np.nanmean(gsiobs[Vusediag_indcs,3]-gsi_hx_A[Vusediag_indcs,3])
		
		Q_OmF_avg[pcount] = np.nanmean(gsiobs[Qusediag_indcs,0]-gsi_hx_F[Qusediag_indcs,0])
		T_OmF_avg[pcount] = np.nanmean(gsiobs[Tusediag_indcs,1]-gsi_hx_F[Tusediag_indcs,1])
		U_OmF_avg[pcount] = np.nanmean(gsiobs[Uusediag_indcs,2]-gsi_hx_F[Uusediag_indcs,2])
		V_OmF_avg[pcount] = np.nanmean(gsiobs[Vusediag_indcs,3]-gsi_hx_F[Vusediag_indcs,3])
		################
		Q_OmA_std[pcount] = np.nanstd(gsiobs[Qusediag_indcs,0]-gsi_hx_A[Qusediag_indcs,0])
		T_OmA_std[pcount] = np.nanstd(gsiobs[Tusediag_indcs,1]-gsi_hx_A[Tusediag_indcs,1])
		U_OmA_std[pcount] = np.nanstd(gsiobs[Uusediag_indcs,2]-gsi_hx_A[Uusediag_indcs,2])
		V_OmA_std[pcount] = np.nanstd(gsiobs[Vusediag_indcs,3]-gsi_hx_A[Vusediag_indcs,3])
		
		Q_OmF_std[pcount] = np.nanstd(gsiobs[Qusediag_indcs,0]-gsi_hx_F[Qusediag_indcs,0])
		T_OmF_std[pcount] = np.nanstd(gsiobs[Tusediag_indcs,1]-gsi_hx_F[Tusediag_indcs,1])
		U_OmF_std[pcount] = np.nanstd(gsiobs[Uusediag_indcs,2]-gsi_hx_F[Uusediag_indcs,2])
		V_OmF_std[pcount] = np.nanstd(gsiobs[Vusediag_indcs,3]-gsi_hx_F[Vusediag_indcs,3])
		############################
		############################
		############################
		############################
		###### ENSEMBLE  ##########
		############################
		############################
		############################
		############################
		############################			
		#print 'gsihxaqsprd=',gsi_hx_Asprd[:,0]
		#print 'len(gsihxaqsprd_empty)=',len(ENSindcs[(gsi_hx_Asprd[:,0] != emptyval)])
		#print 'boolean=',(gsi_hx_Asprd[:,0] != float(emptyval))
		#print 'sumptemp=',sum(ptemp[:,0])
		Q_ENSAdiag_indcs =( ENSindcs[(gsi_hx_Asprd[:,0] != emptyval) & (ptemp[:,0]==1)] ); #print 'len(Q_Asprdindc=)',len(Q_ENSAdiag_indcs)
		T_ENSAdiag_indcs =( ENSindcs[(gsi_hx_Asprd[:,1] != emptyval) & (ptemp[:,1]==1)] ); #print 'T_Asprd=',gsi_hx_Asprd[T_ENSAdiag_indcs,1]
		U_ENSAdiag_indcs =( ENSindcs[(gsi_hx_Asprd[:,2] != emptyval) & (ptemp[:,2]==1)] )
		V_ENSAdiag_indcs =( ENSindcs[(gsi_hx_Asprd[:,3] != emptyval) & (ptemp[:,3]==1)] ) 
		
		Q_N_ENSAtotdiag = len(Q_ENSAdiag_indcs); #print 'Q_NensAtot=',Q_N_ENSAtotdiag
		T_N_ENSAtotdiag = len(T_ENSAdiag_indcs)
		U_N_ENSAtotdiag = len(U_ENSAdiag_indcs)
		V_N_ENSAtotdiag = len(V_ENSAdiag_indcs)
		################
		################
		
		Q_ENSFdiag_indcs =( ENSindcs[(gsi_hx_Fsprd[:,0] != emptyval) & (ptemp[:,0]==1)] )
		T_ENSFdiag_indcs =( ENSindcs[(gsi_hx_Fsprd[:,1] != emptyval) & (ptemp[:,1]==1)] ) 
		U_ENSFdiag_indcs =( ENSindcs[(gsi_hx_Fsprd[:,2] != emptyval) & (ptemp[:,2]==1)] )
		V_ENSFdiag_indcs =( ENSindcs[(gsi_hx_Fsprd[:,3] != emptyval) & (ptemp[:,3]==1)] ) 
		
		Q_N_ENSFtotdiag = len(Q_ENSFdiag_indcs); #print 'Q_NensFtot=',Q_N_ENSFtotdiag
		T_N_ENSFtotdiag = len(T_ENSFdiag_indcs)
		U_N_ENSFtotdiag = len(U_ENSFdiag_indcs)
		V_N_ENSFtotdiag = len(V_ENSFdiag_indcs)
		################
		################
		################
		################
		
		Q_ENSAusediag_indcs = ENSindcs[((gsi_hx_Asprd[:,0] != emptyval) & (gsiENSuse[:,0]==1)) & (ptemp[:,0]==1)]
		T_ENSAusediag_indcs = ENSindcs[((gsi_hx_Asprd[:,1] != emptyval) & (gsiENSuse[:,1]==1)) & (ptemp[:,1]==1)]
		U_ENSAusediag_indcs = ENSindcs[((gsi_hx_Asprd[:,2] != emptyval) & (gsiENSuse[:,2]==1)) & (ptemp[:,2]==1)]
		V_ENSAusediag_indcs = ENSindcs[((gsi_hx_Asprd[:,3] != emptyval) & (gsiENSuse[:,3]==1)) & (ptemp[:,3]==1)]
		
		Q_N_ENSAusediag  = len(Q_ENSAdiag_indcs); #print 'Q_NensAuse=',Q_N_ENSAusediag
		T_N_ENSAusediag  = len(T_ENSAdiag_indcs)
		U_N_ENSAusediag  = len(U_ENSAdiag_indcs)
		V_N_ENSAusediag  = len(V_ENSAdiag_indcs)
		################
		################
		
		Q_ENSFusediag_indcs = ENSindcs[((gsi_hx_Fsprd[:,0] != emptyval) & (gsiENSuse[:,0]==1)) & (ptemp[:,0]==1)]
		T_ENSFusediag_indcs = ENSindcs[((gsi_hx_Fsprd[:,1] != emptyval) & (gsiENSuse[:,1]==1)) & (ptemp[:,1]==1)]
		U_ENSFusediag_indcs = ENSindcs[((gsi_hx_Fsprd[:,2] != emptyval) & (gsiENSuse[:,2]==1)) & (ptemp[:,2]==1)]
		V_ENSFusediag_indcs = ENSindcs[((gsi_hx_Fsprd[:,3] != emptyval) & (gsiENSuse[:,3]==1)) & (ptemp[:,3]==1)]
		
		Q_N_ENSFusediag = len(Q_ENSFusediag_indcs); #print 'Q_NensFuse=',Q_N_ENSFusediag
		T_N_ENSFusediag = len(T_ENSFusediag_indcs)
		U_N_ENSFusediag = len(U_ENSFusediag_indcs)
		V_N_ENSFusediag = len(V_ENSFusediag_indcs)
		################
		################
		################
		
                print 'ENSindcs[(gsi_hx_Asprd[:,1] != emptyval)]=',ENSindcs[(gsi_hx_Asprd[:,1] != emptyval)]
                print 'ENSindcs[(gsiENSuse[:,1]==1)]=',ENSindcs[(gsiENSuse[:,1]==1)]
                print 'ENSindcs[(ptemp[:,1]==1)]=',ENSindcs[(ptemp[:,1]==1)]
                print 'T_ENSAusediag_indcs=',T_ENSAusediag_indcs
		
		################
		################
		Q_Asprd_avg[pcount] = np.nanmean(gsi_hx_Asprd[Q_ENSAusediag_indcs,0]); #print 'Q_Asprd=',gsi_hx_Asprd[Q_ENSAusediag_indcs,0]
		T_Asprd_avg[pcount] = np.nanmean(gsi_hx_Asprd[T_ENSAusediag_indcs,1])
		U_Asprd_avg[pcount] = np.nanmean(gsi_hx_Asprd[U_ENSAusediag_indcs,2])
		V_Asprd_avg[pcount] = np.nanmean(gsi_hx_Asprd[V_ENSAusediag_indcs,3])
                print 'T_Asprd_avg=',T_Asprd_avg[pcount]
		
		Q_Fsprd_avg[pcount] = np.nanmean(gsi_hx_Fsprd[Q_ENSFusediag_indcs,0])
		T_Fsprd_avg[pcount] = np.nanmean(gsi_hx_Fsprd[T_ENSFusediag_indcs,1])
		U_Fsprd_avg[pcount] = np.nanmean(gsi_hx_Fsprd[U_ENSFusediag_indcs,2])
		V_Fsprd_avg[pcount] = np.nanmean(gsi_hx_Fsprd[V_ENSFusediag_indcs,3])
		print 'T_Fsprd_avg=',T_Fsprd_avg[pcount]
		################
		################
		Q_Asprd_std[pcount] = np.nanstd(gsi_hx_Asprd[Q_ENSAusediag_indcs,0])
		T_Asprd_std[pcount] = np.nanstd(gsi_hx_Asprd[T_ENSAusediag_indcs,1])
		U_Asprd_std[pcount] = np.nanstd(gsi_hx_Asprd[U_ENSAusediag_indcs,2])
		V_Asprd_std[pcount] = np.nanstd(gsi_hx_Asprd[V_ENSAusediag_indcs,3])
		
		Q_Fsprd_std[pcount] = np.nanstd(gsi_hx_Fsprd[Q_ENSFusediag_indcs,0])
		T_Fsprd_std[pcount] = np.nanstd(gsi_hx_Fsprd[T_ENSFusediag_indcs,1])
		U_Fsprd_std[pcount] = np.nanstd(gsi_hx_Fsprd[U_ENSFusediag_indcs,2])
		V_Fsprd_std[pcount] = np.nanstd(gsi_hx_Fsprd[V_ENSFusediag_indcs,3])
		################
		################
		################
		Q_Asprderr_avg[pcount] = np.nanmean(ENSsprederrA[Q_ENSAusediag_indcs,0])
		T_Asprderr_avg[pcount] = np.nanmean(ENSsprederrA[T_ENSAusediag_indcs,1])
		U_Asprderr_avg[pcount] = np.nanmean(ENSsprederrA[U_ENSAusediag_indcs,2])
		V_Asprderr_avg[pcount] = np.nanmean(ENSsprederrA[V_ENSAusediag_indcs,3])
		
		Q_Fsprderr_avg[pcount] = np.nanmean(ENSsprederrF[Q_ENSFusediag_indcs,0])
		T_Fsprderr_avg[pcount] = np.nanmean(ENSsprederrF[T_ENSFusediag_indcs,1])
		U_Fsprderr_avg[pcount] = np.nanmean(ENSsprederrF[U_ENSFusediag_indcs,2])
		V_Fsprderr_avg[pcount] = np.nanmean(ENSsprederrF[V_ENSFusediag_indcs,3])
		################
		Q_OmAens_avg[pcount] = np.nanmean(OmAens[Q_ENSAusediag_indcs,0])
		T_OmAens_avg[pcount] = np.nanmean(OmAens[T_ENSAusediag_indcs,1])
		U_OmAens_avg[pcount] = np.nanmean(OmAens[U_ENSAusediag_indcs,2])
		V_OmAens_avg[pcount] = np.nanmean(OmAens[V_ENSAusediag_indcs,3])
		
		Q_OmFens_avg[pcount] = np.nanmean(OmFens[Q_ENSFusediag_indcs,0])
		T_OmFens_avg[pcount] = np.nanmean(OmFens[T_ENSFusediag_indcs,1])
		U_OmFens_avg[pcount] = np.nanmean(OmFens[U_ENSFusediag_indcs,2])
		V_OmFens_avg[pcount] = np.nanmean(OmFens[V_ENSFusediag_indcs,3])
		################
		################
		Q_OmAens_std[pcount] = np.nanstd(OmAens[Q_ENSAusediag_indcs,0])
		T_OmAens_std[pcount] = np.nanstd(OmAens[T_ENSAusediag_indcs,1])
		U_OmAens_std[pcount] = np.nanstd(OmAens[U_ENSAusediag_indcs,2])
		V_OmAens_std[pcount] = np.nanstd(OmAens[V_ENSAusediag_indcs,3])
		
		Q_OmFens_std[pcount] = np.nanstd(OmFens[Q_ENSFusediag_indcs,0])
		T_OmFens_std[pcount] = np.nanstd(OmFens[T_ENSFusediag_indcs,1])
		U_OmFens_std[pcount] = np.nanstd(OmFens[U_ENSFusediag_indcs,2])
		V_OmFens_std[pcount] = np.nanstd(OmFens[V_ENSFusediag_indcs,3])
		################
		################
	
	
	###################
	###################
	lendata=gsiobs.shape[0]
	indcs=np.arange(lendata)
	

	PS_diag_indcs=( indcs[(gsiobs[:,4] != emptyval)] )
#	PW_diag_indcs=( indcs[(gsiobs[:,5] != emptyval)] )
	
	PS_Ntotdiag = len(PS_diag_indcs)
#	PW_Ntotdiag = len(PW_diag_indcs)
	
	PS_diagavg_obs =  np.nanmean(gsiobs[PS_diag_indcs,4])
#	PW_diagavg_obs =  np.nanmean(gsiobs[PW_diag_indcs,5])
	
	PSusediag_indcs=( indcs[((gsiobs[:,4] != emptyval) & (gsiuse[:,4]==1))] )
#	PWusediag_indcs=( indcs[((gsiobs[:,5] != emptyval) & (gsiuse[:,5]==1))] )
	
	PS_Nusediag = len(PSusediag_indcs)
#	PW_Nusediag = len(PWusediag_indcs)
	
	PS_diagavg_use_obs =  np.nanmean(gsiobs[PSusediag_indcs,4])
#	PW_diagavg_use_obs =  np.nanmean(gsiobs[PWusediag_indcs,5])
	
	PS_A_avg = np.nanmean(gsi_hx_A[PSusediag_indcs,4])
#	PW_A_avg = np.nanmean(gsi_hx_A[PWusediag_indcs,5])
	
	PS_F_avg = np.nanmean(gsi_hx_F[PSusediag_indcs,4])
#	PW_F_avg = np.nanmean(gsi_hx_F[PWusediag_indcs,5])
	
	PS_OmA_avg = np.nanmean(gsiobs[PSusediag_indcs,4]-gsi_hx_A[PSusediag_indcs,4])
#	PW_OmA_avg = np.nanmean(gsiobs[PWusediag_indcs,5]-gsi_hx_A[PWusediag_indcs,5])
	
	PS_OmF_avg = np.nanmean(gsiobs[PSusediag_indcs,4]-gsi_hx_F[PSusediag_indcs,4])
#	PW_OmF_avg = np.nanmean(gsiobs[PWusediag_indcs,5]-gsi_hx_F[PWusediag_indcs,5])
	
	PS_OmA_std = np.nanstd(gsiobs[PSusediag_indcs,4]-gsi_hx_A[PSusediag_indcs,4])
#	PW_OmA_std = np.nanstd(gsiobs[PWusediag_indcs,5]-gsi_hx_A[PWusediag_indcs,5])
	
	PS_OmF_std = np.nanstd(gsiobs[PSusediag_indcs,4]-gsi_hx_F[PSusediag_indcs,4])
#	PW_OmF_std = np.nanstd(gsiobs[PWusediag_indcs,5]-gsi_hx_F[PWusediag_indcs,5])
	
	PS_ENSAdiag_indcs=( ENSindcs[(gsi_hx_Asprd[:,4] != emptyval)] )
#	PW_ENSAdiag_indcs=( ENSindcs[(gsi_hx_Asprd[:,5] != emptyval)] )
	
	PS_N_ENSAtotdiag = len(PS_ENSAdiag_indcs)
#	PW_N_ENSAtotdiag = len(PW_ENSAdiag_indcs)
	
	PS_ENSFdiag_indcs=( ENSindcs[(gsi_hx_Fsprd[:,4] != emptyval)] )
#	PW_ENSFdiag_indcs=( ENSindcs[(gsi_hx_Fsprd[:,5] != emptyval)] )
	
	PS_N_ENSFtotdiag = len(PS_ENSFdiag_indcs)
#	PW_N_ENSFtotdiag = len(PW_ENSFdiag_indcs)
	
	PS_ENSAusediag_indcs= ENSindcs[((gsi_hx_Asprd[:,4] != emptyval) & (gsiENSuse[:,4]==1))]
#	PW_ENSAusediag_indcs= ENSindcs[((gsi_hx_Asprd[:,5] != emptyval) & (gsiENSuse[:,5]==1))]
	
	PS_N_ENSAusediag = len(PS_ENSAdiag_indcs)
#	PW_N_ENSAtotdiag = len(PW_ENSAdiag_indcs)
	
	PS_ENSFusediag_indcs= ENSindcs[((gsi_hx_Fsprd[:,4] != emptyval) & (gsiENSuse[:,4]==1))]
#	PW_ENSFusediag_indcs= ENSindcs[((gsi_hx_Fsprd[:,5] != emptyval) & (gsiENSuse[:,5]==1))]
	
	PS_N_ENSFusediag = len(PS_ENSFusediag_indcs)
#	PW_N_ENSFusediag = len(PW_ENSFusediag_indcs)
	########
	
	
	#########
	PS_Asprd_avg = np.nanmean(gsi_hx_Asprd[PS_ENSAusediag_indcs,4])
#	PW_Asprd_avg = np.nanmean(gsi_hx_Asprd[PW_ENSAusediag_indcs,5])
	
	PS_Fsprd_avg = np.nanmean(gsi_hx_Fsprd[PS_ENSFusediag_indcs,4])
#	PW_Fsprd_avg = np.nanmean(gsi_hx_Fsprd[PW_ENSFusediag_indcs,5])
	
	PS_Asprd_std = np.nanstd(gsi_hx_Asprd[PS_ENSAusediag_indcs,4])
#	PW_Asprd_std = np.nanstd(gsi_hx_Asprd[PW_ENSAusediag_indcs,5])
	
	PS_Fsprd_std = np.nanstd(gsi_hx_Fsprd[PS_ENSFusediag_indcs,4])
#	PW_Fsprd_std = np.nanstd(gsi_hx_Fsprd[PW_ENSFusediag_indcs,5])
	
	PS_Asprderr_avg = np.nanmean(ENSsprederrA[PS_ENSAusediag_indcs,4])
#	PW_Asprderr_avg = np.nanmean(ENSsprederrA[PW_ENSAusediag_indcs,5])
	
	PS_Fsprderr_avg = np.nanmean(ENSsprederrF[PS_ENSFusediag_indcs,4])
#	PW_Fsprderr_avg = np.nanmean(ENSsprederrF[PW_ENSFusediag_indcs,5])
	
	PS_OmAens_avg = np.nanmean(OmAens[PS_ENSAusediag_indcs,4])
#	PW_OmAens_avg = np.nanmean(OmAens[PW_ENSAusediag_indcs,5])
	
	PS_OmFens_avg = np.nanmean(OmFens[PS_ENSFusediag_indcs,4])
#	PW_OmFens_avg = np.nanmean(OmFens[PW_ENSFusediag_indcs,5])
	
	PS_OmAens_std = np.nanstd(OmAens[PS_ENSAusediag_indcs,4])
#	PW_OmAens_std = np.nanstd(OmAens[PW_ENSAusediag_indcs,5])
	
	PS_OmFens_std = np.nanstd(OmFens[PS_ENSFusediag_indcs,4])
#	PW_OmFens_std = np.nanstd(OmFens[PW_ENSFusediag_indcs,5])
	
	###################
	###################
	###################
	
	
	
	
	
	
	
	
		
	################
        print 'Q_diagavg_obs=',Q_diagavg_obs
	plotdata_nc['Q_diagavg_obs'][:]  =  Q_diagavg_obs; del  Q_diagavg_obs
	plotdata_nc['T_diagavg_obs'][:]  =  T_diagavg_obs; del  T_diagavg_obs
	plotdata_nc['U_diagavg_obs'][:]  =  U_diagavg_obs; del  U_diagavg_obs
	plotdata_nc['V_diagavg_obs'][:]  =  V_diagavg_obs; del  V_diagavg_obs
	plotdata_nc['PS_diagavg_obs'][:] = PS_diagavg_obs; del PS_diagavg_obs
#	plotdata_nc['PW_diagavg_obs'][:] = PW_diagavg_obs; del PW_diagavg_obs
	
	plotdata_nc['Q_diagavg_use_obs'][:]  =  Q_diagavg_use_obs; del  Q_diagavg_use_obs
	plotdata_nc['T_diagavg_use_obs'][:]  =  T_diagavg_use_obs; del  T_diagavg_use_obs
	plotdata_nc['U_diagavg_use_obs'][:]  =  U_diagavg_use_obs; del  U_diagavg_use_obs
	plotdata_nc['V_diagavg_use_obs'][:]  =  V_diagavg_use_obs; del  V_diagavg_use_obs
	plotdata_nc['PS_diagavg_use_obs'][:] = PS_diagavg_use_obs; del PS_diagavg_use_obs
#	plotdata_nc['PW_diagavg_use_obs'][:] = PW_diagavg_use_obs; del PW_diagavg_use_obs
	
	
	plotdata_nc['Q_Ntotdiag'][:]  =  Q_Ntotdiag; del  Q_Ntotdiag
	plotdata_nc['T_Ntotdiag'][:]  =  T_Ntotdiag; del  T_Ntotdiag
	plotdata_nc['U_Ntotdiag'][:]  =  U_Ntotdiag; del  U_Ntotdiag
	plotdata_nc['V_Ntotdiag'][:]  =  V_Ntotdiag; del  V_Ntotdiag
	plotdata_nc['PS_Ntotdiag'][:] = PS_Ntotdiag; del PS_Ntotdiag
#	plotdata_nc['PW_Ntotdiag'][:] = PW_Ntotdiag; del PW_Ntotdiag
	
	plotdata_nc['Q_Nusediag'][:]  =  Q_Nusediag; del  Q_Nusediag
	plotdata_nc['T_Nusediag'][:]  =  T_Nusediag; del  T_Nusediag
	plotdata_nc['U_Nusediag'][:]  =  U_Nusediag; del  U_Nusediag
	plotdata_nc['V_Nusediag'][:]  =  V_Nusediag; del  V_Nusediag
	plotdata_nc['PS_Nusediag'][:] = PS_Nusediag; del PS_Nusediag
#	plotdata_nc['PW_Nusediag'][:] = PW_Nusediag; del PW_Nusediag
	
	##################
	plotdata_nc['Q_A_avg'][:]  =  Q_A_avg; del  Q_A_avg
	plotdata_nc['T_A_avg'][:]  =  T_A_avg; del  T_A_avg
	plotdata_nc['U_A_avg'][:]  =  U_A_avg; del  U_A_avg
	plotdata_nc['V_A_avg'][:]  =  V_A_avg; del  V_A_avg
	plotdata_nc['PS_A_avg'][:] = PS_A_avg; del PS_A_avg
#	plotdata_nc['PW_A_avg'][:] = PW_A_avg; del PW_A_avg
	
	plotdata_nc['Q_F_avg'][:]  =  Q_F_avg; del  Q_F_avg
	plotdata_nc['T_F_avg'][:]  =  T_F_avg; del  T_F_avg
	plotdata_nc['U_F_avg'][:]  =  U_F_avg; del  U_F_avg
	plotdata_nc['V_F_avg'][:]  =  V_F_avg; del  V_F_avg
	plotdata_nc['PS_F_avg'][:] = PS_F_avg; del PS_F_avg
#	plotdata_nc['PW_F_avg'][:] = PW_F_avg; del PW_F_avg
	##################
	plotdata_nc['Q_OmA_avg'][:]  =  Q_OmA_avg; del  Q_OmA_avg
	plotdata_nc['T_OmA_avg'][:]  =  T_OmA_avg; del  T_OmA_avg
	plotdata_nc['U_OmA_avg'][:]  =  U_OmA_avg; del  U_OmA_avg
	plotdata_nc['V_OmA_avg'][:]  =  V_OmA_avg; del  V_OmA_avg
	plotdata_nc['PS_OmA_avg'][:] = PS_OmA_avg; del PS_OmA_avg
#	plotdata_nc['PW_OmA_avg'][:] = PW_OmA_avg; del PW_OmA_avg
	
	plotdata_nc['Q_OmF_avg'][:]  =  Q_OmF_avg; del  Q_OmF_avg
	plotdata_nc['T_OmF_avg'][:]  =  T_OmF_avg; del  T_OmF_avg
	plotdata_nc['U_OmF_avg'][:]  =  U_OmF_avg; del  U_OmF_avg
	plotdata_nc['V_OmF_avg'][:]  =  V_OmF_avg; del  V_OmF_avg
	plotdata_nc['PS_OmF_avg'][:] = PS_OmF_avg; del PS_OmF_avg
#	plotdata_nc['PW_OmF_avg'][:] = PW_OmF_avg; del PW_OmF_avg
	##################
	plotdata_nc['Q_OmA_std'][:]  =  Q_OmA_std; del  Q_OmA_std
	plotdata_nc['T_OmA_std'][:]  =  T_OmA_std; del  T_OmA_std
	plotdata_nc['U_OmA_std'][:]  =  U_OmA_std; del  U_OmA_std
	plotdata_nc['V_OmA_std'][:]  =  V_OmA_std; del  V_OmA_std
	plotdata_nc['PS_OmA_std'][:] = PS_OmA_std; del PS_OmA_std
#	plotdata_nc['PW_OmA_std'][:] = PW_OmA_std; del PW_OmA_std
	
	plotdata_nc['Q_OmF_std'][:]  =  Q_OmF_std; del  Q_OmF_std
	plotdata_nc['T_OmF_std'][:]  =  T_OmF_std; del  T_OmF_std
	plotdata_nc['U_OmF_std'][:]  =  U_OmF_std; del  U_OmF_std
	plotdata_nc['V_OmF_std'][:]  =  V_OmF_std; del  V_OmF_std
	plotdata_nc['PS_OmF_std'][:] = PS_OmF_std; del PS_OmF_std
#	plotdata_nc['PW_OmF_std'][:] = PW_OmF_std; del PW_OmF_std
	
	
	##################
	##################
	##################
	##################
	##################
	
	
	plotdata_nc['Q_Asprd_avg'][:]  =  Q_Asprd_avg; del   Q_Asprd_avg
	plotdata_nc['T_Asprd_avg'][:]  =  T_Asprd_avg; del   T_Asprd_avg
	plotdata_nc['U_Asprd_avg'][:]  =  U_Asprd_avg; del   U_Asprd_avg
	plotdata_nc['V_Asprd_avg'][:]  =  V_Asprd_avg; del   V_Asprd_avg
	plotdata_nc['PS_Asprd_avg'][:] = PS_Asprd_avg; del  PS_Asprd_avg
#	plotdata_nc['PW_Asprd_avg'][:] = PW_Asprd_avg; del  PW_Asprd_avg
	
	plotdata_nc['Q_Fsprd_avg'][:]  =  Q_Fsprd_avg; del   Q_Fsprd_avg
	plotdata_nc['T_Fsprd_avg'][:]  =  T_Fsprd_avg; del   T_Fsprd_avg
	plotdata_nc['U_Fsprd_avg'][:]  =  U_Fsprd_avg; del   U_Fsprd_avg
	plotdata_nc['V_Fsprd_avg'][:]  =  V_Fsprd_avg; del   V_Fsprd_avg
	plotdata_nc['PS_Fsprd_avg'][:] = PS_Fsprd_avg; del  PS_Fsprd_avg
#	plotdata_nc['PW_Fsprd_avg'][:] = PW_Fsprd_avg; del  PW_Fsprd_avg
	
	##################
	
	plotdata_nc['Q_Asprd_std'][:]  = Q_Asprd_std; del  Q_Asprd_std
	plotdata_nc['T_Asprd_std'][:]  = T_Asprd_std; del  T_Asprd_std
	plotdata_nc['U_Asprd_std'][:]  = U_Asprd_std; del  U_Asprd_std
	plotdata_nc['V_Asprd_std'][:]  = V_Asprd_std; del  V_Asprd_std
	plotdata_nc['PS_Asprd_std'][:] =PS_Asprd_std; del PS_Asprd_std
#	plotdata_nc['PW_Asprd_std'][:] =PW_Asprd_std; del PW_Asprd_std
	
	plotdata_nc['Q_Fsprd_std'][:]  = Q_Fsprd_std; del  Q_Fsprd_std
	plotdata_nc['T_Fsprd_std'][:]  = T_Fsprd_std; del  T_Fsprd_std
	plotdata_nc['U_Fsprd_std'][:]  = U_Fsprd_std; del  U_Fsprd_std
	plotdata_nc['V_Fsprd_std'][:]  = V_Fsprd_std; del  V_Fsprd_std
	plotdata_nc['PS_Fsprd_std'][:] =PS_Fsprd_std; del PS_Fsprd_std
#	plotdata_nc['PW_Fsprd_std'][:] =PW_Fsprd_std; del PW_Fsprd_std
	#################
	###############
	plotdata_nc['Q_Asprderr_avg'][:]  = Q_Asprderr_avg; del  Q_Asprderr_avg
	plotdata_nc['T_Asprderr_avg'][:]  = T_Asprderr_avg; del  T_Asprderr_avg
	plotdata_nc['U_Asprderr_avg'][:]  = U_Asprderr_avg; del  U_Asprderr_avg
	plotdata_nc['V_Asprderr_avg'][:]  = V_Asprderr_avg; del  V_Asprderr_avg
	plotdata_nc['PS_Asprderr_avg'][:] =PS_Asprderr_avg; del PS_Asprderr_avg
#	plotdata_nc['PW_Asprderr_avg'][:] =PW_Asprderr_avg; del PW_Asprderr_avg
	
	plotdata_nc['Q_Fsprderr_avg'][:]  = Q_Fsprderr_avg; del  Q_Fsprderr_avg
	plotdata_nc['T_Fsprderr_avg'][:]  = T_Fsprderr_avg; del  T_Fsprderr_avg
	plotdata_nc['U_Fsprderr_avg'][:]  = U_Fsprderr_avg; del  U_Fsprderr_avg
	plotdata_nc['V_Fsprderr_avg'][:]  = V_Fsprderr_avg; del  V_Fsprderr_avg
	plotdata_nc['PS_Fsprderr_avg'][:] =PS_Fsprderr_avg; del PS_Fsprderr_avg
#	plotdata_nc['PW_Fsprderr_avg'][:] =PW_Fsprderr_avg; del PW_Fsprderr_avg
	#################
	###############
	plotdata_nc['Q_OmAens_avg'][:]  = Q_OmAens_avg; del  Q_OmAens_avg
	plotdata_nc['T_OmAens_avg'][:]  = T_OmAens_avg; del  T_OmAens_avg
	plotdata_nc['U_OmAens_avg'][:]  = U_OmAens_avg; del  U_OmAens_avg
	plotdata_nc['V_OmAens_avg'][:]  = V_OmAens_avg; del  V_OmAens_avg
	plotdata_nc['PS_OmAens_avg'][:] =PS_OmAens_avg; del PS_OmAens_avg
#	plotdata_nc['PW_OmAens_avg'][:] =PW_OmAens_avg; del PW_OmAens_avg
	
	plotdata_nc['Q_OmFens_avg'][:]  = Q_OmFens_avg; del  Q_OmFens_avg
	plotdata_nc['T_OmFens_avg'][:]  = T_OmFens_avg; del  T_OmFens_avg
	plotdata_nc['U_OmFens_avg'][:]  = U_OmFens_avg; del  U_OmFens_avg
	plotdata_nc['V_OmFens_avg'][:]  = V_OmFens_avg; del  V_OmFens_avg
	plotdata_nc['PS_OmFens_avg'][:] =PS_OmFens_avg; del PS_OmFens_avg
#	plotdata_nc['PW_OmFens_avg'][:] =PW_OmFens_avg; del PW_OmFens_avg
	################################
	plotdata_nc['Q_OmAens_std'][:]  = Q_OmAens_std; del  Q_OmAens_std
	plotdata_nc['T_OmAens_std'][:]  = T_OmAens_std; del  T_OmAens_std
	plotdata_nc['U_OmAens_std'][:]  = U_OmAens_std; del  U_OmAens_std
	plotdata_nc['V_OmAens_std'][:]  = V_OmAens_std; del  V_OmAens_std
	plotdata_nc['PS_OmAens_std'][:] =PS_OmAens_std; del PS_OmAens_std
#	plotdata_nc['PW_OmAens_std'][:] =PW_OmAens_std; del PW_OmAens_std
	
	plotdata_nc['Q_OmFens_std'][:]  = Q_OmFens_std; del  Q_OmFens_std
	plotdata_nc['T_OmFens_std'][:]  = T_OmFens_std; del  T_OmFens_std
	plotdata_nc['U_OmFens_std'][:]  = U_OmFens_std; del  U_OmFens_std
	plotdata_nc['V_OmFens_std'][:]  = V_OmFens_std; del  V_OmFens_std
	plotdata_nc['PS_OmFens_std'][:] =PS_OmFens_std; del PS_OmFens_std
#	plotdata_nc['PW_OmFens_std'][:] =PW_OmFens_std; del PW_OmFens_std
	
	################
	###################
	plotdata_nc['Plevels'][:] = pcutoffs; del pcutoffs	
	##########################################################################################
	##########################################################################################	
	plotdata_nc.close()
	del plotdata_nc
	del latindcs
	

nc_diagdata.close()










