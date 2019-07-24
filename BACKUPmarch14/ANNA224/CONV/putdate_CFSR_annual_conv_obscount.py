from netCDF4 import Dataset
import numpy as np
import os
import read_diag

def putdate_CFSR_annual_conv_obscount(diagpath, date, outputpath):
   #######################################
   fname_ges = diagpath+'/'+str(date)+'/diag_conv_ges.'+str(date)
   print 'fname ges=',fname_ges
   if (not os.path.isfile(fname_ges) or os.stat(fname_ges).st_size == 0):
      print '--- conventional data not available for ', date
      return
   diag_ctrl_f = read_diag.diag_conv(fname_ges,endian='big',fformat='old')
   diag_ctrl_f.read_obs()

   nobs_all = diag_ctrl_f.nobs

   diagvarnames = ['  t',  '  u', '  q', ' ps']
   varnames     = [  't',   'uv',   'q',  'ps']
   obvar = diag_ctrl_f.obtype
   obtype = diag_ctrl_f.code
   gsi_used  = diag_ctrl_f.used

   for ivar in range(len(varnames)):
     varidx = diagvarnames[ivar] == obvar

     outfile = outputpath+'/CONV_CFSR_'+str(date)[0:4]+'_'+varnames[ivar].strip()+'_obscounts.nc'
     print outfile
     anndata = Dataset(outfile, 'a')
     alldate=anndata['All_Dates']
     idate = np.nonzero(alldate[:]==int(date))[0][0]
     anndata['Full_Dates'][idate] = int(date)

     useidx  = np.logical_and(varidx, gsi_used == 1)
     acftindx = np.logical_and(useidx, np.in1d(obtype, [130,131,133,134,135,230,231,233,234,235]))
     sfcindx  = np.logical_and(useidx, np.in1d(obtype, [180,181,182,183,187,192,193,194,280,282,284,294,281,287,288,292,293,295]))
     sondindx = np.logical_and(useidx, np.in1d(obtype, [120, 122, 132,220,221,222,232]))
     profindx = np.logical_and(useidx, np.in1d(obtype, [223,224,227,228,229]))
     satwndindx = np.logical_and(useidx, np.in1d(obtype, [np.arange(240,261)]))
     scatwndindx = np.logical_and(useidx, np.in1d(obtype,[283, 284, 285, 286,289, 290, 291]))

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

