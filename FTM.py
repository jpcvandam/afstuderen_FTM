#dit script is de Python variant van het FTM door Jaco van der Gaast in Pascal
#Auteur: John van Dam
#Datum: 17 augustus 2015

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
import datetime
import matplotlib.dates as mdates
import datetime as dt




#functiedefinities rekenen

#haal eerst de coordinaten op van de locatie waar de grondwaterstand berekend moet worden, hierbij gelijk de b1 en b2 waarden uit de Staringreeks, tevens c, dt [kan misschien door gebruiker ingesteld worden, anders default 1], ht_dt [moet dus de dag ervoor berekend worden], Pt uit de waterbalans database

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
    ht = cw(drainageweerstand, qbot, hgem) + delta(bergingscoefficient, drainageweerstand) * (ht_dt - cw(drainageweerstand, qbot, hgem)) + omega(drainageweerstand, bergingscoefficient) * (Pt/10)
    if ht<0:
	ht = ht
	Pt = Pt
    else: 
	ht =0
	Pt = Pt/10
    return ht, Pt	
    #return(ht)


def afvoer(grondwaterstand, neerslag): #geeft altijd 0 terug, omdat de gronwaterstand bij het maaiveld automatisch afgekapt wordt, die functie uit de grondwaterstandsdefinitie halen heeft geen zin, omdat dan doorgerekend wordt met een grondwaterstand boven maaiveld en dat klopt ook niet.
    if grondwaterstand>0:
        return (neerslag/10)
    else:
        return 0



#hier begint dan het programma

for i in [215]:
    meteobestand_in = 'Waterbalans_METEO'+str(i)+'.csv'
    dfNettoNeerslag = pd.read_csv(meteobestand_in, header=False, skiprows=1, names = ['datum', 'NN1', 'NN2' ], delimiter =',', parse_dates=[0])


#print dfNettoNeerslag #print was alleen om de zaak te testen

array_neerslagoverschot = dfNettoNeerslag['NN1'].values
#print array_neerslagoverschot #print was alleen om de zaak te testen
#print dfMeteo.neerslagoverschot

bodembestand = 'Bodemdata.txt'
dfBodem=pd.read_csv(bodembestand, header=None, delimiter =',', names = ['#runn', 'al', 'hgem', 'drainw', 'berg', 'qbot' ]) #names = ['#runn', 'al', 'hgem', 'drainw', 'berg', 'qbot' ]
#print dfBodem #print was alleen om de zaak te testen

array_drainweerstand = dfBodem['drainw'].values
array_hgem = dfBodem['hgem'].values
array_bergingscoefficient = dfBodem['berg'].values
array_qbot = dfBodem['qbot'].values
#hgem', 'drainw', 'berg', 'qbot


array_grondwaterstand = np.zeros(shape = (2, len(array_neerslagoverschot)), order='C')
#array_afvoer = np.zeros(shape = (len(array_neerslagoverschot)), order='C')
print array_grondwaterstand #print was alleen om de zaak te test
for i in range(1,len(array_neerslagoverschot)):
    array_grondwaterstand[0,i] = gws_op_t(array_bergingscoefficient[0], array_drainweerstand[0], array_grondwaterstand[0, (i-1)], array_qbot[0], array_hgem[0], array_neerslagoverschot[i])[0]
    array_grondwaterstand[1,i] = gws_op_t(array_bergingscoefficient[0], array_drainweerstand[0], array_grondwaterstand[0, (i-1)], array_qbot[0], array_hgem[0], array_neerslagoverschot[i])[1]

print array_grondwaterstand
#for i in range(1,len(array_grondwaterstand)):
   #array_afvoer[i]=afvoer(array_grondwaterstand[i], array_neerslagoverschot[i])
#array_afvoer=afvoer(array_grondwaterstand, array_neerslagoverschot)
#print array_afvoer #print was alleen om de zaak te testen

#print dfNettoNeerslag.ix[0, 'datum']
startdatum = dfNettoNeerslag.ix[0, 'datum']
dates = pd.date_range(startdatum, periods=len(array_neerslagoverschot))
dfGWS = pd.Series(array_grondwaterstand[0], index=dates)
#dfafstroming = pd.Series(array_grondwaterstand[1], index=dates)
#dfOutput = pd.concat([dfGWS, dfafstroming])
#print dfGWS #print was alleen om de zaak te testen

GWSbestand_uit = 'GWS_out.csv'
#GWSdates=dfMeteo['Dag'].combineAdd(dfGWS)
dfGWS.to_csv(GWSbestand_uit,  index=True, sep=',', header=None)
pd.Series.plot(dfGWS, kind='line')
ax = pylab.gca()
ax.set_ylabel('$cm-mv$')

pylab.savefig('Grondwaterstanden.png', bbox_inches='tight')
# without the line below, the figure won't show
pylab.close()
