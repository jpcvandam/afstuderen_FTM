#Dit script haalt data van alle KNMI stations op en schrijft ze weg onder de naam: METEO+stationsnummer+TXT
#Auteur: John van Dam
#Datum: 26 augustus 2015
#informatie te vinden op http://www.knmi.nl/klimatologie/daggegevens/scriptxs-nl.html

import urllib
import urllib2
import csv
import pandas as pd

for i in [127 ,  32 ,  206 ,  331 ,  200 ,  18 ,  125 ,  16 ,  609 ,  272 ,  161 ,  998 ,  316 ,  313 ,  20 ,  163 ,  551 ,  148 ,  343 ,  35 ,  208 ,  275 ,  325 ,  29 ,  350 ,  203 ,  138 ,  211 ,  153 ,  321 ,  340 ,  311 ,  247 ,  204 ,  165 ,  139 ,  129 ,  17 ,  320 ,  147 ,  280 ,  273 ,  323 ,  268 ,  249 ,  168 ,  202 ,  135 ,  348 ,  319 ,  285 ,  385 ,  617 ,  212 ,  344 ,  126 ,  553 ,  159 ,  251 ,  253 ,  279 ,  8 ,  209 ,  37 ,  270 ,  391 ,  170 ,  33 ,  554 ,  552 ,  227 ,  324 ,  244 ,  162 ,  255 ,  240 ,  999 ,  108 ,  230 ,  604 ,  277 ,  377 ,  201 ,  379 ,  550 ,  152 ,  225 ,  142 ,  207 ,  330 ,  263 ,  266 ,  167 ,  995 ,  133 ,  290 ,  615 ,  39 ,  210 ,  41 ,  258 ,  312 ,  229 ,  19 ,  260 ,  370 ,  315 ,  166 ,  375 ,  380 ,  616 ,  300 ,  128 ,  252 ,  28 ,  286 ,  40 ,  283 ,  310 ,  250 ,  614 ,  308 ,  215 ,  254 ,  278 ,  271 ,  605 ,  130 ,  328 ,  239 ,  122 ,  267 ,  143 ,  205 ,  158 ,  269 ,  13 ,  235 ,  257 ,  36 ,  248 ,  38 ,  356 ,  34 ,  265 ,  169 ,  164 ,  603 ,  242  ]:
    url = 'http://www.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi'
    values = {'stns' : i,
              'byear' : 1970,
              'bmonth' : 1,
              'bday' : 1,
              'eyear' : 2015,
              'emonth': 8,
              'eday' : 25,
              'vars' : 'PRCP = DR:RH:EV24' }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    #print the_page
    meteobestandsnaam = 'METEO'+str(i)+'.TXT'
    meteobestand = open(meteobestandsnaam, 'w')
    meteobestand.write(the_page)
    meteobestand.close()
