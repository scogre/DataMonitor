from putdate_annual_rad import putdate_annual_rad

diagpath='/lustre/f1/Oar.Esrl.Nggps_psd/2003stream/'
date=2003030206
instrmnt='amsua'
satlite='n15'
latrange=[-90, 90]
outfile='/lustre/f1/Scott.Gregory/FV3s2003/FV3s2003_2003_AMSUA_n15_GLOBL.nc'

putdate_annual_rad(diagpath, date, instrmnt, satlite, latrange, outfile)



