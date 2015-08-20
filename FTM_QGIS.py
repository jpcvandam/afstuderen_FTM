#code om het Python FTM in QGIS te kunnen runnen
#Auteur: John van Dam
#Datum 20 augustus 2015
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
import datetime
import matplotlib.dates as mdates
import datetime as dt
from numpy.numarray.functions import value
import matplotlib.dates as mdates

#Functiedefinities, hier staan dus de echte rekenmodules
def delta(bergingscoefficient, drainageweerstand) :
    delta = np.exp(-1.0 /( bergingscoefficient * drainageweerstand))
    return(delta)


def omega(drainageweerstand, bergingscoefficient): 
    omega = drainageweerstand * (1.0 - delta(bergingscoefficient, drainageweerstand))
    return(omega)


def cw(drainageweerstand, qbot, hgem):
    cw = ((drainageweerstand * (qbot/10))*1) + hgem
    return(cw)


def gws_op_t(bergingscoefficient, drainageweerstand, ht_dt,  qbot, hgem, Pt) :
    ht = cw(drainageweerstand, qbot, hgem) + delta(bergingscoefficient, drainageweerstand) * (ht_dt - cw(drainageweerstand, qbot, hgem)) + omega(drainageweerstand, bergingscoefficient) * Pt
    if ht<0:
        return ht
    else:
        return 0
    

meteobestand='/home/john/Documenten/FTM/HyGis/QGIS/METEO669.TXT'

dfMeteo=pd.read_fwf(meteobestand, widths=[14,14,14,14,14], header = None, names = ['dag', 'maand' , 'jaar' ,'neerslag' , 'verdamping'], parse_dates={"Datetime" : [0,1,2]})
dfMeteo = dfMeteo.set_index('Datetime')
dfMeteo_out = pd.Series(dfMeteo.neerslag-dfMeteo.verdamping)
#dfMeteo_out['neerslagoverschot']=dfMeteo.neerslag-dfMeteo.verdamping
#print dfMeteo_out #print was alleen om de zaak te testen
meteobestand_uit = 'Meteo_out.csv'
dfMeteo_out.to_csv(meteobestand_uit,  index=True, sep=',', header=True)

array_neerslagoverschot = dfMeteo_out.values
#haal bodemdata
#haal meteo
#doe daar iets mee

output_file = open('/home/john/Documenten/FTM/HyGis/QGIS/Bodemdata.txt', 'w')
#line = '%s\n' % ("#runn        al     hgem  drainw    berg    qbot  ")
#unicode_line = line.encode('utf-8')
#output_file.write(unicode_line)
layer = iface.activeLayer()
features = layer.selectedFeatures()
for f in features:
#for f in layer.getFeatures():
#  geom = f.geometry()
#  print f['id'], f['berg']
  runn = 1
  al = 365
  hgem = f['ontwbasis'] * -1
  drainw = f['drainwtot']
  berg = f['bergcoef10'] / 100
  qbot = f['kwel10'] / 10

  print f['kwel10']


#  line = '%8.0f%8.0f%8.0f%8.0f%8.3f%8.3f\n' % (f['runn'],f['al'],
#         f['hgem'],f['drainw'],f['berg'],f['qbot'])
  line = '%f,%f,%f,%f,%f,%f\n' % (runn,al,
         hgem,drainw,berg,qbot)
#          geom.asPoint().y(), geom.asPoint().x())
  print line
  unicode_line = line.encode('utf-8')
  output_file.write(unicode_line)
output_file.close()


bodembestand = '/home/john/Documenten/FTM/HyGis/QGIS/Bodemdata.txt'
dfBodem=pd.read_csv(bodembestand, header=None, delimiter =',', names = ['#runn', 'al', 'hgem', 'drainw', 'berg', 'qbot' ]) #names = ['#runn', 'al', 'hgem', 'drainw', 'berg', 'qbot' ]
#print dfBodem #print was alleen om de zaak te testen

array_drainweerstand = dfBodem['drainw'].values
array_hgem = dfBodem['hgem'].values
array_bergingscoefficient = dfBodem['berg'].values
array_qbot = dfBodem['qbot'].values

# GHG en GLG uit textbestand halen Jvd: GHG en GLG moeten door dit programma worden berekend
#fileinput = open('/home/john/Documenten/FTM/HyGis/QGIS/testgwlstatistics.txt', 'r')
#fileinput.readline()
#fileinput.readline()
#for line in fileinput:
#print fileinput.read(4),
#fileinput.read(4),
#GHG = fileinput.read(8)
#fileinput.readline()
#fileinput.readline()
#fileinput.read(4),
#GLG = fileinput.read(8)
#fileinput.close()


#fileinput = open('/home/john/Documenten/FTM/HyGis/QGIS/testgwlstatistics.txt', 'r')
#print(fileinput.readline()),
#print(fileinput.readline())
#fileinput.readline()
#fileinput.readline()

array_grondwaterstand = np.zeros(shape = (11323), order='C')
#print array_grondwaterstand #print was alleen om de zaak te test
for i in range(1,len(array_grondwaterstand)):
     array_grondwaterstand[i] = gws_op_t(array_bergingscoefficient[0], array_drainweerstand[0], array_grondwaterstand[i-1], array_qbot[0], array_hgem[0], array_neerslagoverschot[i])


#for i in range(1,len(array_grondwaterstand)):
#    array_grondwaterstand[i]=bovenmaaiveld(array_grondwaterstand[i])

#print array_grondwaterstand #print was alleen om de zaak te testen

dates = pd.date_range('19700101', periods=11323)
dfGWS = pd.Series(array_grondwaterstand, index=dates)
#print dfGWS #print was alleen om de zaak te testen

GWSbestand_uit = '/home/john/Documenten/FTM/HyGis/QGIS/GWS_out.csv'
#GWSdates=dfMeteo['Dag'].combineAdd(dfGWS)
dfGWS.to_csv(GWSbestand_uit,  index=True, sep=',', header=None)
pd.Series.plot(dfGWS, kind='line')
ax = pylab.gca()
ax.set_ylabel('$cm-mv$')

pylab.savefig('/home/john/Documenten/FTM/HyGis/QGIS/Grondwaterstanden.png', bbox_inches='tight')
# without the line below, the figure won't show
pylab.show()


