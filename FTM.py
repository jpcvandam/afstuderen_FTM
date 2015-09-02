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



###################################################################
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
    ht = cw(drainageweerstand, qbot, hgem) + delta(bergingscoefficient, drainageweerstand) * (ht_dt - cw(drainageweerstand, qbot, hgem)) + omega(drainageweerstand, bergingscoefficient) * (Pt/100)
    if ht<0:
	ht = ht
	afstroming = 0
    else: 
	ht =0
	afstroming = Pt/100
    return ht, afstroming	
    #return(ht)


def afvoer(grondwaterstand, neerslag): #geeft altijd 0 terug, omdat de gronwaterstand bij het maaiveld automatisch afgekapt wordt, die functie uit de grondwaterstandsdefinitie halen heeft geen zin, omdat dan doorgerekend wordt met een grondwaterstand boven maaiveld en dat klopt ook niet.
    if grondwaterstand>0:
        return (neerslag/10)
    else:
        return 0


###################################################################
#hier begint dan het programma
nummer_meteostation = 286

for i in [nummer_meteostation]:
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
#print array_grondwaterstand #print was alleen om de zaak te test
for i in range(1,len(array_neerslagoverschot)):
    array_grondwaterstand[0,i] = gws_op_t(array_bergingscoefficient[0], array_drainweerstand[0], array_grondwaterstand[0, (i-1)], array_qbot[0], array_hgem[0], array_neerslagoverschot[i])[0]
    array_grondwaterstand[1,i] = gws_op_t(array_bergingscoefficient[0], array_drainweerstand[0], array_grondwaterstand[0, (i-1)], array_qbot[0], array_hgem[0], array_neerslagoverschot[i])[1]


###################################################################

#hieronder wordt het outputbestand met de grondwaterstanden en de oppervlakkige afstroming gemaakt
#print dfNettoNeerslag.ix[0, 'datum']
startdatum = dfNettoNeerslag.ix[0, 'datum']
dates = pd.date_range(startdatum, periods=len(array_neerslagoverschot))
dfGWS = pd.Series(array_grondwaterstand[0], index=dates)
serafstroming = pd.Series(array_grondwaterstand[1], index=dates)
#print serafstroming

#print dfGWS #print was alleen om de zaak te testen

dfGrondwaterstanden = dfGWS.to_frame(name = 'Grondwaterstanden')
#print dfGrondwaterstanden

dfAfstroming = serafstroming.to_frame(name = 'Afstroming')

dfOutput = pd.merge(dfGrondwaterstanden, dfAfstroming,how='inner', on=None, left_on=None, right_on=None, left_index=True, right_index=True)
#print dfOutput

GWSbestand_uit = 'GWS_out_'+str(nummer_meteostation)+'.csv'
dfOutput.to_csv(GWSbestand_uit,  index=True, sep=',')
###################################################################
#berekening van GLG en GHG
#for i in [4, 5, 6, 7, 8, 9]:
#    dfGLG = dfGWS[((dfGWS.index.month == i) & (14 == dfGWS.index.day)  # 
#                    | (dfGWS.index.month == i) & (dfGWS.index.day == 28))]  #
#    print dfGLG.mean()
###################################################################
#GLG uit het dataframe dfGWS halen
dfGLG = dfGWS[((dfGWS.index.month == 4) & (14 == dfGWS.index.day)  # 
                | (dfGWS.index.month == 4) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 5) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 5) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 6) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 6) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 7) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 7) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 8) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 8) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 9) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 9) & (dfGWS.index.day == 28))]  #
#print dfGLG.mean()


grouped_l = dfGLG.groupby(lambda x: x.year)
#for year, group in grouped_l:
#    print year
#    print group
#print grouped_l.nsmallest(3)
extremen_l = grouped_l.nsmallest(3).to_frame(name='extremen_l')
#print extremen_l.mean()


GLG = extremen_l.mean()
array_GLG = np.full((1, len(array_neerslagoverschot)), GLG, order='C') #maak een array met de uiteindelijke GLG om die later te kunnen plotten
dfGLGs = pd.Series(array_GLG[0], index=dates) #array converteren naar pandas dataframe, omdat dat makkelijker plot

GLGbestand_uit = 'GLG_out_'+str(nummer_meteostation)+'.csv'
dfGLG.to_csv(GLGbestand_uit,  index=True, sep=',')
###################################################################
#GLG uit het dataframe dfGWS halen

#for i in [10, 11, 12, 1, 2, 3]:
#    dfGHG = dfGWS[((dfGWS.index.month == i) & (14 == dfGWS.index.day)  # 
#                    | (dfGWS.index.month == i) & (dfGWS.index.day == 28))]  #
#print dfGHG.mean()

dfGHG = dfGWS[((dfGWS.index.month == 10) & (14 == dfGWS.index.day)  # 
                | (dfGWS.index.month == 10) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 11) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 11) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 12) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 12) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 1) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 1) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 2) & (dfGWS.index.day == 28)
                | (dfGWS.index.month == 2) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 3) & (dfGWS.index.day == 14)
                | (dfGWS.index.month == 3) & (dfGWS.index.day == 28))]  #

#print dfGHG.mean()
#waarschijnlijk nu eerst een dataframe maken met pandas, het is anders een array die pandas niet snapt
#GHGS = dfGHG.to_frame(name='Wintermetingen')

###################################################################


#print GHGS.index.freq #doet wel iets, maar niet iets waar ik op zit te wachten


#print GHGS

grouped_h = dfGHG.groupby(lambda x: x.year)
#for year, group in grouped_h:
#    print year
#    print group
#print grouped_h.nlargest(3)
extremen = grouped_h.nlargest(3).to_frame(name='extremen')
#print extremen.mean()

#print GHGS#['2009']#.nlargest(3)
#print GHGS.size
#print GHGS['Wintermetingen'].mean()

###################################################################

GHG = extremen.mean()

array_GHG = np.full((1, len(array_neerslagoverschot)), GHG, order='C') #maak een array met de uiteindelijke GHG om die later te kunnen plotten
dfGHGs = pd.Series(array_GHG[0], index=dates) #array converteren naar pandas dataframe, omdat dat makkelijker plot

GHGbestand_uit = 'GHG_out_'+str(nummer_meteostation)+'.csv'
dfGHGs.to_csv(GHGbestand_uit,  index=True, sep=',')
###################################################################
#een klein beetje statistiek om te testen
#print dfGWS.nsmallest(25)
#print dfGWS.nlargest(25)
#print dfGrondwaterstanden.mean()
###################################################################
#plotje maken van de grondwaterstanden en opslaan
# Create plots with pre-defined labels.
pd.Series.plot(dfGWS, kind='line', label='Grondwaterstand')
pd.Series.plot(dfGHGs, label='GHG')
pd.Series.plot(dfGLGs, label='GLG')

plt.legend(loc='upper center', shadow=True, fontsize='x-large')

#pd.Series.plot(dfGWS.mean(), kind='line')
ax = pylab.gca()
ax.set_ylabel('$cm-mv$')
plt.xlabel('Tijd')
plt.title('Tijdstijghoogtelijn')
pylab.savefig('Grondwaterstanden_'+str(nummer_meteostation)+'.png', bbox_inches='tight')
pylab.close()
