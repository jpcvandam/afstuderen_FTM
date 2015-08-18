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

#functiedefinitie meteogegevens inladen
def leesmeteo(meteobestand):
    dfMeteo=pd.read_fwf(meteobestand, widths=[14,14,14,14,14], header = None, names = ['dag', 'maand' , 'jaar' ,'neerslag' , 'verdamping'], parse_dates={"Datetime" : [0,1,2]})
    dfMeteo = dfMeteo.set_index('Datetime')
    return dfMeteo


#functiedefinitie rekenen
#def waterbalans(dfMeteo.neerslag, dfMeteo.verdamping):
#    dfMeteo.neerslagoverschot=dfMeteo.neerslag-dfMeteo.verdamping
#    return dfMeteo.neerslagoverschot




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
    ht = cw(drainageweerstand, qbot, hgem) + delta(bergingscoefficient, drainageweerstand) * (ht_dt - cw(drainageweerstand, qbot, hgem)) + omega(drainageweerstand, bergingscoefficient) * Pt
    return(ht)

#print omega(1.0, 0.1, 0.2)
#print delta(1.0, 0.2)
#print gws_op_t(delta(1.0, 0.2), 125.0, 130.0, omega(1.0, 0.1, 0.2), 2.0)

#functiedefinitie gegevens wegschrijven
#het moet de oorspronkelijke datumlijst + het verschil tussen de kolommen 'neerslag' en 'verdamping' wegschrijven onder de naam neerslagoverschot
#def schrijfmeteo(meteobestand_uit):
#    dfMeteo.to_csv(meteobestand_uit, names=['datum', 'neerslag', 'verdamping'])
    #return dfMeteo_uit

#hier begint dan het programma

meteobestand='METEO669.TXT'

dfMeteo=pd.read_fwf(meteobestand, widths=[14,14,14,14,14], header = None, names = ['dag', 'maand' , 'jaar' ,'neerslag' , 'verdamping'], parse_dates={"Datetime" : [0,1,2]})
dfMeteo = dfMeteo.set_index('Datetime')
#dfMeteo['dt'] = pd.to_datetime(dfMeteo.jaar+dfMeteo.maand+dfMeteo.dag,format='%Y%m%d')
#dfMeteo['dt3'] = dfMeteo.dt + dfMeteo.dt2

#format = "%d%m%Y"
#times = pd.to_datetime(dfMeteo['dag'] + dfMeteo['maand'] + dfMeteo['jaar'], format=format)
#print times #print was alleen om de zaak te testen

#dfMeteo['date'] = dt.datetime(dfMeteo['jaar'],dfMeteo['maand'],dfMeteo['dag'])
#print leesmeteo('METEO669.TXT') #bestandsextensies zijn case-senSiTive
#print dfMeteo #print was alleen om de zaak te testen
print dfMeteo.info() #print is alleen om de zaak te testen

#demonstratie hoe je een array maakt
#arraypiet = dfMeteo['neerslag'].values
#print arraypiet

pd.DataFrame.plot(dfMeteo, kind='line')
ax = pylab.gca()
ax.set_ylabel('$mm/dag$')

pylab.savefig('Neerslag+verdamping.png', bbox_inches='tight')
# without the line below, the figure won't show
pylab.show()


dfMeteo_out = pd.Series(dfMeteo.neerslag-dfMeteo.verdamping)
#dfMeteo_out['neerslagoverschot']=dfMeteo.neerslag-dfMeteo.verdamping
#print dfMeteo_out #print was alleen om de zaak te testen
meteobestand_uit = 'Meteo_out.csv'
dfMeteo_out.to_csv(meteobestand_uit,  index=True, sep=',', header=True)

array_neerslagoverschot = dfMeteo_out.values
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

#b = np.ndenumerate(array_grondwaterstand)
#for position,value in b: print position-1,value # position is the N-dimensional index
ht=0

array_grondwaterstand = gws_op_t(array_bergingscoefficient, array_drainweerstand, ht, array_qbot, array_hgem, array_neerslagoverschot)



#print array_grondwaterstand #print was alleen om de zaak te testen

dates = pd.date_range('19700101', periods=11323)


dfGWS = pd.Series(array_grondwaterstand, index=dates)
#print dfGWS #print was alleen om de zaak te testen
GWSbestand_uit = 'GWS_out.csv'
#GWSdates=dfMeteo['Dag'].combineAdd(dfGWS)
dfGWS.to_csv(GWSbestand_uit,  index=True, sep=',', header=None)
pd.Series.plot(dfGWS, kind='line')
ax = pylab.gca()
ax.set_ylabel('$cm-mv$')

pylab.savefig('Grondwaterstanden.png', bbox_inches='tight')
# without the line below, the figure won't show
pylab.show()
