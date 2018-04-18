from netCDF4 import Dataset
import numpy as np
import sys, os


if len(sys.argv) < 4:
    raise SystemExit('python merge_diag_convvarbs.py <date> <input conv path> <output file path>')

# file names from command line args.
rundate = sys.argv[1]
conv_filepath = sys.argv[2]
out_filename = sys.argv[3]

nan=float('nan')

obcol_dict={}
obcol_dict['q'] = 0
obcol_dict['t'] = 1
obcol_dict['u'] = 2
obcol_dict['v'] = 3
obcol_dict['ps'] = 4
Ncol=len(obcol_dict)


varbs=['q','t','uv','ps']
nobs_temp=nan*np.ones(len(varbs))
for mm in range(len(varbs)):
   varb=varbs[mm]
   controlnc_file = conv_filepath+'diag_conv_'+varb+'_anl.'+rundate+'_control.nc4'
   print 'file=',controlnc_file
   nc_diagdata = Dataset(controlnc_file,'r')
   gsierr=nc_diagdata['Errinv_Final'][:]
   nobs_temp[mm]=len(gsierr)
   rowtotal=np.sum(nobs_temp[0:mm+1])
   print 'rowtotal=',rowtotal
   nc_diagdata.close()
nobs_diag=int(np.sum(nobs_temp))
ndiag_obd = int(Ncol)

gsi_hx_Aarray = nan*np.ones((nobs_diag,ndiag_obd))
gsi_hx_Farray = nan*np.ones((nobs_diag,ndiag_obd))
gsierrarray = nan*np.ones((nobs_diag,ndiag_obd))
gsiusearray = nan*np.ones((nobs_diag,ndiag_obd))
gsiobsarray = nan*np.ones((nobs_diag,ndiag_obd))
gsiensobsarray = nan*np.ones((nobs_diag,ndiag_obd))
gsipressarray = nan*np.ones((nobs_diag,ndiag_obd))
#gsipressarray = -99999*np.ones((nobs_diag,ndiag_obd))
gsilatarray = nan*np.ones(nobs_diag)
gsilonarray = nan*np.ones(nobs_diag)
gsi_hx_Aensarray = nan*np.ones((nobs_diag,ndiag_obd))
gsi_hx_Fensarray = nan*np.ones((nobs_diag,ndiag_obd))
gsi_hx_Asprdarray = nan*np.ones((nobs_diag,ndiag_obd))
gsi_hx_Fsprdarray = nan*np.ones((nobs_diag,ndiag_obd))
gsiENSusearray = nan*np.ones((nobs_diag,ndiag_obd))


#	float EnKF_fit_ges(nobs) ;
#	float EnKF_spread_ges(nobs) ;
#	float EnKF_fit_anl(nobs) ;
#	float EnKF_spread_anl(nobs) ;



rowtotal=0
for mm in range(len(varbs)):
   rowstart=rowtotal
   rowtotal=int(np.sum(nobs_temp[0:mm+1]))
   varb=varbs[mm]

   controlnc_file = conv_filepath+'diag_conv_'+varb+'_anl.'+rundate+'_control.nc4'
   nc_diagdata = Dataset(controlnc_file,'r')
   ensmeannc_file = conv_filepath+'diag_conv_'+varb+'_ges.'+rundate+'_ensmean.nc4'
   nc_ensdata = Dataset(ensmeannc_file,'r')
   enssprdnc_file = conv_filepath+'diag_conv_'+varb+'_ges.ensmean_spread.nc4'
   nc_sprddata = Dataset(enssprdnc_file,'r')

   #####################
   if varb=='uv':
      obcol_u = obcol_dict['u']
      gsiobsarray[rowstart:rowtotal,obcol_u]=nc_diagdata['u_Observation'][:]
#      print 'gsiobsarray',gsiobsarray

      gsi_hx_Aarray[rowstart:rowtotal,obcol_u]= gsiobsarray[rowstart:rowtotal,obcol_u] - nc_diagdata['u_Obs_Minus_Forecast_adjusted'][:]
      gsi_hx_Farray[rowstart:rowtotal,obcol_u]= gsiobsarray[rowstart:rowtotal,obcol_u] - nc_ensdata['u_Obs_Minus_Forecast_adjusted'][:] 
      gsiensobsarray[rowstart:rowtotal,obcol_u]= nc_ensdata['u_Observation'][:]                                            
