from netCDF4 import Dataset
import numpy as np
import os

def putdate_annual_conv_obscount(diagpath, date, stream, var, outputpath):

   fname = diagpath+'/'+str(date)+'/diag_conv_'+var+'_ges.'+str(date)+'_control.nc4'
   if (not os.path.isfile(fname)):
      print '---', var, ' not available for ', date
      return
   diag_ctrl_f = Dataset(fname,'r')
     
   print 'Filling in ', var , ' for ', date

   nobs = len(diag_ctrl_f.dimensions['nobs'])
   obtype = diag_ctrl_f['Observation_Type']
   gsi_used  = diag_ctrl_f['Analysis_Use_Flag'][:]

   outfile = outputpath+'/CONV_'+stream+'_'+str(date)[0:4]+'_'+var+'_obscounts.nc'
   anndata = Dataset(outfile, 'a')
   alldate=anndata['All_Dates']
   idate = np.nonzero(alldate[:]==int(date))[0][0]
   anndata['Full_Dates'][idate] = int(date)

   useidx  = (gsi_used == 1)
   acftindx = np.logical_and(useidx, np.isin(obtype, [130,131,133,134,135,230,231,233,234,235]))
   sfcindx  = np.logical_and(useidx, np.isin(obtype, [180,181,182,183,187,192,193,194,280,282,284,294,281,287,288,292,293,295]))
   sondindx = np.logical_and(useidx, np.isin(obtype, [120, 122, 132,220,221,222,232]))
   profindx = np.logical_and(useidx, np.isin(obtype, [223,224,227,228,229]))
   satwndindx = np.logical_and(useidx, np.isin(obtype, [np.arange(240,261)]))
   scatwndindx = np.logical_and(useidx, np.isin(obtype,[283, 284, 285, 286,289, 290, 291]))

   print np.unique(obtype)
   nobs_all  = len(obtype[useidx])
   nobs_acft = len(obtype[acftindx])
   nobs_sfc  = len(obtype[sfcindx])
   nobs_sond = len(obtype[sondindx])
   nobs_prof = len(obtype[profindx])
   nobs_satw = len(obtype[satwndindx])
   nobs_scatw = len(obtype[scatwndindx])
   nobs_other = nobs_all - nobs_acft - nobs_sfc - nobs_sond - nobs_prof - nobs_satw - nobs_scatw
   anndata['nobs_used'][idate]  = nobs_all
   anndata['nobs_acft'][idate]  = nobs_acft
   anndata['nobs_sfc'][idate]   = nobs_sfc
   anndata['nobs_sond'][idate]  = nobs_sond
   anndata['nobs_prof'][idate]  = nobs_prof
   anndata['nobs_satw'][idate]  = nobs_satw
   anndata['nobs_scatw'][idate] = nobs_scatw
   anndata['nobs_other'][idate] = nobs_other
   print nobs_all, ', acft=', nobs_acft, ', sfc=', nobs_sfc, ', sonde=', nobs_sond, ', prof=', nobs_prof, ', satw=', nobs_satw, ', scatw=', nobs_scatw, ', other=', nobs_other 
   anndata.close()	
