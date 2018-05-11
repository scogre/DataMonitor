import sys
from create_annual_rad import create_annual_rad

if len(sys.argv) < 2:
    raise SystemExit('python make_rad_annual_all.py <stream start year> <data year>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
outpath='/lustre/f1/Scott.Gregory/FV3s'
regions=['GLOBL','TROPI','NORTH','SOUTH']
#instrmnt='AMSUA'
satlite='n15'

instrmnts=['hirs2','msu','avhrr3','hirs3','amsua','amsub','hirs4','mhs','ssmis','airs','atms','cris','seviri','iasi']  


hirs2_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
msu_channels    = [ 1, 2, 3, 4]
avhrr3_channels = [ 3, 4, 5]
hirs3_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
amsua_channels  = [ 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 15]
amsub_channels  = [ 1, 2, 3, 4, 5]
hirs4_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
mhs_channels    = [ 1, 2, 3, 4, 5]
ssmis_channels  = [ 1, 2, 3, 4, 5, 6, 7, 24]
airs_channels   = [   7,  15,  20,  21,  22,  27,  28,  40,  52,  69, \
                     72,  92,  93,  98,  99, 104, 105, 110, 111, 116, \
                    117, 123, 128, 129, 138, 139, 144, 145, 150, 151, \
                    156, 157, 162, 168, 169, 172, 173, 174, 175, 179, \
                    180, 185, 186, 190, 192, 198, 201, 204, 207, 210, \
                    215, 216, 221, 226, 227, 232, 252, 253, 256, 257, \
                    261, 262, 267, 272, 295, 299, 305, 310, 321, 325, \
                    333, 338, 355, 362, 375, 453, 475, 497, 528, 587, \
                    672, 787, 791, 870, 914, 950,1301,1304,1329,1371, \
                   1382,1415,1424,1449,1455,1477,1500,1519,1565,1574, \
                   1627,1669,1694,1766,1800,1826,1865,1866,1868,1869, \
                   1872,1873,1876,1881,1882,1911,1917,1918,1924,1928 ]
atms_channels   = [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, \
                   11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22]
cris_channels   = [  37,  49,  51,  53,  59,  61,  63,  64,  65,  67, \
                     69,  71,  73,  75,  79,  80,  81,  83,  85,  87, \
                     88,  89,  93,  95,  96,  99, 104, 106, 107, 116, \
                    120, 123, 124, 125, 126, 130, 132, 133, 136, 137, \
                    138, 142, 143, 144, 145, 147, 148, 150, 151, 153, \
                    154, 155, 157, 158, 159, 160, 161, 162, 163, 164, \
                    165, 166, 168, 170, 171, 173, 175, 198, 211, 224, \
                    279, 311, 342, 392, 404, 427, 464, 482, 501, 529, \
                    710, 713 ]
seviri_channels = [ 5, 6]
iasi_channels   = [  16,  38,  49,  51,  55,  57,  59,  61,  63,  66, \
                     70,  72,  74,  79,  81,  83,  85,  87, 104, 106, \
                    109, 111, 113, 116, 119, 122, 125, 128, 131, 133, \
                    135, 138, 141, 144, 146, 148, 151, 154, 157, 159, \
                    161, 163, 167, 170, 173, 176, 180, 185, 187, 193, \
                    199, 205, 207, 210, 212, 214, 217, 219, 222, 224, \
                    226, 230, 232, 236, 239, 243, 246, 249, 252, 254, \
                    260, 262, 265, 267, 269, 275, 282, 294, 296, 299, \
                    303, 306, 323, 327, 329, 335, 345, 347, 350, 354, \
                    356, 360, 366, 371, 373, 375, 377, 379, 381, 383, \
                    386, 389, 398, 401, 404, 407, 410, 414, 416, 426, \
                    428, 432, 434, 439, 445, 457, 515, 546, 552, 559, \
                    566, 571, 573, 646, 662, 668, 756, 867, 906, 921, \
                   1027,1046,1121,1133,1191,1194,1271,1479,1509,1513, \
                   1521,1536,1574,1579,1585,1587,1626,1639,1643,1652, \
                   1658,1671,1786,1805,1884,1991,2019,2094,2119,2213, \
                   2239,2271,2321,2398,2701]


for instrmnt in instrmnts:
   channelsname=instrmnt+'_channels'
   channels=eval(channelsname)
   print 'channels_name,channels=', channelsname,channels
   for reg in regions:
      create_annual_rad(outpath, streamyr, datayr, instrmnt, channels, satlite, reg)
   del channels


#FV3s2003
#amsua_n15
#amsua_n16
#amsub_n15
#amsub_n16
#amsub_n17
#avhrr_n16
#avhrr_n17
#hirs2_n14
#hirs3_n16
#hirs3_n17
#msu_n14
#sbuv2_n16
#sndr_g08


#FV3s2007
#airs_aqua
#amsua_aqua
#amsua_n15
#amsua_n18
#amsub_n15
#amsub_n16
#amsub_n17
#hirs3_n17
#mhs_n18
#sbuv2_n17
#sbuv2_n18
#sndr_g11   ??????????


#FV3s2011                   
#airs_aqua
#amsua_aqua
#amsua_metop-a
#amsua_n15
#amsua_n18
#amsua_n19
#avhrr_metop-a
#avhrr_n18
#hirs3_n17
#hirs4_metop-a
#hirs4_n19
#iasi_metop-a
#mhs_metop-a
#mhs_n18
#mhs_n19
#omi_aura
#sbuv2_n18
#sbuv2_n19


#FV3s2015                   
#airs_aqua                   
#amsua_aqua                   
#amsua_metop-a
#amsua_metop-b
#amsua_n15
#amsua_n18                   
#atms_npp                   
#avhrr_metop-a
#avhrr_n18
#cris_npp
#hirs4_metop-a
#iasi_metop-a
#mhs_metop-a
#mhs_metop-b
#mhs_n18
#mhs_n19
#omi_aura
#sbuv2_n19
#seviri_m10