#      print 'gsiensobsarray',gsiensobsarray
#      gsi_hx_Aensarray[rowstart:rowtotal,obcol_u]= gsiensobsarray[rowstart:rowtotal,obcol_u] - nc_ensdata['u_Obs_Minus_Forecast_adjusted'][:]
#      gsi_hx_Fensarray[rowstart:rowtotal,obcol_u]= gsiensobsarray[rowstart:rowtotal,obcol_u] - nc_ensdata['u_Obs_Minus_Forecast_adjusted'][:]
      gsi_hx_Aensarray[rowstart:rowtotal,obcol_u]= gsiensobsarray[rowstart:rowtotal,obcol_u] - nc_sprddata['u_EnKF_fit_anl'][:] 
      gsi_hx_Fensarray[rowstart:rowtotal,obcol_u]= gsiensobsarray[rowstart:rowtotal,obcol_u] - nc_sprddata['u_EnKF_fit_ges'][:] 

      gsiENSusearray[rowstart:rowtotal,obcol_u]=nc_sprddata['u_EnKF_use_flag'][:] ##ENS                                     ##### U,V
      gsi_hx_Asprdarray[rowstart:rowtotal,obcol_u]=np.sqrt(nc_sprddata['u_EnKF_spread_anl'][:])                                     ##### U,V
      gsi_hx_Fsprdarray[rowstart:rowtotal,obcol_u]=np.sqrt(nc_sprddata['u_EnKF_spread_ges'][:])                                     ##### U,V

#      gsierrarray[rowstart:rowtotal,obcol_u]=nc_diagdata['Errinv_Final'][:]
      gsierrarray[rowstart:rowtotal,obcol_u]=(((nc_diagdata['Errinv_Final'][:])**2)**-1)
      print 'gsierrarray[rowstart:rowtotal,obcol_u]=',gsierrarray[rowstart:rowtotal,obcol_u]
#      gsiusearray[rowstart:rowtotal,obcol_u]=nc_diagdata['Prep_Use_Flag'][:]
      gsiusearray[rowstart:rowtotal,obcol_u]=nc_diagdata['Analysis_Use_Flag'][:]
      gsipressarray[rowstart:rowtotal,obcol_u]=nc_diagdata['Pressure'][:]
      gsilatarray[rowstart:rowtotal]=nc_diagdata['Latitude'][:]
      gsilonarray[rowstart:rowtotal]=nc_diagdata['Longitude'][:]

      #####    U and V will share rows
      obcol_v = obcol_dict['v']
      gsiobsarray[rowstart:rowtotal,obcol_v]=nc_diagdata['v_Observation'][:]                                               ##### U,V

      gsi_hx_Aarray[rowstart:rowtotal,obcol_v]= gsiobsarray[rowstart:rowtotal,obcol_v] - nc_diagdata['v_Obs_Minus_Forecast_adjusted'][:] ##ANL             ##### U,V
      gsi_hx_Farray[rowstart:rowtotal,obcol_v]= gsiobsarray[rowstart:rowtotal,obcol_v] - nc_ensdata['v_Obs_Minus_Forecast_adjusted'][:] ##GES             ##### U,V

      gsiensobsarray[rowstart:rowtotal,obcol_v]= nc_ensdata['v_Observation'][:]                                               ##### U,V
#      gsi_hx_Aensarray[rowstart:rowtotal,obcol_v]= gsiensobsarray[rowstart:rowtotal,obcol_v] - nc_ensdata['v_Obs_Minus_Forecast_adjusted'][:]              ##### U,V
#      gsi_hx_Fensarray[rowstart:rowtotal,obcol_v]= gsiensobsarray[rowstart:rowtotal,obcol_v] - nc_ensdata['v_Obs_Minus_Forecast_adjusted'][:]              ##### U,V
      gsi_hx_Aensarray[rowstart:rowtotal,obcol_v]= gsiensobsarray[rowstart:rowtotal,obcol_v] - nc_sprddata['v_EnKF_fit_anl'][:]             ##### U,V
      gsi_hx_Fensarray[rowstart:rowtotal,obcol_v]= gsiensobsarray[rowstart:rowtotal,obcol_v] - nc_sprddata['v_EnKF_fit_ges'][:]              ##### U,V

      gsiENSusearray[rowstart:rowtotal,obcol_v]=nc_sprddata['v_EnKF_use_flag'][:] ##ENS                                     ##### U,V
      gsi_hx_Asprdarray[rowstart:rowtotal,obcol_v]=np.sqrt(nc_sprddata['v_EnKF_spread_anl'][:])                                     ##### U,V
      gsi_hx_Fsprdarray[rowstart:rowtotal,obcol_v]=np.sqrt(nc_sprddata['v_EnKF_spread_ges'][:])                                    ##### U,V

