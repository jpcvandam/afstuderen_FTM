#script om een raster met GDAL te bevragen
#auteur: John van Dam
#Datum: 15 september 2015

import subprocess

def raster_q(bestand, x1, y1):
    waarde = subprocess.check_output(["gdallocationinfo","-valonly","-geoloc", bestand, x1, y1])
    return waarde


x= "6.4569"
y= "53.2149"

berg = subprocess.check_output(["gdallocationinfo","-valonly","-geoloc", "/home/john/ftm/ftm/ftm/data/Bergingscoefficient1.tif", x, y])
print berg

drainw = subprocess.check_output(["gdallocationinfo","-valonly", "-geoloc","/home/john/ftm/ftm/ftm/data/Drainageweerstand1.tif", x, y])
print drainw
q_bot = subprocess.check_output(["gdallocationinfo","-valonly","-geoloc", "/home/john/ftm/ftm/ftm/data/Kwel-kk-nz1.tif", x, y])
print q_bot
ontw = subprocess.check_output(["gdallocationinfo","-valonly","-geoloc", "/home/john/ftm/ftm/ftm/data/Ontwateringsbasis1.tif", x, y])
print ontw

print raster_q("/home/john/ftm/ftm/ftm/data/Drainageweerstand1.tif", x, y)
