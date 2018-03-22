# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 23:33:09 2016

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

