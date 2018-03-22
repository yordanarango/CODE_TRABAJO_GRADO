# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 04:54:14 2016

@author: yordan
"""

import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

#==============================================================================
'''SELECCIÓN DE SERIES RESOLUCIÓN HORARIA'''
#==============================================================================

ArchivoU = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/ZONAL-REPROYECCION/1979alt.nc')
ArchivoV = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/MERIDIONAL-REPROYECCION/1979alt.nc')

Variables = [v for v in ArchivoU.variables]
print Variables

LON = ArchivoV.variables['LON'][:]-360
LAT = ArchivoV.variables['LAT'][:]

posiciones = ['TT','PP','PN']
longitudes = [-95.0, -87.5, -79.75]
latitudes = [14.5, 10.25, 7.5]

datep = pd.date_range('1979-01-01 00:00:00', '2015-12-31 23:00:00', freq='3H')
date = pd.DatetimeIndex(datep)
Serie = pd.DataFrame(index=date, columns=['TT','PP', 'PN']) 

for i, j, k in zip(longitudes,latitudes, posiciones):
    for l in range(1979, 2016): # De 0 a 37, porque sólo se va a hacer hasta el 2015
        U = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/ZONAL-REPROYECCION/'+str(l)+'alt.nc')
        V = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/MERIDIONAL-REPROYECCION/'+str(l)+'alt.nc')
        lOn = np.where(LON == i)[0][0]
        lAt = np.where(LAT == j)[0][0]
        v = V.variables['V'][:, lAt, lOn]
        u = U.variables['U'][:, lAt, lOn]
        spd = np.sqrt(u*u+v*v)
        Serie[k][str(l)+'-01-01 00:00:00':str(l)+'-12-31 23:00:00'] = spd
        
MA = Serie.as_matrix(columns=None)
spd_TT = MA[:,0]
spd_PP = MA[:,1]
spd_PN = MA[:,2]

##############
"CICLO DIURNO"
##############

serie_TT = spd_TT 
media_TT = np.zeros((12,8)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
fechas = pd.date_range('1979-01-01 00:00:00','2015-12-31 22:00:00', freq='3H') # serie con fechas cada 6 horas, desde 1979/01/01 hasta 2015/12/31

for i in range(1,13): # Se recorre cada mes
    for j in range(0, 22, 3): # Se recorre cada horario
        selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
        for k in range(len(serie_TT)): # Se recorre toda la serie
            if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                    selec.append(serie_TT[k]) # Si cumple, se adiciona a la lista
        media_TT[i-1, j/3] = np.mean(selec) # Se guarda wl valor de la media




serie_PP = spd_PP 
media_PP = np.zeros((12,8)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
fechas = pd.date_range('1979-01-01 00:00:00','2015-12-31 22:00:00', freq='3H')# serie con fechas cada 6 horas, desde 1979/01/01 hasta 2015/12/31

for i in range(1,13): # Se recorre cada mes
    for j in range(0, 22, 3): # Se recorre cada horario
        selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
        for k in range(len(serie_PP)): # Se recorre toda la serie
            if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                    selec.append(serie_PP[k]) # Si cumple, se adiciona a la lista
        media_PP[i-1, j/3] = np.mean(selec) # Se guarda wl valor de la media




serie_PN = spd_PN 
media_PN = np.zeros((12,8)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
fechas = pd.date_range('1979-01-01 00:00:00','2015-12-31 22:00:00', freq='3H') # serie con fechas cada 6 horas, desde 1979/01/01 hasta 2015/12/31

for i in range(1,13): # Se recorre cada mes
    for j in range(0, 22, 3): # Se recorre cada horario
        selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
        for k in range(len(serie_PN)): # Se recorre toda la serie
            if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                    selec.append(serie_PN[k]) # Si cumple, se adiciona a la lista
        media_PN[i-1, j/3] = np.mean(selec) # Se guarda wl valor de la media

####################
"ANOMALÍAS HORARIAS"
####################        
ano_TT = np.zeros(len(serie_TT))
for i in range(len(serie_TT)):
    ano_TT[i] = serie_TT[i]-media_TT[fechas[i].month-1, fechas[i].hour/3]


ano_PP = np.zeros(len(serie_PP))
for i in range(len(serie_PP)):
    ano_PP[i] = serie_PP[i]-media_PP[fechas[i].month-1, fechas[i].hour/3]


ano_PN = np.zeros(len(serie_PN))
for i in range(len(serie_PN)):
    ano_PN[i] = serie_PN[i]-media_PN[fechas[i].month-1, fechas[i].hour/3]
    
##################################################################
"IDENTIFICACIÓN DE FECHAS QUE SUPERAN UMBRAL TT-7, PP-6.5, PN-6.5"
##################################################################

Ser_TT = np.zeros(len(spd_TT))
Ser_PP = np.zeros(len(spd_PP))
Ser_PN = np.zeros(len(spd_PN))

###### TT ######
for i in range(len(Ser_TT)):
    if spd_TT[i] > 7:
        Ser_TT[i] = spd_TT[i]

##### PP ######
for i in range(len(Ser_PP)):
    if spd_PP[i] > 6.5:
        Ser_PP[i] = spd_PP[i]

#### PN ######
for i in range(len(Ser_PN)):
    if spd_PN[i] > 6.5:
        Ser_PN[i] = spd_PN[i]

###################################
"ÍNDICES EN LOS QUE HAY EVENTOS TT"
###################################
def indices_eventos(Ser_TT):

    i = 0
    evn_TT = []
    
    while i<(len(Ser_TT)-1):    
        if Ser_TT[i] != 0: # Primero se verifica que la posición i tenga un valor
            j = i
            l = 3 # Esto es para poder entrar al while
            while l <= 4:        
                if j < (len(Ser_TT)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector ser, la siguiente línea arrojará un error
                    while Ser_TT[j+1] !=0: # Se hace éste while para saber hasta qué posición llega el evento 
                        j = j+1
                        if j == (len(Ser_TT)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de ser, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                            break
    
                    if j < (len(Ser_TT)-9): # Esta línea es debida a la siguiente, para que no se genere un error
                        if np.any(Ser_TT[j+1:j+9] != np.zeros(8)) == True: # Se debe revisar que las siguientes 8 posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+9): # para hallar en qué posición de las 8 que se juzgan se encuentra la posición con valor distinto de cero 
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while no se vuelva a repetir
                        else:
                            l = 5 # Para que el while no se vuelva a repetir
    
                    elif j < (len(Ser_TT)-8): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-9
                        if np.any(Ser_TT[j+1:j+8] != np.zeros(7)) == True:
                            for k in range(j+1, j+8):
                                if Ser_TT[k] != 0:
                                    l = 2 
                                    j = k
                                    break
                                else:
                                    l = 5 
                        else:
                            l = 5
                    
                    elif j < (len(Ser_TT)-7): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-8
                        if np.any(Ser_TT[j+1:j+7] != np.zeros(6)) == True: 
                            for k in range(j+1, j+7): 
                                if Ser_TT[k] != 0:
                                    l = 2 
                                    j = k
                                    break
                                else:
                                    l = 5 
                        else:
                            l = 5                
                    
                    elif j < (len(Ser_TT)-6): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-7
                        if np.any(Ser_TT[j+1:j+6] != np.zeros(5)) == True: 
                            for k in range(j+1, j+6):  
                                if Ser_TT[k] != 0:
                                    l = 2 
                                    j = k
                                    break
                                else:
                                    l = 5 
                        else:
                            l = 5                
                    
                    elif j < (len(Ser_TT)-5): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-6
                        if np.any(Ser_TT[j+1:j+5] != np.zeros(4)) == True: 
                            for k in range(j+1, j+5):
                                if Ser_TT[k] != 0:
                                    l = 2 
                                    j = k
                                    break
                                else:
                                    l = 5 
                        else:
                            l = 5 
                    
                    elif j < (len(Ser_TT)-4): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-5
                        if np.any(Ser_TT[j+1:j+4] != np.zeros(3)) == True:
                            for k in range(j+1, j+4):
                                if Ser_TT[k] != 0:
                                    l = 2
                                    j = k
                                    break
                                else:
                                    l = 5
                        else:
                            l = 5                        
                    
                    elif j < (len(Ser_TT)-3): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-4
                        if np.any(Ser_TT[j+1:j+3] != np.zeros(2)) == True:
                            for k in range(j+1, j+3):
                                if Ser_TT[k] != 0:
                                    l = 2
                                    j = k
                                    break
                                else:
                                    l = 5
                        else:
                            l = 5
                    
                    elif j < (len(Ser_TT)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-3
                        if np.any(Ser_TT[j+1:j+2] != 0) == True:
                            for k in range(j+1, j+2):
                                if Ser_TT[k] != 0:
                                    l = 2
                                    j = k
                                    break
                                else:
                                    l = 5
                        else:
                            l = 5                
                    else:
                        l = 5
                else:
                    l = 5
            evn_TT.append((i,j))       
            i = j+8 # ésta sería la nueva posición donde comienza todo el bucle     
        else:
            i = i+1 # Siguiente posicion a examinar
    EVN_TT = np.array((evn_TT))
    return EVN_TT

EVN_TT = indices_eventos(Ser_TT)
EVN_PP = indices_eventos(Ser_PP)
EVN_PN = indices_eventos(Ser_PN)

################ 
"DERIVADA EN TT"
################

#ano_TT
#EVN_TT

def derived(serie, index, path, chorro):
    ano_max = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    ano_min = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    
    lim_sup = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    lim_inf = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    for q in range(len(index[:,0])):
        if index[q,0] != index[q,1]:
            c = index[q,0]+np.where(serie[index[q,0]:index[q,1]+1] == np.max(serie[index[q,0]:index[q,1]+1]))
            cc = c[0,0]
            if serie[cc-12] > ano_max:
                ano_max = serie[cc-12]
            if serie[cc-12] < ano_min:
                ano_min = serie[cc-12]
            if np.max(serie[cc-12:cc+13]) > lim_sup:
                lim_sup = np.max(serie[cc-12:cc+13])
            if np.min(serie[cc-6:cc+7]) < lim_inf:
                lim_inf = np.min(serie[cc-12:cc+13])
        else:
            cc = index[q,0]
            if serie[cc-12] > ano_max:
                ano_max = serie[cc-12]
            if serie[cc-12] < ano_min:
                ano_min = serie[cc-12]
            if np.max(serie[cc-12:cc+13]) > lim_sup:
                lim_sup = np.max(serie[cc-12:cc+13])
            if np.min(serie[cc-12:cc+12]) < lim_inf:
                lim_inf = np.min(serie[cc-12:cc+13])


    ano_Max = ano_max//1+1
    ano_Min = ano_min//1 

    ano_Max.astype(int)
    ano_Min.astype(int)


    der_Max = 1
    der_Min = 1
    
    for f in np.arange(ano_Min, ano_Max+1):
        fig = plt.figure(figsize=(8,6))
        ax1 = fig.add_subplot(111)
        for g in range(len(index[:,0])):
            if index[g,0] != index[g,1]:
                c = index[g,0]+np.where(serie[index[g,0]:index[g,1]+1] == np.max(serie[index[g,0]:index[g,1]+1]))
                cc = c[0,0]
                if cc <= len(serie)-13:        
                    if f <= serie[cc-12] < f+1:
                        der = np.zeros(len(serie[cc-12:cc+13]))                
                        for h in range(len(der)):
                            der[h] = serie[cc-12+h+1] - serie[cc-12+h]
                        if np.max(der) > der_Max:
                            der_Max = np.max(der)
                        if np.min(der) < der_Min:
                            der_Min = np.min(der)
            else:
                if index[g,1] <= len(serie)-13:        
                    if f+1 <= serie[index[g,1]-12]< f+1:
                        der = np.zeros(len(serie[cc-12:cc+13]))
                        for h in range(len(der)):
                            der[h] = serie[index[g,1]-12+h+1] - serie[index[g,1]-12+h] 
                        if np.max(der) > der_Max:
                            der_Max = np.max(der)
                        if np.min(der) < der_Min:
                            der_Min = np.min(der)
    
    
    for r in np.arange(ano_Min, ano_Max+1):
        fig = plt.figure(figsize=(8,6))
        ax1 = fig.add_subplot(111)
        for i in range(len(index[:,0])):
            if index[i,0] != index[i,1]:
                c = index[i,0]+np.where(serie[index[i,0]:index[i,1]+1] == np.max(serie[index[i,0]:index[i,1]+1]))
                cc = c[0,0]
                if cc <= len(serie)-13:        
                    if r <= serie[cc-12] < r+1:
                        der = np.zeros(len(serie[cc-12:cc+13]))                
                        for j in range(len(der)):
                            der[j] = serie[cc-12+j+1] - serie[cc-12+j]
                        ax1.plot( serie[cc-12:cc+13], der, '.', color='k')
            else:
                if index[i,1] <= len(serie)-13:        
                    if r+1 <= serie[index[i,1]-12]< r+1:
                        der = np.zeros(len(serie[cc-12:cc+13]))
                        for j in range(len(der)):
                            der[j] = serie[index[i,1]-12+j+1] - serie[index[i,1]-12+j] 
                        ax1.plot(serie[index[i,1]-12:index[i,1]+13], der, '.', color='k')
        ax1.grid(True)
        ax1.set_xlabel('$Velocity$ $(m/s)$', size='15')
        ax1.set_xlim(lim_inf-1, lim_sup+1)
        ax1.set_ylabel('$\Delta$ $Speed$ $(m/s)$', size='15')
        ax1.set_ylim(der_Min-0.5, der_Max+0.5)
        ax1.set_title('Speed derived ('+chorro+', '+str(r)+', '+str(r+1)+')', size='14')
        ax1.legend(loc='best')
        plt.savefig(path +'/'+chorro+str(r)+'_'+str(r+1)+'.png',dpi=100, bbox_inches='tight')
        plt.close('all')
    return lim_inf, lim_sup

#########
"PLOT TT"
#########

def eventos_centro(ano_TT, EVN_TT, path, chorro):
    colores = ['#0B0B61', '#045FB4', '#00FF80','#80FF00','#BFFF00','#FFFF00','#FFBF00','#FF8000','#FF4000','#DF0101', '#8A0808']

    ano_max = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    ano_min = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    
    lim_sup = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    lim_inf = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    
    ymax = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    ymin = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
  
    for q in range(len(EVN_TT[:,0])):
        if EVN_TT[q,0] != EVN_TT[q,1]:
            c = EVN_TT[q,0]+np.where(ano_TT[EVN_TT[q,0]:EVN_TT[q,1]+1] == np.max(ano_TT[EVN_TT[q,0]:EVN_TT[q,1]+1]))
            cc = c[0,0]
            if ano_TT[cc] > ano_max:
                ano_max = ano_TT[cc]
            if ano_TT[cc] < ano_min:
                ano_min = ano_TT[cc]
            if np.max(ano_TT[cc-12]) > lim_sup:
                lim_sup = np.max(ano_TT[cc-12])
            if np.min(ano_TT[cc-12]) < lim_inf:
                lim_inf = np.min(ano_TT[cc-12])
            if np.max(ano_TT[cc-12:cc+13]) > ymax:
                ymax = np.max(ano_TT[cc-12:cc+13])
            if np.min(ano_TT[cc-6:cc+7]) < ymin:
                ymin = np.min(ano_TT[cc-12:cc+13])
        else:
            cc = EVN_TT[q,0]
            if ano_TT[cc] > ano_max:
                ano_max = ano_TT[cc]
            if ano_TT[cc] < ano_min:
                ano_min = ano_TT[cc]
            if np.max(ano_TT[cc-12]) > lim_sup:
                lim_sup = np.max(ano_TT[cc-12])
            if np.min(ano_TT[cc-12]) < lim_inf:
                lim_inf = np.min(ano_TT[cc-12])
            if np.max(ano_TT[cc-12:cc+13]) > ymax:
                ymax = np.max(ano_TT[cc-12:cc+13])
            if np.min(ano_TT[cc-6:cc+7]) < ymin:
                ymin = np.min(ano_TT[cc-12:cc+13])

       
    ano_max = ano_max/1
    ano_min = ano_min/1
    ano_max = ano_max.astype(int)
    ano_min = ano_min.astype(int)

    lim_inf = lim_inf/1
    lim_sup = lim_sup/1
    lim_inf = lim_inf.astype(int)
    lim_sup = lim_sup.astype(int)

    for z in np.arange(ano_min, ano_max+1):
    
        fig = plt.figure(figsize=(8,3))
        ax1 = fig.add_subplot(111)
        for i in range(len(EVN_TT[:,0])):
            if EVN_TT[i,0] != EVN_TT[i,1]:
                c = EVN_TT[i,0]+np.where(ano_TT[EVN_TT[i,0]:EVN_TT[i,1]+1] == np.max(ano_TT[EVN_TT[i,0]:EVN_TT[i,1]+1]))
                cc = c[0,0]
                if cc <= len(ano_TT)-13:        
                    if z <= ano_TT[cc] < z+1:       
                        for j, k in enumerate(np.arange(lim_inf,lim_sup,2)):                
                            if k <= ano_TT[cc-12] < k+2:
                                ax1.plot(range(0,25), ano_TT[cc-12:cc+13], linewidth=0.7, color= colores[j] , alpha = 0.6)
            else:
                if EVN_TT[i,1] <= len(ano_TT)-13:        
                    if z <= ano_TT[EVN_TT[i,1]]< z+1:
                        for j, k in enumerate(np.arange(lim_inf,lim_sup,2)):                
                            if k <= ano_TT[EVN_TT[i,1]-12] < k+2:
                                ax1.plot(range(0,25), ano_TT[EVN_TT[i,1]-12:EVN_TT[i,1]+13], linewidth=1, color= colores[j], alpha = 0.6)                

        my_xticks = ['-36:00','-30:00','-24:00', '-18:00', '-12:00', '-06:00', '00:00', '06:00', '12:00', '18:00', '24:00', '30:00', '36:00']
        plt.xticks((0, 2, 4, 6, 8, 10 , 12, 14, 16, 18, 20, 22, 24),my_xticks)
        ax1.grid(True)
        ax1.set_xlabel('$Time$ $(h)$', size='15')
        ax1.set_ylabel('$Speed$ $(m/s)$', size='15')
        ax1.set_ylim(ymin-1, ymax+1)
        ax1.set_title('Speed derived ('+chorro+', '+str(z)+', '+str(z+1)+')', size='14')
        ax1.legend(loc='best')
        plt.savefig(path +'/'+chorro+str(z)+'_'+str(z+1)+'.png',dpi=100, bbox_inches='tight')
        plt.close('all')
    return z

##################
"PLOT TT COMIENZO"
##################
def eventos_comienzo(ano_TT, EVN_TT, path, chorro):    
    ano_max = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    ano_min = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
        
    lim_sup = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    lim_inf = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    
    ymax = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    ymin = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    
    
    for q in range(len(EVN_TT[:,0])):
        if EVN_TT[q,0] != EVN_TT[q,1]:
            c = EVN_TT[q,0]+np.where(ano_TT[EVN_TT[q,0]:EVN_TT[q,1]+1] == np.max(ano_TT[EVN_TT[q,0]:EVN_TT[q,1]+1]))
            cc = c[0,0]
            if ano_TT[cc] > ano_max:
                ano_max = ano_TT[cc]
            if ano_TT[cc] < ano_min:
                ano_min = ano_TT[cc]
            if np.max(ano_TT[cc-12]) > lim_sup:
                lim_sup = np.max(ano_TT[cc-12])
            if np.min(ano_TT[cc-12]) < lim_inf:
                lim_inf = np.min(ano_TT[cc-12])
            if np.max(ano_TT[cc-12:cc+13]) > ymax:
                ymax = np.max(ano_TT[cc-12:cc+13])
            if np.min(ano_TT[cc-6:cc+7]) < ymin:
                ymin = np.min(ano_TT[cc-12:cc+13])
    
    
        else:
            cc = EVN_TT[q,0]
            if ano_TT[cc] > ano_max:
                ano_max = ano_TT[cc]
            if ano_TT[cc] < ano_min:
                ano_min = ano_TT[cc]
            if np.max(ano_TT[cc-12]) > lim_sup:
                lim_sup = np.max(ano_TT[cc-12])
            if np.min(ano_TT[cc-12]) < lim_inf:
                lim_inf = np.min(ano_TT[cc-12])
            if np.max(ano_TT[cc-12:cc+13]) > ymax:
                ymax = np.max(ano_TT[cc-12:cc+13])
            if np.min(ano_TT[cc-6:cc+7]) < ymin:
                ymin = np.min(ano_TT[cc-12:cc+13])
    
    ano_max = ano_max/1
    ano_min = ano_min/1
    ano_max = ano_max.astype(int)
    ano_min = ano_min.astype(int)
    
    lim_inf = lim_inf/1
    lim_sup = lim_sup/1
    lim_inf = lim_inf.astype(int)
    lim_sup = lim_sup.astype(int)
    
    
    for w in np.arange(lim_inf, lim_sup): 
        fig = plt.figure(figsize=(8,3))
        ax1 = fig.add_subplot(111)
        for i in range(len(EVN_TT[:,0])):
            if EVN_TT[i,0] != EVN_TT[i,1]:
                c = EVN_TT[i,0]+np.where(ano_TT[EVN_TT[i,0]:EVN_TT[i,1]+1] == np.max(ano_TT[EVN_TT[i,0]:EVN_TT[i,1]+1]))
                cc = c[0,0]
                if cc <= len(ano_TT)-13:
                    if w <= ano_TT[cc-12] < w+1:       
                        ax1.plot(range(0,25) ,ano_TT[cc-12:cc+13], linewidth=0.7, color='#9437f1', alpha = 0.6)
            else:
                if EVN_TT[i,1] <= len(ano_TT)-13:        
                    if w+1 <= ano_TT[EVN_TT[i,1]-12]< w+1:
                        ax1.plot(range(0,25), ano_TT[EVN_TT[i,1]-12:EVN_TT[i,1]+13], linewidth=0.7, color='#9437f1', alpha = 0.4)
        my_xticks = ['-36:00','-30:00','-24:00', '-18:00', '-12:00', '-06:00', '00:00', '06:00', '12:00', '18:00', '24:00', '30:00', '36:00']
        plt.xticks((0, 2, 4, 6, 8, 10 , 12, 14, 16, 18, 20, 22, 24),my_xticks)
        ax1.grid(True)
        ax1.set_xlabel('$Time$ $(h)$', size='15')
        ax1.set_ylabel('$Speed$ $(m/s)$', size='15')
        ax1.set_ylim(ymin-1, ymax+1)
        ax1.set_title('Speed derived ('+chorro+', '+str(w)+', '+str(w+1)+')', size='14')
        ax1.legend(loc='best')
        plt.savefig(path +'/'+chorro+str(w)+'_'+str(w+1)+'.png',dpi=100, bbox_inches='tight')
        plt.close('all')
    