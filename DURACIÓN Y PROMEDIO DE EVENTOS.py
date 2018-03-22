from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

wnd_tehuantepec = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/tehuantepec_wind_data.txt', delimiter=',')
wnd_papagayo = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/papagayo_wind_data.txt', delimiter=',')
wnd_panama = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/panama_wind_data.txt', delimiter=',')               

fechas = pd.date_range('1998/01/01', periods=len(wnd_tehuantepec), freq='6H')

evn_TT = []
i = 0
a = 8
b = np.zeros(a)
while i < (len(wnd_tehuantepec)-a): # Se va a recorrer el vector para ver qué eventos cumplen el criterio de los seis días y el del promedio   
    if np.all(wnd_tehuantepec[i:i+a] != b) == True: # Primero se verifica que almenos hayan seis días seguidos de alta velocidad en los vientos
        j = i+a-1
        if j < (len(wnd_tehuantepec)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector wnd_tehuantepec, la siguiente línea arrojará un error
            while wnd_tehuantepec[j+1] != 0: # Si la condición de los 6 días sucede, se debe primero saber hasta qué posición se sigue el evento sin interrupción
                j = j+1
                if j == (len(wnd_tehuantepec)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de wnd_tehuantepec, ya que de lo contrario, la primera línea del bucle arrojaría error
                    break
        med_TT = np.mean(wnd_tehuantepec[i:j+1]) # Como se sabe la posición hasta donde llega el evento, se procede a calcular el promedio de velocidad en dicho evento
        if med_TT > 18: # Dado que se se tiene ya el promedio, se verifica que este cumpla la condición de que supere un umbral
            evn_TT.append((i,j)) # Dado que se cumple la condición del promedio umbral, se guardan las posiciones final e inicial del evento
        i = j+1 # ésta será la posicón donde empezará de nuevo el bucle, ya que entre 'i' e 'j' (incluídos) se sabe que hay un evento
    else:
        i = i+1




evn_PP = []
i = 0
a = 8
b = np.zeros(a)
while i < (len(wnd_papagayo)-a): # Se va a recorrer el vector para ver qué eventos cumplen el criterio de los seis días y el del promedio   
    if np.all(wnd_papagayo[i:i+a] != b) == True: # Primero se verifica que almenos hayan seis días seguidos de alta velocidad en los vientos
        j = i+a-1
        if j < (len(wnd_papagayo)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector wnd_tehuantepec, la siguiente línea arrojará un error
            while wnd_papagayo[j+1] != 0: # Si la condición de los 6 días sucede, se debe primero saber hasta qué posición se sigue el evento sin interrupción
                j = j+1
                if j == (len(wnd_papagayo)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de wnd_tehuantepec, ya que de lo contrario, la primera línea del bucle arrojaría error
                    break
        med_PP = np.mean(wnd_papagayo[i:j+1]) # Como se sabe la posición hasta donde llega el evento, se procede a calcular el promedio de velocidad en dicho evento
        if med_PP > 12.2: # Dado que se se tiene ya el promedio, se verifica que este cumpla la condición de que supere un umbral
            evn_PP.append((i,j)) # Dado que se cumple la condición del promedio umbral, se guardan las posiciones final e inicial del evento
        i = j+1 # ésta será la posicón donde empezará de nuevo el bucle, ya que entre 'i' e 'j' (incluídos) se sabe que hay un evento
    else:
        i = i+1
        
        
        
        
evn_PN = []
i = 0
a = 8
b = np.zeros(a)
while i < (len(wnd_panama)-a): # Se va a recorrer el vector para ver qué eventos cumplen el criterio de los seis días y el del promedio   
    if np.all(wnd_panama[i:i+a] != b) == True: # Primero se verifica que almenos hayan seis días seguidos de alta velocidad en los vientos
        j = i+a-1
        if j < (len(wnd_panama)-1): # éste condicional se hace ya que en el caso de que j sea una unidad menor a la longitud del vector wnd_tehuantepec, la siguiente línea arrojará un error
            while wnd_panama[j+1] != 0: # Si la condición de los 6 días sucede, se debe primero saber hasta qué posición se sigue el evento sin interrupción
                j = j+1
                if j == (len(wnd_panama)-1): # Se debe parar en el momento en que j alcance una unidad menos a la longitud de wnd_tehuantepec, ya que de lo contrario, la primera línea del bucle arrojaría error
                    break
        med_PN = np.mean(wnd_panama[i:j+1]) # Como se sabe la posición hasta donde llega el evento, se procede a calcular el promedio de velocidad en dicho evento
        if med_PN > 10.4: # Dado que se se tiene ya el promedio, se verifica que este cumpla la condición de que supere un umbral
            evn_PN.append((i,j)) # Dado que se cumple la condición del promedio umbral, se guardan las posiciones final e inicial del evento
        i = j+1 # ésta será la posicón donde empezará de nuevo el bucle, ya que entre 'i' e 'j' (incluídos) se sabe que hay un evento
    else:
        i = i+1