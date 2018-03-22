# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:20:13 2016

@author: yordan
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 00:27:45 2016

@author: yordan
"""

import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/U y V, 6 horas, 10 m, 1979-2016.nc')

######################################## 
"ZONAS DE ALTA INFLUENCIA EN TT, PP, PN"
########################################

u_TT = Archivo.variables['u10'][:54056, 4:19, 7:18] # serie desde 1979/01/01 hasta 2015/12/31
v_TT = Archivo.variables['v10'][:54056, 4:19, 7:18]
u_PP = Archivo.variables['u10'][:54056, 21:34, 30:49]
v_PP = Archivo.variables['v10'][:54056, 21:34, 30:49]
u_PN = Archivo.variables['u10'][:54056, 34:47, 69:78]
v_PN = Archivo.variables['v10'][:54056, 34:47, 69:78]

########################
"VEOCIDAD EN CADA PIXEL"
########################

velTT = np.sqrt(u_TT*u_TT+v_TT*v_TT) 
velPP = np.sqrt(u_PP*u_PP+v_PP*v_PP)
velPN = np.sqrt(u_PN*u_PN+v_PN*v_PN)

###################### 
"COMPOSITE TT, PP, PN"
######################

spd_TT = np.zeros(54056)
spd_PP = np.zeros(54056)
spd_PN = np.zeros(54056)

for i in range(54056):
    spd_TT[i] = np.mean(velTT[i,:,:])
    spd_PP[i] = np.mean(velPP[i,:,:])
    spd_PN[i] = np.mean(velPN[i,:,:])

##############
"CICLO DIURNO"
##############

serie_TT = spd_TT 
media_TT = np.zeros((12,4)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
fechas = pd.date_range('1979/01/01', periods=54056, freq='6H') # serie con fechas cada 6 horas, desde 1979/01/01 hasta 2015/12/31

for i in range(1,13): # Se recorre cada mes
    for j in range(0, 19, 6): # Se recorre cada horario
        selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
        for k in range(len(serie_TT)): # Se recorre toda la serie
            if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                    selec.append(serie_TT[k]) # Si cumple, se adiciona a la lista
        media_TT[i-1, j/6] = np.mean(selec) # Se guarda wl valor de la media




serie_PP = spd_PP 
media_PP = np.zeros((12,4)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
fechas = pd.date_range('1979/01/01', periods=54056, freq='6H') # serie con fechas cada 6 horas, desde 1979/01/01 hasta 2015/12/31

for i in range(1,13): # Se recorre cada mes
    for j in range(0, 19, 6): # Se recorre cada horario
        selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
        for k in range(len(serie_PP)): # Se recorre toda la serie
            if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                    selec.append(serie_PP[k]) # Si cumple, se adiciona a la lista
        media_PP[i-1, j/6] = np.mean(selec) # Se guarda wl valor de la media




serie_PN = spd_PN 
media_PN = np.zeros((12,4)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
fechas = pd.date_range('1979/01/01', periods=54056, freq='6H') # serie con fechas cada 6 horas, desde 1979/01/01 hasta 2015/12/31

for i in range(1,13): # Se recorre cada mes
    for j in range(0, 19, 6): # Se recorre cada horario
        selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
        for k in range(len(serie_PN)): # Se recorre toda la serie
            if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                    selec.append(serie_PN[k]) # Si cumple, se adiciona a la lista
        media_PN[i-1, j/6] = np.mean(selec) # Se guarda wl valor de la media

####################
"ANOMALÍAS HORARIAS"
####################        
ano_TT = np.zeros(len(serie_TT))
for i in range(len(serie_TT)):
    ano_TT[i] = serie_TT[i]-media_TT[fechas[i].month-1, fechas[i].hour/6]


ano_PP = np.zeros(len(serie_PP))
for i in range(len(serie_PP)):
    ano_PP[i] = serie_PP[i]-media_PP[fechas[i].month-1, fechas[i].hour/6]


ano_PN = np.zeros(len(serie_PN))
for i in range(len(serie_PN)):
    ano_PN[i] = serie_PN[i]-media_PN[fechas[i].month-1, fechas[i].hour/6]
    
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

i = 0
evn_TT = []

while i<(len(Ser_TT)-1):    
    if Ser_TT[i] != 0: # Primero se verifica que la posición i tenga un valor
        j = i
        l = 3 # Esto es para poder entrar al while
        while l <= 4:        
            if j < (len(Ser_TT)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector ser, la siguiente línea arrojará un error
                while Ser_TT[j+1] != 0: # Se hace éste while para saber hasta qué posición llega el evento 
                    j = j+1
                    if j == (len(Ser_TT)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de ser, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                        break
                
                if j < (len(Ser_TT)-5): # Esta línea es debida a la siguiente, para que no se genere un error
                    if np.any(Ser_TT[j+1:j+5] != np.zeros(4)) == True: # Se debe revisar que las siguientes cuatro posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                        for k in range(j+1, j+5): # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero 
                            if Ser_TT[k] != 0:
                                l = 2 # Para que el while se vuelva a repetir
                                j = k
                                break
                            else:
                                l = 5 # Para que el while no se vuelva a repetir
                    else:
                        l = 5 # Para que el while no se vuelva a repetir
                
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
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar
EVN_TT = np.array((evn_TT))

###################################
"ÍNDICES EN LOS QUE HAY EVENTOS PP"
###################################
i = 0
evn_PP = []

while i<(len(Ser_PP)-1):    
    if Ser_PP[i] != 0: # Primero se verifica que la posición i tenga un valor
        j = i
        l = 3
        while l <= 4:        
            if j < (len(Ser_PP)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector ser, la siguiente línea arrojará un error
                while Ser_PP[j+1] != 0: # Se hace éste while para saber hasta qué posición llega el evento 
                    j = j+1
                    if j == (len(Ser_PP)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de ser, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                        break
                
                if j < (len(Ser_PP)-5): # Esta línea es debida a la siguiente, para que no se genere un error
                    if np.any(Ser_PP[j+1:j+5] != np.zeros(4)) == True: # Se debe revisar que las siguientes cuatro posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                        for k in range(j+1, j+5): # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero 
                            if Ser_PP[k] != 0:
                                l = 2 # Para que el while se vuelva a repetir
                                j = k
                                break
                            else:
                                l = 5 # Para que el while no se vuelva a repetir
                    else:
                        l = 5 # Para que el while no se vuelva a repetir
                elif j < (len(Ser_PP)-4): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-5
                    if np.any(Ser_PP[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if Ser_PP[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5                        
                elif j < (len(Ser_PP)-3): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-4
                    if np.any(Ser_PP[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if Ser_PP[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(Ser_PP)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-3
                    if np.any(Ser_PP[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if Ser_PP[k] != 0:
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
        evn_PP.append((i,j))       
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar
EVN_PP = np.array((evn_PP))

###################################
"ÍNDICES EN LOS QUE HAY EVENTOS PN"
###################################
i = 0
evn_PN = []

while i<(len(Ser_PN)-1):    
    if Ser_PN[i] != 0: # Primero se verifica que la posición i tenga un valor
        j = i
        l = 3
        while l <= 4:        
            if j < (len(Ser_PN)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector ser, la siguiente línea arrojará un error
                while Ser_PN[j+1] != 0: # Se hace éste while para saber hasta qué posición llega el evento 
                    j = j+1
                    if j == (len(Ser_PN)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de ser, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                        break
                
                if j < (len(Ser_PN)-5): # Esta línea es debida a la siguiente, para que no se genere un error
                    if np.any(Ser_PN[j+1:j+5] != np.zeros(4)) == True: # Se debe revisar que las siguientes cuatro posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                        for k in range(j+1, j+5): # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero 
                            if Ser_PN[k] != 0:
                                l = 2 # Para que el while se vuelva a repetir
                                j = k
                                break
                            else:
                                l = 5 # Para que el while no se vuelva a repetir
                    else:
                        l = 5 # Para que el while no se vuelva a repetir
                elif j < (len(Ser_PN)-4): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-5
                    if np.any(Ser_PN[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if Ser_PN[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5                        
                elif j < (len(Ser_PN)-3): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-4
                    if np.any(Ser_PN[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if Ser_PN[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(Ser_PN)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-3
                    if np.any(Ser_PN[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if Ser_PN[k] != 0:
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
        evn_PN.append((i,j))       
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar
EVN_PN = np.array((evn_PN))

#==============================================================================
"Máximos de cada evento"
#==============================================================================

def eventos_maximos(spd, EVN):
    fechas = pd.date_range('1979-01-01 00:00:00', '2015-12-31 18:00:00', freq='6H')
    SERIE = pd.DataFrame(index= fechas, columns=['spd'])
    SERIE['spd'] = spd
    MAX    = []
    CUANDO = []    
    for i in range(len(EVN)):
        serie_alt = SERIE[EVN[i,0]:EVN[i,1]+1]
        Max       = np.max(serie_alt)[0]
        cuando    = serie_alt.index[(serie_alt.spd == Max)]
        MAX.append(Max)
        CUANDO.append(cuando)
    return CUANDO, MAX
    
cuandoTT, max_TT = eventos_maximos(spd_TT, EVN_TT)
cuandoPP, max_PP = eventos_maximos(spd_PP, EVN_PP)
cuandoPN, max_PN = eventos_maximos(spd_PN, EVN_PN)

for i in range(len(max_TT)):
    if max_TT[i] > 18.0:
        print cuandoTT[i], max_TT[i]
        #print cuandoTT[i], max_TT[i], fechas[EVN_TT[i,0]:EVN_TT[i,1]+1], spd_TT[EVN_TT[i,0]:EVN_TT[i,1]+1]
        
for i in range(len(max_PP)):
    if max_PP[i] > 12.9:
        print cuandoPP[i], max_PP[i]
        #print cuandoPP[i], max_PP[i], fechas[EVN_PP[i,0]:EVN_PP[i,1]+1], spd_PP[EVN_PP[i,0]:EVN_PP[i,1]+1]

for i in range(len(max_PN)):
    if max_PN[i] > 10.94:
        print cuandoPN[i], max_PN[i]
        #print cuandoPN[i], max_PN[i], fechas[EVN_PN[i,0]:EVN_PN[i,1]+1], spd_PN[EVN_PN[i,0]:EVN_PN[i,1]+1]
