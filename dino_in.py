#grondwaterstanden dino inlezen
#auteur: John van Dam
#datum: 2 september 2015

import pandas as pd
import matplotlib.pyplot as plt
import pylab
import numpy as np

dino_naam = 'B07A0981001_0.csv'
dfGWSdino = pd.read_csv(dino_naam, header=True, skiprows=10, delimiter =',', parse_dates=[2], index_col=[2], names=['filternummer','locatie', 'datum', 'peil', 'bijzonderheid'])
#, names = ['LOCATIE','FILTERNUMMER','PEIL', 'DATUM', 'TIJD', 'STAND (MV)','BIJZONDERHEID']
#print dfGWSdino
dfGWSm = dfGWSdino['peil']*-1
#print dfGWSm.index
filternummer = dfGWSdino.ix[0, 'filternummer']

#print dfGWSdino.ix[0, 'peil']


tijdsspanne = dfGWSdino['peil'].size
#print tijdsspanne
#print dfGWSdino['peil'].size
datesm = dfGWSm.index#dfGWSdino['peil'].size)
#print datesm

###################################################################
#GLG uit het dataframe dfGWS halen
dfGLGm = dfGWSm[((dfGWSm.index.month == 4)
                | (dfGWSm.index.month == 5)
                | (dfGWSm.index.month == 6)
                | (dfGWSm.index.month == 7)
                | (dfGWSm.index.month == 8)
                | (dfGWSm.index.month == 9))]  #
#print dfGLG


grouped_lm = dfGLGm.groupby(lambda x: x.year)

#print grouped_l.nsmallest(3)
extremen_lm = grouped_lm.nsmallest(3).to_frame(name='extremen_lm')
#print extremen_lm.mean()


GLGm = extremen_lm.mean()
array_GLGm = np.full((1, tijdsspanne), GLGm, order='C') #maak een array met de uiteindelijke GLG om die later te kunnen plotten
dfGLGsm = pd.Series(array_GLGm[0], index=datesm) #array converteren naar pandas dataframe, omdat dat makkelijker plot


###################################################################
#GLG uit het dataframe dfGWS halen


dfGHGm = dfGWSm[((dfGWSm.index.month == 10)  #
                | (dfGWSm.index.month == 11)
                | (dfGWSm.index.month == 12)
                | (dfGWSm.index.month == 1) 
                | (dfGWSm.index.month == 2) 
                | (dfGWSm.index.month == 3))]  #
#print dfGHGm



###################################################################



grouped_hm = dfGHGm.groupby(lambda x: x.year)

extremen_hm = grouped_hm.nlargest(3).to_frame(name='extremen_hm')
#print extremen_hm
#print extremen_hm.mean()



###################################################################

GHGm = extremen_hm.mean()

array_GHGm = np.full((1, tijdsspanne), GHGm, order='C') #maak een array met de uiteindelijke GHG om die later te kunnen plotten
dfGHGsm = pd.Series(array_GHGm[0], index=datesm) #array converteren naar pandas dataframe, omdat dat makkelijker plot

#print dfGHGsm

###################################################################
#plotje maken van de grondwaterstanden en opslaan
# Create plots with pre-defined labels.
pd.Series.plot(dfGWSm, kind='line', label='Grondwaterstand')
pd.Series.plot(dfGHGsm, label='GHG')
pd.Series.plot(dfGLGsm, label='GLG')

plt.legend(loc='upper center', shadow=True, fontsize='x-large')


ax = pylab.gca()
ax.set_ylabel('$cm-mv$')
plt.xlabel('Tijd')
plt.title('Tijdstijghoogtelijn')
pylab.savefig('Grondwaterstanden_'+str(filternummer)+'.png', bbox_inches='tight')
pylab.close()
