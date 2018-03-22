# -*- coding: utf-8 -*-

import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pylab import hist, show
import pylab as pl
from numpy import genfromtxt
import pickle


###################### 
"COMPOSITE TT, PP, PN"
######################

r = open('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/SERIES COMPOSITES TT, PP, PN/NARR_TT.bin', 'rb')
spd_TT = pickle.load(r)

rr = open('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/SERIES COMPOSITES TT, PP, PN/NARR_PP.bin', 'rb')
spd_PP = pickle.load(rr)

rrr = open('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/NARR/VIENTOS-NARR/SERIES COMPOSITES TT, PP, PN/NARR_PN.bin', 'rb')
spd_PN = pickle.load(rrr)

##################################################################
"IDENTIFICACIÓN DE FECHAS QUE SUPERAN UMBRAL TT-7, PP-6.5, PN-6.5"
##################################################################

serie = spd_TT # spd_TT, spd_PN, spd_TT
Ser = np.zeros(len(serie))

for i in range(len(serie)):
    if serie[i] > 7: # PP-6.5, PN-6.5, TT-7 
        Ser[i] = serie[i]

#############################################################################
"NÚMERO  DE EVENTOS DE CADA MES EN EL VECTOR ser (BASE DE DATOS NARR)"
#############################################################################


fechas1 = pd.date_range('1998/01/01 00:00:00', '2009/12/31 21:00:00', freq='3H')
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')

cont = np.zeros(144)
begin = pd.date_range('1979/01/01 00:00:00', '1997/12/31 21:00:00', freq='3H')
end = pd.date_range('1979/01/01 00:00:00', '2009/12/31 21:00:00', freq='3H')
ser = Ser[len(begin):len(end)] # Corresponde al período entre 1998 y 2009
i = 0

