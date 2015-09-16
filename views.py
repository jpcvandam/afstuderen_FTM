from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render_to_response#, 
from django.template.loader import render_to_string 
import simplejson
from ftm.models import Waypoint
##imports om te rekenen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
from datetime import datetime
import subprocess
from FTM_rekenhart import *
from GxG import *
from GT import GT
from plot_GWS import *
from raster import raster_q

def index(request):
    'Display map'
    waypoints = Waypoint.objects.order_by('name')
    return render_to_response('ftm/index.html', {
        'waypoints': waypoints,
        'content': render_to_string('ftm/waypoints.html', {'waypoints': waypoints}),
    })


def save(request):
    'Save waypoints'
    for waypointString in request.GET.get('waypointsPayload', '').splitlines():
        waypointID, waypointX, waypointY = waypointString.split()
        waypoint = Waypoint.objects.get(id=int(waypointID))
        waypoint.geometry.set_x(float(waypointX))
        waypoint.geometry.set_y(float(waypointY))
        waypoint.save()
    return HttpResponse(simplejson.dumps(dict(isOk=1)), mimetype='application/json')





###################################################################
#hier komt dan het ftm
def ftm(request):
    'Grondwaterstand'
    x = request.GET.get('x')
    y = request.GET.get('y')
    plotje = maak_plotje(x, y)
    return render_to_response("ftm/grafiek.html", { 'x':x, 'y':y, 'plotje': plotje})
    #return render_to_response('ftm/index.html', {
     #   'waypoints': waypoints,
      #  'content': render_to_response('ftm/grafiek.html', {plotje=plotje, x=x, y=y}),
    #})
    

#dit script is de Python variant van het FTM door Jaco van der Gaast in Pascal
#Auteur: John van Dam
#Datum: 17 augustus 2015
#voor het laatst bijgewerkt op 8 september 2015





###################################################################
#variabelen
def maak_plotje(x2, y2):
    nummer_meteostation = 310
    bestandspad='/home/john/ftm/ftm/ftm/data/'
    bestandspad_plot='/home/john/ftm/ftm/ftm/static/'
    bodembestand = bestandspad + 'Bodemdata.txt'

    x= str(x2)#"6.5108"
    y= str(y2)#"53.3847"

###################################################################
#hier begint dan het programma

#voorbewerkte meteo inlezen in een pandas dataframe en dan wegschrijven naar een numpy array
    for i in [nummer_meteostation]:
        meteobestand_in = bestandspad + 'Waterbalans_METEO'+str(i)+'.csv'
        dfNettoNeerslag = pd.read_csv(meteobestand_in, header=False, skiprows=1, names = ['datum', 'NN1', 'NN2' ], delimiter =',', parse_dates=[0])
    array_neerslagoverschot = dfNettoNeerslag['NN1'].values
    lengte = len(array_neerslagoverschot) #arrays die je samen wilt gebruiken in een tijdserie moeten even lang zijn, anders gaat er van alles mis


#bodemdata afkomstig uit de QGIS puntenwolk inlezen in een pandas dataframe en dan wegschrijven naar een numpy arrays
    dfBodem=pd.read_csv(bodembestand, header=None, delimiter =',', names = ['#runn', 'al', 'hgem', 'drainw', 'berg', 'qbot' ])
    #array_bergingscoefficient = np.array([float(raster_q("/home/john/ftm/ftm/ftm/data/Bergingscoefficient1.tif", x, y))])
    #array_drainweerstand = np.array([float(raster_q("/home/john/ftm/ftm/ftm/data/Drainageweerstand1.tif", x, y))])
    #array_qbot = np.array([float(raster_q("/home/john/ftm/ftm/ftm/data/Kwel-kk-nz1.tif", x, y))])
    #array_hgem = np.array([float(raster_q("/home/john/ftm/ftm/ftm/data/Ontwateringsbasis1.tif", x, y))])

    array_drainweerstand = dfBodem['drainw'].values
    array_hgem = dfBodem['hgem'].values
    array_bergingscoefficient = dfBodem['berg'].values
    array_qbot = dfBodem['qbot'].values
#print str(datetime.now()) + 'array vullen met nullen'
#array grondwaterstand voorbereiden en vullen met nullen, zodoende begint de berekening altijd op 0 cm-mv en gaat python niet klagen over de positieaanduiding in een nog niet bestaande array
    array_grondwaterstand = np.zeros(shape = (2, lengte), order='C')
