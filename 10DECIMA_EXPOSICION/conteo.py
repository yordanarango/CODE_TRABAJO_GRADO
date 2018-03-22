# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 08:48:23 2016

@author: yordan
"""

import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pylab import hist, show
import pylab as pl
from numpy import genfromtxt

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

##############################################################################
"IDENTIFICACIÓN DE FECHAS QUE SUPERAN UMBRAL DE LAS DOS DESVIACIONES ESTANDAR"
##############################################################################

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

##################################################################
"NÚMERO  DE EVENTOS DE CADA MES EN TT (BASE DE DATOS ERA INTERIM)"
##################################################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
year = pd.date_range('1998/01/01', '2009/12/31',freq='A')
cont_TT = np.zeros(len(year))
i = 0
ser_TT = Ser_TT[27760:45292]# Corresponde al período entre 1998 y 2009


while i<(len(ser_TT)-1):    
    if ser_TT[i] != 0: # Primero se verifica que la posición i tenga un valor
        j = i
        l = 3
        while l <= 4:        
            if j < (len(ser_TT)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector ser, la siguiente línea arrojará un error
                while ser_TT[j+1] != 0: # Se hace éste while para saber hasta qué posición llega el evento 
                    j = j+1
                    if j == (len(ser_TT)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de ser, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                        break
                
                if j < (len(ser_TT)-5): # Esta línea es debida a la siguiente, para que no se genere un error
                    if np.any(ser_TT[j+1:j+5] != np.zeros(4)) == True: # Se debe revisar que las siguientes cuatro posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                        for k in range(j+1, j+5): # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero 
                            if ser_TT[k] != 0:
                                l = 2 # Para que el while se vuelva a repetir
                                j = k
                                break
                            else:
                                l = 5 # Para que el while no se vuelva a repetir
                    else:
                        l = 5 # Para que el while no se vuelva a repetir
                elif j < (len(ser_TT)-4): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-5
                    if np.any(ser_TT[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if ser_TT[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5                        
                elif j < (len(ser_TT)-3): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-4
                    if np.any(ser_TT[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if ser_TT[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(ser_TT)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-3
                    if np.any(ser_TT[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if ser_TT[k] != 0:
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
        for jj, kk in enumerate(year):
            if fechas1[i].year == kk.year: 
                cont_TT[jj] = cont_TT[jj]+1
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar
cont4 = cont_TT

##################################################################
"NÚMERO  DE EVENTOS DE CADA MES EN PP (BASE DE DATOS ERA INTERIM)"
##################################################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
year = pd.date_range('1998/01/01', '2009/12/31',freq='A')
cont_PP = np.zeros(len(year))
i = 0
ser_PP = Ser_PP[27760:45292] # Corresponde al período entre 1998 y 2009


while i<(len(ser_PP)-1):    
    if ser_PP[i] != 0: # Primero se verifica que la posición i tenga un valor
        j = i
        l = 3
        while l <= 4:        
            if j < (len(ser_PP)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector ser, la siguiente línea arrojará un error
                while ser_PP[j+1] != 0: # Se hace éste while para saber hasta qué posición llega el evento 
                    j = j+1
                    if j == (len(ser_PP)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de ser, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                        break
                
                if j < (len(ser_PP)-5): # Esta línea es debida a la siguiente, para que no se genere un error
                    if np.any(ser_PP[j+1:j+5] != np.zeros(4)) == True: # Se debe revisar que las siguientes cuatro posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                        for k in range(j+1, j+5): # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero 
                            if ser_PP[k] != 0:
                                l = 2 # Para que el while se vuelva a repetir
                                j = k
                                break
                            else:
                                l = 5 # Para que el while no se vuelva a repetir
                    else:
                        l = 5 # Para que el while no se vuelva a repetir
                elif j < (len(ser_PP)-4): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-5
                    if np.any(ser_PP[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if ser_PP[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5                        
                elif j < (len(ser_PP)-3): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-4
                    if np.any(ser_PP[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if ser_PP[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(ser_PP)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-3
                    if np.any(ser_PP[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if ser_PP[k] != 0:
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
        for jj, kk in enumerate(year):
            if fechas1[i].year == kk.year: 
                cont_PP[jj] = cont_PP[jj]+1
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar
cont5 = cont_PP

##################################################################
"NÚMERO  DE EVENTOS DE CADA MES EN PP (BASE DE DATOS ERA INTERIM)"
##################################################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
year = pd.date_range('1998/01/01', '2009/12/31',freq='A')
cont_PN = np.zeros(len(year))
i = 0
ser_PN = Ser_PN[27760:45292] # Corresponde al período entre 1998 y 2009


while i<(len(ser_PN)-1):    
    if ser_PN[i] != 0: # Primero se verifica que la posición i tenga un valor
        j = i
        l = 3
        while l <= 4:        
            if j < (len(ser_PN)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector ser, la siguiente línea arrojará un error
                while ser_PN[j+1] != 0: # Se hace éste while para saber hasta qué posición llega el evento 
                    j = j+1
                    if j == (len(ser_PN)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de ser, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                        break
                
                if j < (len(ser_PN)-5): # Esta línea es debida a la siguiente, para que no se genere un error
                    if np.any(ser_PN[j+1:j+5] != np.zeros(4)) == True: # Se debe revisar que las siguientes cuatro posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                        for k in range(j+1, j+5): # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero 
                            if ser_PN[k] != 0:
                                l = 2 # Para que el while se vuelva a repetir
                                j = k
                                break
                            else:
                                l = 5 # Para que el while no se vuelva a repetir
                    else:
                        l = 5 # Para que el while no se vuelva a repetir
                elif j < (len(ser_PN)-4): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-5
                    if np.any(ser_PN[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if ser_PN[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5                        
                elif j < (len(ser_PN)-3): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-4
                    if np.any(ser_PN[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if ser_PN[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(ser_PN)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-3
                    if np.any(ser_PN[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if ser_PN[k] != 0:
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
        for jj, kk in enumerate(year):
            if fechas1[i].year == kk.year: 
                cont_PN[jj] = cont_PN[jj]+1
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar
cont6 = cont_PN

total = cont6+cont5+cont4