#      gsierrarray[rowstart:rowtotal,obcol_v]=nc_diagdata['Errinv_Final'][:]
      gsierrarray[rowstart:rowtotal,obcol_v]=(((nc_diagdata['Errinv_Final'][:])**2)**-1)
      print 'gsierrarray[rowstart:rowtotal,obcol_v]=',gsierrarray[rowstart:rowtotal,obcol_v]
#      gsiusearray[rowstart:rowtotal,obcol_v]=nc_diagdata['Prep_Use_Flag'][:]
      gsiusearray[rowstart:rowtotal,obcol_v]=nc_diagdata['Analysis_Use_Flag'][:]
      gsipressarray[rowstart:rowtotal,obcol_v]=nc_diagdata['Pressure'][:]

   else:
      print('obtype=',varb)
      obcol = obcol_dict[varb]
      print('rowstart=',rowstart)
      print('rowtotal=',rowtotal)
      print('obcol=',obcol)
      if varb == 't':
         addtovarb = -273.15
         multvarb = 1.0
      elif varb == 'q':
         addtovarb = 0
         multvarb = 1e6
      else:
         addtovarb = 0
         multvarb =1.0

      dummy4length=nc_diagdata['Observation'][:]
      addarray = addtovarb*np.ones(len(dummy4length))
      multarray = multvarb*np.ones(len(dummy4length))

      gsiobsarray[rowstart:rowtotal,obcol]=  multarray * nc_diagdata['Observation'][:] + addarray                   ##### U,V

      gsi_hx_Aarray[rowstart:rowtotal,obcol]= gsiobsarray[rowstart:rowtotal,obcol] - (multarray * nc_diagdata['Obs_Minus_Forecast_adjusted'][:]) ##ANL             ##### U,V
      gsi_hx_Farray[rowstart:rowtotal,obcol]= gsiobsarray[rowstart:rowtotal,obcol] - (multarray * nc_ensdata['Obs_Minus_Forecast_adjusted'][:]) ##GES             ##### U,V

      gsiensobsarray[rowstart:rowtotal,obcol]= multarray * nc_ensdata['Observation'][:] + addarray                                              ##### U,V
#      gsi_hx_Aensarray[rowstart:rowtotal,obcol]= gsiensobsarray[rowstart:rowtotal,obcol] - (multarray * nc_ensdata['Obs_Minus_Forecast_adjusted'][:])              ##### U,V
#      gsi_hx_Fensarray[rowstart:rowtotal,obcol]= gsiensobsarray[rowstart:rowtotal,obcol] - (multarray * nc_ensdata['Obs_Minus_Forecast_adjusted'][:])              ##### U,V
      gsi_hx_Aensarray[rowstart:rowtotal,obcol]= gsiensobsarray[rowstart:rowtotal,obcol] - (multarray * nc_sprddata['EnKF_fit_anl'][:])             ##### U,V
      gsi_hx_Fensarray[rowstart:rowtotal,obcol]= gsiensobsarray[rowstart:rowtotal,obcol] - (multarray * nc_sprddata['EnKF_fit_ges'][:])              ##### U,V

      gsiENSusearray[rowstart:rowtotal,obcol]=nc_sprddata['EnKF_use_flag'][:] ##ENS                    ##### U,V
      gsi_hx_Asprdarray[rowstart:rowtotal,obcol]= np.sqrt(multarray * nc_sprddata['EnKF_spread_anl'][:])        ##### U,V
      gsi_hx_Fsprdarray[rowstart:rowtotal,obcol]= np.sqrt(multarray * nc_sprddata['EnKF_spread_ges'][:])        ##### U,V

      gsierrarray[rowstart:rowtotal,obcol]=((((nc_diagdata['Errinv_Final'][:])/multarray)**2)**-1)
      print 'gsierrarray[rowstart:rowtotal,obcol]=',gsierrarray[rowstart:rowtotal,obcol]
      gsiusearray[rowstart:rowtotal,obcol]=nc_diagdata['Analysis_Use_Flag'][:]
      gsipressarray[rowstart:rowtotal,obcol]=nc_diagdata['Pressure'][:]
      gsilatarray[rowstart:rowtotal]=nc_diagdata['Latitude'][:]
      gsilonarray[rowstart:rowtotal]=nc_diagdata['Longitude'][:]
      
      del addtovarb
      del multvarb

print('FINISHED')


#############################################################################
#############################################################################
#############################################################################

# file names from command line args.
#ncOUTfilename = sys.argv[1]
#ncOUTfilename = 'testing123.nc'
ncOUTfilename = out_filename

