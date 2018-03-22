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

#Variables = [v for v in ArchivoU.variables]
#print Variables

LON = ArchivoV.variables['LON'][:]-360
LAT = ArchivoV.variables['LAT'][:]

posiciones = ['TT','PP','PN']
lon_max = [-96.25, -90.5, -80.75]
lat_max = [16, 11.75, 8.5]
lon_min = [-93.75, -86, -78.75]
lat_min = [12.5, 8.75, 5.5]

datep = pd.date_range('1979-01-01 00:00:00', '2015-12-31 23:00:00', freq='3H')
date = pd.DatetimeIndex(datep)
Serie = pd.DataFrame(index=date, columns=['TT','PP', 'PN']) 

for i, j, k, m, n in zip(lat_max, lat_min, lon_max, lon_min, posiciones):
    for l in range(1979, 2016): # De 0 a 37, porque sólo se va a hacer hasta el 2015
        U = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/ZONAL-REPROYECCION/'+str(l)+'alt.nc')
        V = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/MERIDIONAL-REPROYECCION/'+str(l)+'alt.nc')
        max_lat = np.where(LAT == i)[0][0]
        min_lat = np.where(LAT == j)[0][0]
        max_lon = np.where(LON == k)[0][0]
        min_lon = np.where(LON == m)[0][0]
        
        comp_u = np.zeros(len(U.variables['U']))
        comp_v = np.zeros(len(V.variables['V']))
        
        for x in range(len(comp_u)):
            comp_u[x] = np.mean(U.variables['U'][x, min_lat : max_lat+1, max_lon : min_lon+1])
            comp_v[x] = np.mean(U.variables['U'][x, min_lat : max_lat+1, max_lon : min_lon+1])
        
        spd = np.sqrt(comp_u*comp_u+comp_v*comp_v)
        Serie[n][str(l)+'-01-01 00:00:00':str(l)+'-12-31 23:00:00'] = spd
        
MA = Serie.as_matrix(columns=None)
spd_TT = MA[:,0]
spd_PP = MA[:,1]
spd_PN = MA[:,2]

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

#==============================================================================
"DEFINICIÓN FUNCIÓN PARA ENCONTRAR ÍNDICES EN LOS QUE HAY EVENTOS"
#==============================================================================

