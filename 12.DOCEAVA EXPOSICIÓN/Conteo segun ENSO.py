# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 17:57:44 2016

@author: yordan
"""
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

#==============================================================================
'''Datos de viento'''
#==============================================================================
Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/U y V, 6 horas, 10 m, 1979-2016.nc')

#==============================================================================
"ZONAS DE ALTA INFLUENCIA EN TT, PP, PN"
#==============================================================================

u_TT = Archivo.variables['u10'][:54056, 4:19, 7:18] # serie desde 1979/01/01 hasta 2015/12/31
v_TT = Archivo.variables['v10'][:54056, 4:19, 7:18]
u_PP = Archivo.variables['u10'][:54056, 21:34, 30:49]
v_PP = Archivo.variables['v10'][:54056, 21:34, 30:49]
u_PN = Archivo.variables['u10'][:54056, 34:47, 69:78]
v_PN = Archivo.variables['v10'][:54056, 34:47, 69:78]

#==============================================================================
"VEOCIDAD EN CADA PIXEL"
#==============================================================================

velTT = np.sqrt(u_TT*u_TT+v_TT*v_TT) 
velPP = np.sqrt(u_PP*u_PP+v_PP*v_PP)
velPN = np.sqrt(u_PN*u_PN+v_PN*v_PN)

#==============================================================================
"COMPOSITE TT, PP, PN"
#==============================================================================

spd_TT = np.zeros(54056)
spd_PP = np.zeros(54056)
spd_PN = np.zeros(54056)

for i in range(54056):
    spd_TT[i] = np.mean(velTT[i,:,:])
    spd_PP[i] = np.mean(velPP[i,:,:])
    spd_PN[i] = np.mean(velPN[i,:,:])

#==============================================================================
"IDENTIFICACIÓN DE FECHAS QUE SUPERAN UMBRAL TT-7, PP-6.5, PN-6.5"
#==============================================================================

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

#==============================================================================
"ÍNDICES EN LOS QUE HAY EVENTOS TT"
#==============================================================================

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

#==============================================================================
"ÍNDICES EN LOS QUE HAY EVENTOS PP"
#==============================================================================
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

#==============================================================================
"ÍNDICES EN LOS QUE HAY EVENTOS PN"
#==============================================================================
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
"FECHAS CADA 6H y mensual"
#==============================================================================

FECHAS = pd.date_range('1979-01-01 00:00:00', '2015-12-31 18:00:00', freq='6H')
fechas = pd.date_range('1979-01-31', '2015-12-31', freq = 'M')

#==============================================================================
"CONTADOR DE NUMERO DE EVENTOS POR MES Y VELOCIDAD MEDIA DE LOS EVENTOS DE CADA MES"
#==============================================================================

def criterio_ENSO(EVN, FECHAS, ENSO_FASE, serie): 
    # ENV      : lista con los posiciones de inicio y final de cada evento
    # FECHAS   : fechas con alta resolución, cada 6 horas
    # ENSO_FASE: DataFrame con fechas en resolución mensual y números indicando fase del ENSO (-1, 0, 1)
    # serie    : serie de vientos con resoluciń cada 6 horas    
    enso_fase = ENSO_FASE    
    enso_fase['contador'] = np.zeros(len(enso_fase)) # contendrá el número de eventos por cada mes
    enso_fase['suma'] = np.zeros(len(enso_fase)) # contendrá la suma de los valores medios de cada evento
    for i in range(len(EVN)):
        indx1 = EVN[i][0]
        indx2 = EVN[i][1]
        ano = FECHAS[indx1].year
        mes = FECHAS[indx1].month
        for j in range(len(enso_fase.index)): #Buscando en las fechas de baja resolución(mensual) cual tiene el mismo mes y el mismo año. Luego la fase del ENSO asociada con esa fecha será la que se asigne al índice de interés 
            if ano == enso_fase.index[j].year and mes == enso_fase.index[j].month:
                enso_fase['contador'][j] = enso_fase['contador'][j]+1
                enso_fase['suma'][j] = enso_fase['suma'][j]+np.mean(serie[indx1:indx2+1])

    return enso_fase

##### TT #######==============================================================================
'''enso fase según SOI index 1 = cálido, -1 = frío, 0 = neutro'''
#==============================================================================

ENSO_FASE = pd.DataFrame(index = fechas, columns=['rango'])

ENSO_FASE['rango']['1979-01-31':'1979-12-31'] = [0,0,0,0,0,0,0,0,0,1,1,1]
ENSO_FASE['rango']['1980-01-31':'1980-12-31'] = [1,1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1981-01-31':'1981-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1982-01-31':'1982-12-31'] = [0,0,0,1,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1983-01-31':'1983-12-31'] = [1,1,1,1,1,1,0,0,0,0,0,0]
ENSO_FASE['rango']['1984-01-31':'1984-12-31'] = [0,0,0,0,0,0,0,0,0,-1,-1,-1]
ENSO_FASE['rango']['1985-01-31':'1985-12-31'] = [-1,-1,-1,-1,-1,-1,0,0,0,0,0,0]
ENSO_FASE['rango']['1986-01-31':'1986-12-31'] = [0,0,0,0,0,0,0,0,1,1,1,1]
ENSO_FASE['rango']['1987-01-31':'1987-12-31'] = [1,1,1,1,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1988-01-31':'1988-12-31'] = [1,1,0,0,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1989-01-31':'1989-12-31'] = [-1,-1,-1,-1,-1,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1990-01-31':'1990-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1991-01-31':'1991-12-31'] = [0,0,0,0,0,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1992-01-31':'1992-12-31'] = [1,1,1,1,1,1,1,0,0,0,0,0]
ENSO_FASE['rango']['1993-01-31':'1993-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1994-01-31':'1994-12-31'] = [0,0,0,0,0,0,0,0,0,1,1,1]
ENSO_FASE['rango']['1995-01-31':'1995-12-31'] = [1,1,1,0,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1996-01-31':'1996-12-31'] = [-1,-1,-1,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1997-01-31':'1997-12-31'] = [0,0,0,0,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1998-01-31':'1998-12-31'] = [1,1,1,1,1,0,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1999-01-31':'1999-12-31'] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2000-01-31':'2000-12-31'] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2001-01-31':'2001-12-31'] = [-1,-1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2002-01-31':'2002-12-31'] = [0,0,0,0,0,1,1,1,1,1,1,1]
ENSO_FASE['rango']['2003-01-31':'2003-12-31'] = [1,1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2004-01-31':'2004-12-31'] = [0,0,0,0,0,0,1,1,1,1,1,1]
ENSO_FASE['rango']['2005-01-31':'2005-12-31'] = [1,1,1,1,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2006-01-31':'2006-12-31'] = [0,0,0,0,0,0,0,0,1,1,1,1]
ENSO_FASE['rango']['2007-01-31':'2007-12-31'] = [1,0,0,0,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2008-01-31':'2008-12-31'] = [-1,-1,-1,-1,-1,-1,0,0,0,0,0,0]
ENSO_FASE['rango']['2009-01-31':'2009-12-31'] = [0,0,0,0,0,0,1,1,1,1,1,1]
ENSO_FASE['rango']['2010-01-31':'2010-12-31'] = [1,1,1,1,0,0,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2011-01-31':'2011-12-31'] = [-1,-1,-1,-1,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2012-01-31':'2012-12-31'] = [-1,-1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2013-01-31':'2013-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2014-01-31':'2014-12-31'] = [0,0,0,0,0,0,0,0,0,0,1,1]
ENSO_FASE['rango']['2015-01-31':'2015-12-31'] = [1,1,1,1,1,1,1,1,1,1,1,1]

ENSO_TT = criterio_ENSO(EVN_TT, FECHAS, ENSO_FASE, spd_TT)



#### PP #######==============================================================================
'''enso fase según SOI index 1 = cálido, -1 = frío, 0 = neutro'''
#==============================================================================

ENSO_FASE = pd.DataFrame(index = fechas, columns=['rango'])

ENSO_FASE['rango']['1979-01-31':'1979-12-31'] = [0,0,0,0,0,0,0,0,0,1,1,1]
ENSO_FASE['rango']['1980-01-31':'1980-12-31'] = [1,1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1981-01-31':'1981-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1982-01-31':'1982-12-31'] = [0,0,0,1,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1983-01-31':'1983-12-31'] = [1,1,1,1,1,1,0,0,0,0,0,0]
ENSO_FASE['rango']['1984-01-31':'1984-12-31'] = [0,0,0,0,0,0,0,0,0,-1,-1,-1]
ENSO_FASE['rango']['1985-01-31':'1985-12-31'] = [-1,-1,-1,-1,-1,-1,0,0,0,0,0,0]
ENSO_FASE['rango']['1986-01-31':'1986-12-31'] = [0,0,0,0,0,0,0,0,1,1,1,1]
ENSO_FASE['rango']['1987-01-31':'1987-12-31'] = [1,1,1,1,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1988-01-31':'1988-12-31'] = [1,1,0,0,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1989-01-31':'1989-12-31'] = [-1,-1,-1,-1,-1,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1990-01-31':'1990-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1991-01-31':'1991-12-31'] = [0,0,0,0,0,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1992-01-31':'1992-12-31'] = [1,1,1,1,1,1,1,0,0,0,0,0]
ENSO_FASE['rango']['1993-01-31':'1993-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1994-01-31':'1994-12-31'] = [0,0,0,0,0,0,0,0,0,1,1,1]
ENSO_FASE['rango']['1995-01-31':'1995-12-31'] = [1,1,1,0,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1996-01-31':'1996-12-31'] = [-1,-1,-1,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1997-01-31':'1997-12-31'] = [0,0,0,0,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1998-01-31':'1998-12-31'] = [1,1,1,1,1,0,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1999-01-31':'1999-12-31'] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2000-01-31':'2000-12-31'] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2001-01-31':'2001-12-31'] = [-1,-1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2002-01-31':'2002-12-31'] = [0,0,0,0,0,1,1,1,1,1,1,1]
ENSO_FASE['rango']['2003-01-31':'2003-12-31'] = [1,1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2004-01-31':'2004-12-31'] = [0,0,0,0,0,0,1,1,1,1,1,1]
ENSO_FASE['rango']['2005-01-31':'2005-12-31'] = [1,1,1,1,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2006-01-31':'2006-12-31'] = [0,0,0,0,0,0,0,0,1,1,1,1]
ENSO_FASE['rango']['2007-01-31':'2007-12-31'] = [1,0,0,0,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2008-01-31':'2008-12-31'] = [-1,-1,-1,-1,-1,-1,0,0,0,0,0,0]
ENSO_FASE['rango']['2009-01-31':'2009-12-31'] = [0,0,0,0,0,0,1,1,1,1,1,1]
ENSO_FASE['rango']['2010-01-31':'2010-12-31'] = [1,1,1,1,0,0,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2011-01-31':'2011-12-31'] = [-1,-1,-1,-1,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2012-01-31':'2012-12-31'] = [-1,-1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2013-01-31':'2013-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2014-01-31':'2014-12-31'] = [0,0,0,0,0,0,0,0,0,0,1,1]
ENSO_FASE['rango']['2015-01-31':'2015-12-31'] = [1,1,1,1,1,1,1,1,1,1,1,1]

ENSO_PP = criterio_ENSO(EVN_PP, FECHAS, ENSO_FASE, spd_PP)



#### PN ######==============================================================================
'''enso fase según SOI index 1 = cálido, -1 = frío, 0 = neutro'''
#==============================================================================

ENSO_FASE = pd.DataFrame(index = fechas, columns=['rango'])

ENSO_FASE['rango']['1979-01-31':'1979-12-31'] = [0,0,0,0,0,0,0,0,0,1,1,1]
ENSO_FASE['rango']['1980-01-31':'1980-12-31'] = [1,1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1981-01-31':'1981-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1982-01-31':'1982-12-31'] = [0,0,0,1,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1983-01-31':'1983-12-31'] = [1,1,1,1,1,1,0,0,0,0,0,0]
ENSO_FASE['rango']['1984-01-31':'1984-12-31'] = [0,0,0,0,0,0,0,0,0,-1,-1,-1]
ENSO_FASE['rango']['1985-01-31':'1985-12-31'] = [-1,-1,-1,-1,-1,-1,0,0,0,0,0,0]
ENSO_FASE['rango']['1986-01-31':'1986-12-31'] = [0,0,0,0,0,0,0,0,1,1,1,1]
ENSO_FASE['rango']['1987-01-31':'1987-12-31'] = [1,1,1,1,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1988-01-31':'1988-12-31'] = [1,1,0,0,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1989-01-31':'1989-12-31'] = [-1,-1,-1,-1,-1,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1990-01-31':'1990-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1991-01-31':'1991-12-31'] = [0,0,0,0,0,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1992-01-31':'1992-12-31'] = [1,1,1,1,1,1,1,0,0,0,0,0]
ENSO_FASE['rango']['1993-01-31':'1993-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1994-01-31':'1994-12-31'] = [0,0,0,0,0,0,0,0,0,1,1,1]
ENSO_FASE['rango']['1995-01-31':'1995-12-31'] = [1,1,1,0,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1996-01-31':'1996-12-31'] = [-1,-1,-1,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['1997-01-31':'1997-12-31'] = [0,0,0,0,1,1,1,1,1,1,1,1]
ENSO_FASE['rango']['1998-01-31':'1998-12-31'] = [1,1,1,1,1,0,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['1999-01-31':'1999-12-31'] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2000-01-31':'2000-12-31'] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2001-01-31':'2001-12-31'] = [-1,-1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2002-01-31':'2002-12-31'] = [0,0,0,0,0,1,1,1,1,1,1,1]
ENSO_FASE['rango']['2003-01-31':'2003-12-31'] = [1,1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2004-01-31':'2004-12-31'] = [0,0,0,0,0,0,1,1,1,1,1,1]
ENSO_FASE['rango']['2005-01-31':'2005-12-31'] = [1,1,1,1,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2006-01-31':'2006-12-31'] = [0,0,0,0,0,0,0,0,1,1,1,1]
ENSO_FASE['rango']['2007-01-31':'2007-12-31'] = [1,0,0,0,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2008-01-31':'2008-12-31'] = [-1,-1,-1,-1,-1,-1,0,0,0,0,0,0]
ENSO_FASE['rango']['2009-01-31':'2009-12-31'] = [0,0,0,0,0,0,1,1,1,1,1,1]
ENSO_FASE['rango']['2010-01-31':'2010-12-31'] = [1,1,1,1,0,0,-1,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2011-01-31':'2011-12-31'] = [-1,-1,-1,-1,0,0,0,-1,-1,-1,-1,-1]
ENSO_FASE['rango']['2012-01-31':'2012-12-31'] = [-1,-1,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2013-01-31':'2013-12-31'] = [0,0,0,0,0,0,0,0,0,0,0,0]
ENSO_FASE['rango']['2014-01-31':'2014-12-31'] = [0,0,0,0,0,0,0,0,0,0,1,1]
ENSO_FASE['rango']['2015-01-31':'2015-12-31'] = [1,1,1,1,1,1,1,1,1,1,1,1]

ENSO_PN = criterio_ENSO(EVN_PN, FECHAS, ENSO_FASE, spd_PN)

###### Calculando medias
ENSO_TT['media'] = ENSO_TT['suma']/ENSO_TT['contador']
ENSO_PP['media'] = ENSO_PP['suma']/ENSO_PP['contador']
ENSO_PN['media'] = ENSO_PN['suma']/ENSO_PN['contador']

#==============================================================================
"CICLO ANUAL DE EVENTOS Y MAGNITUD, TT"
#==============================================================================

El_Nino_evns_TT = ENSO_TT.contador[(ENSO_TT.rango == 1)]
La_Nina_evns_TT = ENSO_TT.contador[(ENSO_TT.rango == -1)]
Neutro_evns_TT = ENSO_TT.contador[(ENSO_TT.rango == 0)]

El_Nino_media_TT = ENSO_TT.media[(ENSO_TT.rango == 1)]
La_Nina_media_TT = ENSO_TT.media[(ENSO_TT.rango == -1)]
Neutro_media_TT  = ENSO_TT.media[(ENSO_TT.rango == 0)]

###### CICLOS
NINA_evns_TT = np.zeros(12)
NINO_evns_TT = np.zeros(12)
NEUTRO_evns_TT = np.zeros(12)

NINA_media_TT = np.zeros(12)
NINO_media_TT = np.zeros(12)
NEUTRO_media_TT = np.zeros(12)

for i in range(12):
    NINA_evns_TT[i]   = np.mean(La_Nina_evns_TT[(La_Nina_evns_TT.index.month == i+1)])
    NINO_evns_TT[i]   = np.mean(El_Nino_evns_TT[(El_Nino_evns_TT.index.month == i+1)])
    NEUTRO_evns_TT[i] = np.mean(Neutro_evns_TT [(Neutro_evns_TT.index.month == i+1)])
    
    NINA_media_TT[i]   = np.mean(La_Nina_media_TT[(La_Nina_media_TT.index.month == i+1)])
    NINO_media_TT[i]   = np.mean(El_Nino_media_TT[(El_Nino_media_TT.index.month == i+1)])
    NEUTRO_media_TT[i] = np.mean(Neutro_media_TT [(Neutro_media_TT.index.month == i+1)])
#==============================================================================
"CICLO ANUAL DE EVENTOS Y MAGNITUD, PP"
#==============================================================================

El_Nino_evns_PP = ENSO_PP.contador[(ENSO_PP.rango == 1)]
La_Nina_evns_PP = ENSO_PP.contador[(ENSO_PP.rango == -1)]
Neutro_evns_PP = ENSO_PP.contador[(ENSO_PP.rango == 0)]

El_Nino_media_PP = ENSO_PP.media[(ENSO_PP.rango == 1)]
La_Nina_media_PP = ENSO_PP.media[(ENSO_PP.rango == -1)]
Neutro_media_PP = ENSO_PP.media[(ENSO_PP.rango == 0)]

###### CICLOS
NINA_evns_PP = np.zeros(12)
NINO_evns_PP = np.zeros(12)
NEUTRO_evns_PP = np.zeros(12)

NINA_media_PP = np.zeros(12)
NINO_media_PP = np.zeros(12)
NEUTRO_media_PP = np.zeros(12)

for i in range(12):
    NINA_evns_PP[i]   = np.mean(La_Nina_evns_PP[(La_Nina_evns_PP.index.month == i+1)])
    NINO_evns_PP[i]   = np.mean(El_Nino_evns_PP[(El_Nino_evns_PP.index.month == i+1)])
    NEUTRO_evns_PP[i] = np.mean(Neutro_evns_PP [(Neutro_evns_PP.index.month == i+1)])
    
    NINA_media_PP[i]   = np.mean(La_Nina_media_PP[(La_Nina_media_PP.index.month == i+1)])
    NINO_media_PP[i]   = np.mean(El_Nino_media_PP[(El_Nino_media_PP.index.month == i+1)])
    NEUTRO_media_PP[i] = np.mean(Neutro_media_PP [(Neutro_media_PP.index.month == i+1)])

#==============================================================================
"CICLO ANUAL DE EVENTOS Y MAGNITUD, PP"
#==============================================================================

El_Nino_evns_PN = ENSO_PN.contador[(ENSO_PN.rango == 1)]
La_Nina_evns_PN = ENSO_PN.contador[(ENSO_PN.rango == -1)]
Neutro_evns_PN = ENSO_PN.contador[(ENSO_PN.rango == 0)]

El_Nino_media_PN = ENSO_PN.media[(ENSO_PN.rango == 1)]
La_Nina_media_PN = ENSO_PN.media[(ENSO_PN.rango == -1)]
Neutro_media_PN = ENSO_PN.media[(ENSO_PN.rango == 0)]

###### CICLOS
NINA_evns_PN = np.zeros(12)
NINO_evns_PN = np.zeros(12)
NEUTRO_evns_PN = np.zeros(12)

NINA_media_PN = np.zeros(12)
NINO_media_PN = np.zeros(12)
NEUTRO_media_PN = np.zeros(12)

for i in range(12):
    NINA_evns_PN[i]   = np.mean(La_Nina_evns_PN[(La_Nina_evns_PN.index.month == i+1)])
    NINO_evns_PN[i]   = np.mean(El_Nino_evns_PN[(El_Nino_evns_PN.index.month == i+1)])
    NEUTRO_evns_PN[i] = np.mean(Neutro_evns_PN [(Neutro_evns_PN.index.month == i+1)])
    
    NINA_media_PN[i]   = np.mean(La_Nina_media_PN[(La_Nina_media_PN.index.month == i+1)])
    NINO_media_PN[i]   = np.mean(El_Nino_media_PN[(El_Nino_media_PN.index.month == i+1)])
    NEUTRO_media_PN[i] = np.mean(Neutro_media_PN [(Neutro_media_PN.index.month == i+1)])

#==============================================================================
"PLOT TT"
#==============================================================================
# Eventos
fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(12), NINA_evns_TT, marker='o', color='b', label='La Nina')
ax1.plot(np.arange(12), NINO_evns_TT, marker='v', color='r', label='El Nino')
ax1.plot(np.arange(12), NEUTRO_evns_TT, marker='s', color='k', label='Neutral')
my_xticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(range(12), my_xticks)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Events$', size='15')
ax1.legend(loc='best')
ax1.set_ylim(0, 5.5)
ax1.set_xlim(-1, 12)
ax1.set_title('$Events$ $(TT)$', size='15')
ax1.grid(True)
plt.show()

# Magnitud
fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(12), NINA_media_TT, marker='o', color='b', label='La Nina')
ax1.plot(np.arange(12), NINO_media_TT, marker='v', color='r', label='El Nino')
ax1.plot(np.arange(12), NEUTRO_media_TT, marker='s', color='k', label='Neutral')
my_xticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(range(12), my_xticks)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Speed (m/s)$', size='15')
ax1.legend(loc='best')
ax1.set_ylim(6.4, 10.5)
ax1.set_xlim(-1, 12)
ax1.set_title('$Magnitud$ $(TT)$', size='15')
ax1.grid(True)
plt.show()

#==============================================================================
"PLOT PP"
#==============================================================================
# Eventos
fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(12), NINA_evns_PP, marker='o', color='b', label='La Nina')
ax1.plot(np.arange(12), NINO_evns_PP, marker='v', color='r', label='El Nino')
ax1.plot(np.arange(12), NEUTRO_evns_PP, marker='s', color='k', label='Neutral')
my_xticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(range(12), my_xticks)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Events$', size='15')
ax1.legend(loc='best')
ax1.set_ylim(0, 5.5)
ax1.set_xlim(-1, 12)
ax1.set_title('$Events$ $(PP)$', size='15')
ax1.grid(True)
plt.show()

# Magnitud
fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(12), NINA_media_PP, marker='o', color='b', label='La Nina')
ax1.plot(np.arange(12), NINO_media_PP, marker='v', color='r', label='El Nino')
ax1.plot(np.arange(12), NEUTRO_media_PP, marker='s', color='k', label='Neutral')
my_xticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(range(12), my_xticks)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Speed (m/s)$', size='15')
ax1.legend(loc='best')
ax1.set_ylim(6.4, 10.5)
ax1.set_xlim(-1, 12)
ax1.set_title('$Magnitud$ $(PP)$', size='15')
ax1.grid(True)
plt.show()

#==============================================================================
"PLOT PN"
#==============================================================================
# Eventos
fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(12), NINA_evns_PN, marker='o', color='b', label='La Nina')
ax1.plot(np.arange(12), NINO_evns_PN, marker='v', color='r', label='El Nino')
ax1.plot(np.arange(12), NEUTRO_evns_PN, marker='s', color='k', label='Neutral')
my_xticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(range(12), my_xticks)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Events$', size='15')
ax1.legend(loc='best')
ax1.set_ylim(0, 5.5)
ax1.set_xlim(-1, 12)
ax1.set_title('$Events$ $(PN)$', size='15')
ax1.grid(True)
plt.show()

# Magnitud
fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(12), NINA_media_PN, marker='o', color='b', label='La Nina')
ax1.plot(np.arange(12), NINO_media_PN, marker='v', color='r', label='El Nino')
ax1.plot(np.arange(12), NEUTRO_media_PN, marker='s', color='k', label='Neutral')
my_xticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(range(12), my_xticks)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Speed (m/s)$', size='15')
ax1.legend(loc='best')
ax1.set_ylim(6.4, 10.5)
ax1.set_xlim(-1, 12)
ax1.set_title('$Magnitud$ $(PN)$', size='15')
ax1.grid(True)
plt.show()