#if len(sys.argv) < 4:
#    raise SystemExit('python prep_diag2nc.py <nc filename> <input gsi anl diag> <input gsi ges diag> ')
nc_mergeddiagdata = Dataset(ncOUTfilename,'w')
varbs=['q','t','uv','ps']

diag_varbstr='QOB TOB UOB VOB PRSS'
diag_errstr='QOE TOE UOE VOE POE'
diag_qcstr='QQM TQM UQM VQM PQM'
diag_obs = nc_mergeddiagdata.createDimension('diaginfo',int(Ncol))
nobsd = nc_mergeddiagdata.createDimension('nobs',None)

#######################
gsi_hx_A =\
nc_mergeddiagdata.createVariable('gsi_hx_A',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsi_hx_F =\
nc_mergeddiagdata.createVariable('gsi_hx_F',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsierr =\
nc_mergeddiagdata.createVariable('gsierr',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiuse =\
nc_mergeddiagdata.createVariable('gsiuse',np.uint8,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiobs =\
nc_mergeddiagdata.createVariable('gsiobs',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsipress =\
nc_mergeddiagdata.createVariable('gsipress',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsilat =\
nc_mergeddiagdata.createVariable('gsilat',np.float32,('nobs',),zlib=False)

gsilon =\
nc_mergeddiagdata.createVariable('gsilon',np.float32,('nobs',),zlib=False)

#########
gsi_hx_Aens =\
nc_mergeddiagdata.createVariable('gsi_hx_Aens',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsi_hx_Fens =\
nc_mergeddiagdata.createVariable('gsi_hx_Fens',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsi_hx_Asprd =\
nc_mergeddiagdata.createVariable('gsi_hx_Asprd',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsi_hx_Fsprd =\
nc_mergeddiagdata.createVariable('gsi_hx_Fsprd',np.float32,('nobs','diaginfo'),\
zlib=True,chunksizes=(nobs_diag,ndiag_obd))

gsiENSuse =\
nc_mergeddiagdata.createVariable('gsiENSuse',np.uint8,('nobs','diaginfo'),\
fill_value=255,zlib=True,chunksizes=(nobs_diag,ndiag_obd))
#########
#############################################################################


gsi_hx_A.diaginfo = diag_varbstr
gsi_hx_F.diaginfo = diag_varbstr
gsierr.diaginfo = diag_errstr
gsiuse.diaginfo = diag_qcstr

gsi_hx_A.desc = 'gsi analysis data (model analysis in observation space)'
gsi_hx_F.desc = 'gsi guess data (model guess in observation space)'
gsierr.desc = 'observation errors used by GSI'
gsiuse.desc = 'gsi QC flags (1: used, 0: not used)'

gsi_hx_Aens.diaginfo = diag_varbstr
gsi_hx_Fens.diaginfo = diag_varbstr
gsi_hx_Asprd.diaginfo = diag_varbstr
gsi_hx_Fsprd.diaginfo = diag_varbstr
gsiENSuse.diaginfo = diag_qcstr
gsi_hx_Aens.desc = 'gsi analysis ens mean'
gsi_hx_Fens.desc = 'gsi 1st guess ens mean'
gsi_hx_Asprd.desc = 'gsi analysis ens spread'
gsi_hx_Fsprd.desc = 'gsi 1st guess ens spread'
gsiENSuse.desc = 'gsi ensemble QC flags (1: used, 0: not used)'
#############################################################################
#############################################################################
#############################################################################

nc_mergeddiagdata['gsi_hx_A'][:] = gsi_hx_Aarray[:]
nc_mergeddiagdata['gsierr'][:] = gsierrarray[:]
nc_mergeddiagdata['gsiuse'][:] =  gsiusearray[:]
nc_mergeddiagdata['gsi_hx_F'][:] = gsi_hx_Farray[:]
nc_mergeddiagdata['gsiobs'][:] =  gsiobsarray[:]
nc_mergeddiagdata['gsipress'][:] =  gsipressarray[:]
nc_mergeddiagdata['gsilat'][:] =  gsilatarray[:]
nc_mergeddiagdata['gsilon'][:] =  gsilonarray[:]
nc_mergeddiagdata['gsi_hx_Aens'][:] = gsi_hx_Aensarray[:]
nc_mergeddiagdata['gsi_hx_Fens'][:] = gsi_hx_Fensarray[:]
nc_mergeddiagdata['gsi_hx_Asprd'][:] = gsi_hx_Asprdarray[:]
nc_mergeddiagdata['gsi_hx_Fsprd'][:] = gsi_hx_Fsprdarray[:]
nc_mergeddiagdata['gsiENSuse'][:] =  gsiENSusearray[:]

nc_mergeddiagdata.close()
