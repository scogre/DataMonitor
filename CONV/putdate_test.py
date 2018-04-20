from putdate_annual_conv import putdate_annual_conv

diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/2003stream/'
date=2003010206
var='ps'
diagpref='aaa'
latrange=[-90, 90]
outfile='/lustre/f1/Scott.Gregory/FV3s2003/FV3s2003_2003_PS_GLOBL.nc'

putdate_annual_conv(diagpath, date, var, diagpref, latrange, outfile)





