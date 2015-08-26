#Auteur: John van Dam
#Datum: 25 augustus 2015
#dit script splitst de Meteodata van het KNMI op in datafiles die alleen de data van het een station bevatten en geeft ze vervolgens de naam METEO+stationsnummer+.txt

import pandas as pd
import numpy as np
import pylab
import datetime
import matplotlib.dates as mdates
import datetime as dt
#from numpy.numarray.functions import value

#bestandspad = '/home/john/data/'
for i in [215, 225, 235, 240, 242, 249, 251, 257, 260, 380 ]:
    meteobestand_in = 'METEO'+str(i)+'.TXT'
    dfMeteo=pd.read_csv(meteobestand_in, header=True, skiprows=17, skipinitialspace=True, index_col=1, delimiter =',', names = ['STN','YYYYMMDD', 'DR', 'RH', 'RHX', 'RHXH', 'EV24 = DR', 'RH', 'EV24'], parse_dates=[1])
    #print dfMeteo

    dfmeteo_out=dfMeteo.RH.sub(dfMeteo.EV24, axis=0)
    #print dfmeteo_out

    meteobestand_uit = 'Waterbalans_METEO'+str(i)+'.csv'
    dfmeteo_out.to_csv(meteobestand_uit,  index=True, sep=',', header=True)