while i<(len(ser)-1):
    if ser[i] != 0: # Primero se verifica que la posición i tenga un valor
        j = i
        l = 3 # Esto es para poder entrar al while
        while l <= 4:        
            if j < (len(ser)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector ser, la siguiente línea arrojará un error
                while ser[j+1] != 0: # Se hace éste while para saber hasta qué posición llega el evento 
                    j = j+1
                    if j == (len(ser)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de ser, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                        break

                if j < (len(ser)-9): # Esta línea es debida a la siguiente, para que no se genere un error
                    if np.any(ser[j+1:j+9] != np.zeros(8)) == True: # Se debe revisar que las siguientes ocho posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                        for k in range(j+1, j+9): # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero 
                            if ser[k] != 0:
                                l = 2 # Para que el while se vuelva a repetir
                                j = k
                                break
                            else:
                                l = 5 # Para que el while no se vuelva a repetir
                    else:
                        l = 5 # Para que el while no se vuelva a repetir               
    
                elif j < (len(ser)-8): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-9
                    if np.any(ser[j+1:j+8] != np.zeros(7)) == True: 
                        for k in range(j+1, j+8):  
                            if ser[k] != 0:
                                l = 2 
                                j = k
                                break
                            else:
                                l = 5 
                    else:
                        l = 5 
                
                elif j < (len(ser)-7): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-8
                    if np.any(ser[j+1:j+7] != np.zeros(6)) == True: 
                        for k in range(j+1, j+7):
                            if ser[k] != 0:
                                l = 2 
                                j = k
                                break
                            else:
                                l = 5 
                    else:
                        l = 5 

                elif j < (len(ser)-6): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-7
                    if np.any(ser[j+1:j+6] != np.zeros(5)) == True: 
                        for k in range(j+1, j+6):  
                            if ser[k] != 0:
                                l = 2 
                                j = k
                                break
                            else:
                                l = 5 
                    else:
                        l = 5 
                                
                
                elif j < (len(ser)-5): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-6
                    if np.any(ser[j+1:j+5] != np.zeros(4)) == True: 
                        for k in range(j+1, j+5):                            
                            if ser[k] != 0:
                                l = 2 
                                j = k
                                break
                            else:
                                l = 5 
                    else:
                        l = 5 # Para que el while no se vuelva a repetir
                
                elif j < (len(ser)-4): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-5
                    if np.any(ser[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if ser[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5                        
                
                elif j < (len(ser)-3): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-4
                    if np.any(ser[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if ser[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                
                elif j < (len(ser)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(ser)-3
                    if np.any(ser[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if ser[k] != 0:
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
        for jj, kk in enumerate(meses1):
            if fechas1[i].month == kk.month and fechas1[i].year == kk.year: 
                cont[jj] = cont[jj]+1
        i = j+8 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar
cont4 = cont

#######################
"LECTURA DE DATOS RASI"
#######################

wnd_tehuantepec = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/tehuantepec_wind_data.txt', delimiter=',')
wnd_papagayo = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/papagayo_wind_data.txt', delimiter=',')
wnd_panama = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/panama_wind_data.txt', delimiter=',')               

##########################################
"NÚMERO DE EVENTOS DE CADA MES TT EN RASI"
##########################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
cont_TT = np.zeros(144)
i = 0
while i<(len(wnd_tehuantepec)-1):    
    if wnd_tehuantepec[i] != 0: # Primero se verifica que la posición i tenga un valor
        j = i
        l = 3
        while l <= 4:        
            if j < (len(wnd_tehuantepec)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector wnd_tehuantepec, la siguiente línea arrojará un error
                while wnd_tehuantepec[j+1] != 0: # Se hace éste while para saber hasta qué posición llega el evento 
                    j = j+1
                    if j == (len(wnd_tehuantepec)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de wnd_tehuantepec, ya que de lo contrario, cuando se evalúe la condición del bucle se tendría un error
                        break
                
                if j < (len(wnd_tehuantepec)-5): # Esta línea es debida a la siguiente, para que no se genere un error
                    if np.any(wnd_tehuantepec[j+1:j+5] != np.zeros(4)) == True: # Se debe revisar que las siguientes cuatro posiciones a la posición j no tengan un valor, ya que de lo contrario, esos valores harán parte del evento al que pertenece el valor de la posición j
                        for k in range(j+1, j+5): # para hallar en qué posición de las cuatro que se juzgan se encuentra la posición con valor distinto de cero 
                            if wnd_tehuantepec[k] != 0:
                                l = 2 # Para que el while se vuelva a repetir
                                j = k
                                break
                            else:
                                l = 5 # Para que el while no se vuelva a repetir
                    else:
                        l = 5 # Para que el while no se vuelva a repetir
                elif j < (len(wnd_tehuantepec)-4): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(wnd_tehuantepec)-5
                    if np.any(wnd_tehuantepec[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if wnd_tehuantepec[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5                        
                elif j < (len(wnd_tehuantepec)-3): # Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(wnd_tehuantepec)-4
                    if np.any(wnd_tehuantepec[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if wnd_tehuantepec[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(wnd_tehuantepec)-2):# Éste condicional tiene lugar cuando en la identificación de la posición j, ésta toma el valor de len(wnd_tehuantepec)-3
                    if np.any(wnd_tehuantepec[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if wnd_tehuantepec[k] != 0:
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
        for jj, kk in enumerate(meses1):
            if fechas1[i].month == kk.month and fechas1[i].year == kk.year: 
                cont_TT[jj] = cont_TT[jj]+1
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar

cont1 = cont_TT

##########################################
"NÚMERO DE EVENTOS DE CADA MES PP EN RASI"
##########################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
cont_PP = np.zeros(144)
i = 0
while i<(len(wnd_papagayo)-1):    
    if wnd_papagayo[i] != 0: # Primero se verifica que almenos hayan seis días seguidos de alta velocidad en los vientos
        j = i
        l = 3
        while l <= 4:        
            if j < (len(wnd_papagayo)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector wnd_tehuantepec, la siguiente línea arrojará un error
                while wnd_papagayo[j+1] != 0: # Si la condición de los 6 días sucede, se debe primero saber hasta qué posición se sigue el evento sin interrupción
                    j = j+1
                    if j == (len(wnd_papagayo)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de wnd_tehuantepec, ya que de lo contrario, la primera línea del bucle arrojaría error
                        break
                
                if j < (len(wnd_papagayo)-5):
                    if np.any(wnd_papagayo[j+1:j+5] != np.zeros(4)) == True:
                        for k in range(j+1, j+5):
                            if wnd_papagayo[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(wnd_papagayo)-4):
                    if np.any(wnd_papagayo[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if wnd_papagayo[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5                        
                elif j < (len(wnd_papagayo)-3):
                    if np.any(wnd_papagayo[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if wnd_papagayo[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(wnd_papagayo)-2):
                    if np.any(wnd_papagayo[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if wnd_papagayo[k] != 0:
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
        for jj, kk in enumerate(meses1):
            if fechas1[i].month == kk.month and fechas1[i].year == kk.year: 
                cont_PP[jj] = cont_PP[jj]+1
        i = j+4        
    else:
        i = i+1

cont2 = cont_PP

##########################################
"NÚMERO DE EVENTOS DE CADA MES PN EN RASI"
##########################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
cont_PN = np.zeros(144)
i = 0
while i<(len(wnd_panama)-1):    
    if wnd_panama[i] != 0: # Primero se verifica que almenos hayan seis días seguidos de alta velocidad en los vientos
        j = i
        l = 3
        while l <= 4:        
            if j < (len(wnd_panama)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector wnd_tehuantepec, la siguiente línea arrojará un error
                while wnd_panama[j+1] != 0: # Si la condición de los 6 días sucede, se debe primero saber hasta qué posición se sigue el evento sin interrupción
                    j = j+1
                    if j == (len(wnd_panama)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de wnd_tehuantepec, ya que de lo contrario, la primera línea del bucle arrojaría error
                        break
                
                if j < (len(wnd_panama)-5):
                    if np.any(wnd_panama[j+1:j+5] != np.zeros(4)) == True:
                        for k in range(j+1, j+5):
                            if wnd_panama[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(wnd_panama)-4):
                    if np.any(wnd_panama[j+1:j+4] != np.zeros(3)) == True:
                        for k in range(j+1, j+4):
                            if wnd_panama[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5       
                elif j < (len(wnd_panama)-3):
                    if np.any(wnd_panama[j+1:j+3] != np.zeros(2)) == True:
                        for k in range(j+1, j+3):
                            if wnd_panama[k] != 0:
                                l = 2
                                j = k
                                break
                            else:
                                l = 5
                    else:
                        l = 5
                elif j < (len(wnd_panama)-2):
                    if np.any(wnd_panama[j+1:j+2] != 0) == True:
                        for k in range(j+1, j+2):
                            if wnd_panama[k] != 0:
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
        for jj, kk in enumerate(meses1):
            if fechas1[i].month == kk.month and fechas1[i].year == kk.year: 
                cont_PN[jj] = cont_PN[jj]+1
        i = j+4
    else:
        i = i+1

cont3 = cont_PN

##########################
"PLOT EVENTOS DE CADA MES"
##########################

fig = plt.figure(figsize=(15,4.8))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(0,144), cont3, marker='o', color='#8904B1', label='RASI Events')
ax1.plot(np.arange(0,144), cont4, marker='D', color='#FF4000', label='NARR Events')
my_xticks = ['Jan/98','Jul','Jan/99','Jul','Jan/00','Jul','Jan/01','Jul','Jan/02','Jul','Jan/03','Jul','Jan/04','Jul','Jan/05','Jul','Jan/06','Jul','Jan/07','Jul','Jan/08','Jul','Jan/09','Jul']
plt.xticks(np.arange(0,144,6), my_xticks, rotation=90)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Events$', size='15')
ax1.legend(loc='best')
ax1.set_ylim(cont4.min()-0.5, cont4.max()+0.5)
ax1.set_xlim(0, 145)
ax1.set_title('$RASI$ $and$ $NARR$ $events$ $(PN)$', size='15')
ax1.grid(True)