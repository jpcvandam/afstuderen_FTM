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
    dfMeteo=pd.read_csv(meteobestand, names=['datum', 'neerslag', 'verdamping'], skipinitialspace=True, delim_whitespace=True, parse_dates=True, index_col=[0,1,2])
    return dfMeteo


#functiedefinitie rekenen
#def waterbalans(dfMeteo.neerslag, dfMeteo.verdamping):
#    dfMeteo.neerslagoverschot=dfMeteo.neerslag-dfMeteo.verdamping
#    return dfMeteo.neerslagoverschot

def gws_op_t(delta0, ht_dt, c, omega0, Pt) :
    ht = c + delta0 * (ht_dt - c) + omega0 * Pt
    return ht


#haal eerst de coordinaten op van de locatie waar de grondwaterstand berekend moet worden, hierbij gelijk de b1 en b2 waarden uit de Staringreeks, tevens c, dt [kan misschien door gebruiker ingesteld worden, anders default 1], ht_dt [moet dus de dag ervoor berekend worden], Pt uit de waterbalans database

def delta(dt, b2) :
    delta1 = np.exp(-3.0 * dt/b2)
    return(delta1)


def omega(dt, b1, b2) :
    omega1 = b1 * (1.0 - np.exp(-3.0 * dt/b2))
    return(omega1)


print omega(1.0, 0.1, 0.2)
print delta(1.0, 0.2)
print gws_op_t(delta(1.0, 0.2), 125.0, 130.0, omega(1.0, 0.1, 0.2), 2.0)

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
#print times

#dfMeteo['date'] = dt.datetime(dfMeteo['jaar'],dfMeteo['maand'],dfMeteo['dag'])
#print leesmeteo('METEO669.TXT') #bestandsextensies zijn case-senSiTive
print dfMeteo
print dfMeteo.info()

pd.DataFrame.plot(dfMeteo, kind='line')
# without the line below, the figure won't show
pylab.show()

#dfMeteo.neerslagoverschot=dfMeteo.neerslag-dfMeteo.verdamping
#print dfMeteo.neerslagoverschot

#schrijfmeteo('meteobestand_uit.txt')