def indices_eventos(Ser_TT):
    
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
                    
                    if j < (len(Ser_TT)-9): # Esta línea es debida a la siguiente, para que no se genere un error
                        if np.any(Ser_TT[j+1:j+9] != np.zeros(8)) == True: # Se debe revisar que las siguientes ocho posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+9): # para hallar en qué posición de las ocho que se juzgan se encuentra la posición con valor distinto de cero 
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while NO se vuelva a repetir
                        else:
                            l = 5 # Para que el while NO se vuelva a repetir
    
                    elif j < (len(Ser_TT)-8): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-9
                        if np.any(Ser_TT[j+1:j+8] != np.zeros(7)) == True: # Se debe revisar que las siguientes siete posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+8):  # para hallar en qué posición de las siete que se juzgan se encuentra la posición con valor distinto de cero
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while NO se vuelva a repetir
                        else:
                            l = 5 # Para que el while NO se vuelva a repetir               
                    
                    elif j < (len(Ser_TT)-7): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-8
                        if np.any(Ser_TT[j+1:j+7] != np.zeros(6)) == True:  # Se debe revisar que las siguientes seis posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+7): # para hallar en qué posición de las seis que se juzgan se encuentra la posición con valor distinto de cero
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while NO se vuelva a repetir
                        else:
                            l = 5 # Para que el while NO se vuelva a repetir
                    
                    elif j < (len(Ser_TT)-6):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-7
                        if np.any(Ser_TT[j+1:j+6] != np.zeros(5)) == True:  # Se debe revisar que las siguientes cinco posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+6):  # para hallar en qué posición de las cinco que se juzgan se encuentra la posición con valor distinto de cero
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while NO se vuelva a repetir
                        else:
                            l = 5 # Para que el while NO se vuelva a repetir
                            
                    elif j < (len(Ser_TT)-5):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-6
                        if np.any(Ser_TT[j+1:j+5] != np.zeros(4)) == True:  # Se debe revisar que las siguientes cuatro posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+5):  # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while NO se vuelva a repetir
                        else:
                            l = 5 # Para que el while NO se vuelva a repetir
    
                    elif j < (len(Ser_TT)-4):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-5
                        if np.any(Ser_TT[j+1:j+4] != np.zeros(3)) == True:  # Se debe revisar que las siguientes tres posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+4):  # para hallar en qué posición de las tres que se juzgan se encuentra la posición con valor distinto de cero
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while NO se vuelva a repetir
                        else:
                            l = 5 # Para que el while NO se vuelva a repetir
    
                    elif j < (len(Ser_TT)-3):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-4
                        if np.any(Ser_TT[j+1:j+3] != np.zeros(2)) == True:  # Se debe revisar que las siguientes dos posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+3):  # para hallar en qué posición de las dos que se juzgan se encuentra la posición con valor distinto de cero
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while NO se vuelva a repetir
                        else:
                            l = 5 # Para que el while NO se vuelva a repetir
    
                    elif j < (len(Ser_TT)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-3
                        if np.any(Ser_TT[j+1:j+2] != 0) == True:  # Se debe revisar que la siguiente posicion a la posición j no tenga un valor, ya que de lo contrario, ese valor hará parte del evento al que pertenece el valor de la posición j
                            for k in range(j+1, j+2):
                                if Ser_TT[k] != 0:
                                    l = 2 # Para que el while se vuelva a repetir
                                    j = k
                                    break
                                else:
                                    l = 5 # Para que el while NO se vuelva a repetir
                        else:
                            l = 5 # Para que el while NO se vuelva a repetir
    
                    else:
                        l = 5 # Para que el while NO se vuelva a repetir
                else:
                    l = 5 # Para que el while NO se vuelva a repetir
            evn_TT.append((i,j))       
            i = j+8 # ésta sería la nueva posición donde comienza todo el bucle     
        else:
            i = i+1 # Siguiente posicion a examinar
    EVN_TT = np.array((evn_TT))
    return EVN_TT

EVN_TT = indices_eventos(Ser_TT)
EVN_PP = indices_eventos(Ser_PP)
EVN_PN = indices_eventos(Ser_PN)

#==============================================================================
"SCATTER DERIVADA"
#==============================================================================

def derived(serie, index, path, chorro):
    ano_max = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    ano_min = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    
    lim_sup = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    lim_inf = 1 # éste es un npumero cualquiera que está dentro de los límites físicos de las anomalías
    
    for q in range(len(index[:])):
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


#==============================================================================
"DERIVADAS"
#==============================================================================

def plot_derivadas(spd_TT, EVN_TT, path, chorro):
    for m in range(16):
        fig = plt.figure(figsize=(8,6))
        ax1 = fig.add_subplot(111)
        for i in range(len(EVN_TT[:])):
            if EVN_TT[i,0] != EVN_TT[i,1]:
                c = EVN_TT[i,0]+np.where(spd_TT[EVN_TT[i,0]:EVN_TT[i,1]+1] == np.max(spd_TT[EVN_TT[i,0]:EVN_TT[i,1]+1]))
                cc = c[0,0]
                if cc <= len(spd_TT)-13:        
                    if m <= spd_TT[cc-12] < m+1:
                        der = np.zeros(len(spd_TT[cc-12:cc+13]))                
                        for j in range(len(der)):
                            der[j] = spd_TT[cc-12+j+1]-spd_TT[cc-12+j]
                        ax1.plot(range(len(der)), der, linewidth=0.7, color='k', alpha = 0.7)
            else:
                if EVN_TT[i,1] <= len(spd_TT)-13:        
                    if m <= spd_TT[EVN_TT[i,1]-12]< m+1:
                        der = np.zeros(len(spd_TT[cc-12:cc+13]))
                        for j in range(len(der)):
                            der[j] = spd_TT[EVN_TT[i,1]-12+j+1]-spd_TT[EVN_TT[i,1]-12+j] 
                        ax1.plot(range(len(der)), der, linewidth=0.7, color='k', alpha = 0.7)
        my_xticks = ['-36','-33','-30','-27','-24','-21','-18','-15','-12','-09','-06','-03','00','03','06','09','12','15','18','21','24','27','30','33','36']
        plt.xticks(range(len(der)),my_xticks)
        ax1.grid(True)
        ax1.set_xlabel('$Time$ $(h)$', size='15')
        ax1.set_ylabel('$\Delta$ $Speed$ $(m/s)$', size='15')
        ax1.set_title('Derived from Wind Speed, '+str(float(m))+' - '+str(float(m+1))+' ('+chorro+')', size='14')
        ax1.legend(loc='best')
        ax1.set_ylim(-5, 7)
        plt.savefig(path+'/'+str(m)+'-'+str(m+1)+'.png',dpi=100,bbox_inches='tight')
    
plot_derivadas(spd_PN, EVN_PN, '/home/yordan/Escritorio/DERIVADAS_NARR/PN', 'PN')    
 
 
 
 
 
 