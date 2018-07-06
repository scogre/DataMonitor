import sys
from create_annual_rad import create_annual_rad
###python make_rad_annual_CFSR.py 1999 1999 /lfs3/projects/gfsenkf/Scott.Gregory/CFSR/
if len(sys.argv) < 2:
    raise SystemExit('python make_rad_annual_CFSR.py <stream start year> <data year> <output path>')
streamyr = int(sys.argv[1])
datayr = int(sys.argv[2])
outputpath = sys.argv[3]
regions=['GLOBL','TROPI','NORTH','SOUTH']


instrmnts=['airs', 'amsua',  'amsua',  'amsua','amsua', 'amsua', 'amsua', 'amsua', 'amsub', 'amsub', 'amsub', 'atms' , 'avhrr'  , 'avhrr', 'avhrr', 'avhrr', 'avhrr', 'cris', 'hirs2' , 'hirs3', 'hirs3', 'hirs4'   , 'hirs4' , 'iasi'   ,    'mhs',     'mhs', 'mhs' , 'mhs', 'msu', 'seviri', 'sndr', 'sndr']
satlites=[ 'aqua', 'aqua' ,'metop-a','metop-b','n15'  , 'n16'  , 'n18'  , 'n19'  , 'n15'  , 'n16'  , 'n17'  , 'npp'  , 'metop-a', 'n15'  , 'n16'  , 'n17'  , 'n18'  , 'npp' , 'n14'   , 'n16'  , 'n17'  , 'metop-a' , 'n19'   , 'metop-a','metop-a', 'metop-b', 'n18' , 'n19', 'n14',  'm10'  , 'g08' , 'g11' ]


    
hirs2_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
msu_channels    = [ 1, 2, 3, 4]
avhrr_channels = [ 3, 4, 5]
hirs3_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
amsua_channels  = [ 1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 15]
amsub_channels  = [ 1, 2, 3, 4, 5]
hirs4_channels  = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
sndr_channels   = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
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

numinst=len(instrmnts)
#for instrmnt in instrmnts:
for nn in range(numinst):
   instrmnt=instrmnts[nn]
   satlite=satlites[nn]
   channelsname=instrmnt+'_channels'
   channels=eval(channelsname)
   print 'channels_name,channels=', channelsname,channels
   for region in regions:
      outfile=outputpath+'/RAD_CFSR_'+str(datayr)+'_'+instrmnt+'_'+satlite+'_'+region+'.nc'
      create_annual_rad(outfile, streamyr, datayr, instrmnt, channels, satlite, region)
   del channels



