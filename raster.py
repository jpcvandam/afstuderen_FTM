#script om een raster met GDAL te bevragen
#auteur: John van Dam
#Datum: 15 september 2015

import subprocess
x= "6.510"
y= "53.156"

berg = subprocess.check_output(["gdallocationinfo","-valonly", "/home/john/ftm/ftm/ftm/data/Bergingscoefficient.tif", x, y])
print berg

drainw = subprocess.check_output(["gdallocationinfo","-valonly", "/home/john/ftm/ftm/ftm/data/Drainageweerstand.tif", x, y])
print drainw
q_bot = subprocess.check_output(["gdallocationinfo","-valonly", "/home/john/ftm/ftm/ftm/data/Kwel-kk-nz.tif", x, y])
print q_bot
ontw = subprocess.check_output(["gdallocationinfo","-valonly", "/home/john/ftm/ftm/ftm/data/Ontwateringsbasis.tif", x, y])
print ontw
