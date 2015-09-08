#module Gt bepalen
#Auteur: John van Dam
#Datum: 8 september 2015

def GT(ghg, glg):
    if (ghg > -25.0) and (glg > -50.0):
        gtnr = '11' 
        gt = 'Ia' 
    elif (ghg < -25.0) and (glg > -50.0):
        gtnr = '12' 
        gt = 'Ib' 
    elif (ghg > -25.0) and ((glg < -50.0) and (glg > -80.0)):
        gtnr = '21' 
        gt = 'AIa' 
    elif ((ghg < -25.0) and (ghg > -40)) and ((glg < -50.0) and (glg > -80.0)):
        gtnr = '22' 
        gt = 'IIb' 
    elif (ghg < -40.0) and ((glg < -50.0) and (glg > -80.0)):
        gtnr = '23' 
        gt = 'IIc' 
    elif (ghg > -25.0) and ((glg < -80.0) and (glg > -120.0)):
        gtnr = '31' 
        gt = 'IIIa' 
    elif ((ghg < -25.0) and (ghg > -40)) and ((glg < -80.0) and (glg > -120.0)):
        gtnr = '32' 
        gt = 'IIIb' 
    elif ((ghg < -40.0) and (ghg > -80.0)) and ((glg < -80.0) and (glg > -120.0)):
        gtnr = '41' 
        gt = 'IVu' 
    elif (ghg < -80.0) and ((glg < -80.0) and (glg > -120.0)):
        gtnr = '42' 
        gt = 'IVc' 
    elif (ghg > -25.0) and (glg < -120.0):
        gtnr = '51' 
        gt = 'Va' 
    elif ((ghg < -25.0) and (ghg > -40.0)) and (glg < -120.0):
        gtnr = '52' 
        gt = 'Vb' 
    elif ((ghg < -40.0) and (ghg > -80.0)) and ((glg < -120.0) and (glg > -180.0)):
        gtnr = '61' 
        gt = 'VIo' 
    elif ((ghg < -40.0) and (ghg > -80.0)) and (glg < -180.0):
        gtnr = '62' 
        gt = 'VId' 
    elif ((ghg < -80.0) and (ghg > -140.0)) and ((glg < -120.0) and (glg > -180.0)):
        gtnr = '71' 
        gt = 'VIIo' 
    elif ((ghg < -80.0) and (ghg > -140.0)) and (glg < -180.0):
        gtnr = '72' 
        gt = 'VIId' 
    elif (ghg < -140.0) and ((glg < -120.0) and (glg > -180.0)):
        gtnr = '81' 
        gt = 'VIIIo' 
    elif (ghg < -140.0) and (glg < -180.0):
        gtnr = '82' 
        gt = 'VIIId'
    return gtnr, gt