#print str(datetime.now()) + 'beginnen met rekenen'
#door de functie gws_op_t uit het rekenhart aan te roepen en met behulp van een for loop uit te voeren wordt voor iedere dag de grondwaterstand berekend met de netto neerslag en de bodemdata, tegelijk wordt de oppervlakkige afstroming berekend, maar dit laatste is nog in ontwikkeling
    for i in range(1,lengte):
        array_grondwaterstand[0,i] = gws_op_t(array_bergingscoefficient[0], array_drainweerstand[0], array_grondwaterstand[0, (i-1)], array_qbot[0], array_hgem[0], array_neerslagoverschot[i])[0]
        array_grondwaterstand[1,i] = gws_op_t(array_bergingscoefficient[0], array_drainweerstand[0], array_grondwaterstand[0, (i-1)], array_qbot[0], array_hgem[0], array_neerslagoverschot[i])[1]

#print str(datetime.now()) + 'data aanmaken voor series'
###################################################################
#hieronder wordt het outputbestand met de grondwaterstanden en de oppervlakkige afstroming gemaakt

#startdatum en dates zijn variabelen die in het verloop van het programma gebruikt worden om een array of serie om te kunnen zetten naar een dataframe met datums
    startdatum = dfNettoNeerslag.ix[0, 'datum']
    dates = pd.date_range(startdatum, periods=lengte)
    #print str(datetime.now()) + 'array naar series'
#dfGWS en serafstroming worden met behulp van pd.Series omgezet in een tijdserie waarbij de grondwaterstanden en afstroming een datum hebben
    dfGWS = pd.Series(array_grondwaterstand[0], index=dates)
    serafstroming = pd.Series(array_grondwaterstand[1], index=dates)
    #print str(datetime.now()) + 'frames maken van grondwaterstanden en afstroming'
#de net gemaakte tijdseries worden omgezet in een dataframe, dat is gemakkelijker met pandas te hanteren voor wegschrijven naar csv en plotten
    dfGrondwaterstanden = dfGWS.to_frame(name = 'Grondwaterstanden')
    dfAfstroming = serafstroming.to_frame(name = 'Afstroming')
#het grondwaterframe en het afstromingsframe worden samengevoegd tot een dataframe, waardoor beide series in een csv-bestand weggezet kunnen worden
#print str(datetime.now()) + 'dataframes samenvoegen en wegschrijven naar een csv'
    dfOutput = pd.merge(dfGrondwaterstanden, dfAfstroming,how='inner', on=None, left_on=None, right_on=None, left_index=True, right_index=True)
#variabele bestandsnaam voor het grondwaterstandenbestand, deze is afhankelijk van het meteostationsnummer om bij verschillende tijdseries niet over de vorige heen te schrijven
    #GWSbestand_uit = 'GWS_out_'+str(nummer_meteostation)+'.csv'
    #dfOutput.to_csv(GWSbestand_uit,  index=True, sep=',')
#print str(datetime.now()) + 'GxG berekenen'
#met behulp van de module GxG.py worden de GHG en GLG berekend en voor het plotten in een dataframe met datums gestopt, anders kan er geen horizontale lijn voor een getal geplot worden
    GHG = GHG_berekening(dfGWS, dates, array_neerslagoverschot, nummer_meteostation)[0]
    GLG = GLG_berekening(dfGWS, dates, array_neerslagoverschot, nummer_meteostation)[0]
    dfGHGs = GHG_berekening(dfGWS, dates, array_neerslagoverschot, nummer_meteostation)[1]
    dfGLGs = GLG_berekening(dfGWS, dates, array_neerslagoverschot, nummer_meteostation)[1]

#print str(datetime.now()) + 'plotten'
###################################################################
#plotje maken van de grondwaterstanden en opslaan
    return plot(dfGWS, dfGHGs, dfGLGs, nummer_meteostation, bestandspad_plot, x2, y2)

#print str(datetime.now()) + 'print de gt'
#via de terminal de grondwatertrap en het nummer van die grondwatertrap printen
    #print GT(GHG[0],GLG[0])
    #print str(datetime.now()) + 'einde'
