#Dit script haalt data van alle KNMI stations op en schrijft ze weg onder de naam: METEO+stationsnummer+TXT
#Auteur: John van Dam
#Datum: 26 augustus 2015
#informatie te vinden op http://www.knmi.nl/klimatologie/daggegevens/scriptxs-nl.html

import urllib
import urllib2
import csv
import pandas as pd

#variabelen
bjaar='2015'
bmaand='08'
bdag=11
ejaar='2015'
emaand='08'
edag=bdag+10
#station = '277'

for i in ['277', '235', '280', '260']:
    url = 'http://www.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi'
    values = {'stns' : 'i',
              'byear' : 'bjaar',
              'bmonth' : 'bmaand',
              'bday' : 'bdag',
              'eyear' : 'ejaar',
              'emonth': 'emaand',
              'eday' : 'edag',
              'vars' : 'PRCP = DR:RH:EV24' }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    #print the_page
    meteobestandsnaam = 'METEO'+i+'.TXT'
    meteobestand = open(meteobestandsnaam, 'w')
    meteobestand.write(the_page)
    meteobestand.close()
