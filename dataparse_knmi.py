#Auteur: John van Dam
#Datum: 26 augustus 2015
#dit script berekend de waterbalans (neerslag - potentiele Makkink verdamping) aan de hand van de Meteodata van het KNMI en geeft ze vervolgens de naam Waterbalans_METEO+stationsnummer+.txt

import pandas as pd
import numpy as np
import pylab
import datetime
import matplotlib.dates as mdates
import datetime as dt


#bestandspad = '/home/john/data/'
#In deze loop zijn alleen de weerstations opgenomen waarvan daadwerkelijk data opgehaald is, het script 'datagrab_knmi.py' haalt voor alle bekende stations data op, maar het merendeel blijkt alleen een header te bevatten met coordinaten en een legenda. Vervolgens zijn er echter niet altijd metingen voor neerslag en verdamping, of er wel andere gegevens op die stations zijn weet ik niet; heb ik niet gebrobeerd, omdat die voor dit project toch nutteloos zijn.
for i in [215, 225, 235, 240, 242, 249, 251, 257, 260, 265, 267, 269, 270, 273, 275, 277, 278, 279, 280, 283, 286, 290, 310, 323,  319, 330, 340, 344, 348, 350, 356, 370, 375, 377, 380, 391,  ]:
    meteobestand_in = 'METEO'+str(i)+'.TXT'
    dfMeteo=pd.read_csv(meteobestand_in, header=True, skiprows=17, skipinitialspace=True, index_col=1, delimiter =',', names = ['STN','YYYYMMDD', 'DR', 'RH', 'RHX', 'RHXH', 'EV24 = DR', 'RH', 'EV24'], parse_dates=[1])

    dfmeteo_out=dfMeteo.RH.sub(dfMeteo.EV24, axis=0)

    meteobestand_uit = 'Waterbalans_METEO'+str(i)+'.csv'
    dfmeteo_out.to_csv(meteobestand_uit,  index=True, sep=',', header=True)
