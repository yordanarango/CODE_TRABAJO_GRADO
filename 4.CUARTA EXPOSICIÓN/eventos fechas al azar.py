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

#########################
"VELOCIDAD EN CADA PIXEL"
#########################

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
        selec = [] # Cada horario de cada mes, se debe volver a crear la lista, que es donde se guardarán los datos de horario de cada mes
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
    
##############################
"ÍNDICES DE FECHAS ALEATORIAS"
##############################

EVN_TT = np.random.randint(0, len(serie_TT), 100)
EVN_PP = np.random.randint(0, len(serie_TT), 100)
EVN_PN = np.random.randint(0, len(serie_TT), 100)

#########
"PLOT TT"
#########

fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
for i in range(len(EVN_TT)):
    c = EVN_TT[i]-30+np.where(ano_TT[EVN_TT[i]-30:EVN_TT[i]+31] == np.max(ano_TT[EVN_TT[i]-30:EVN_TT[i]+31]))
    cc = c[0,0]
    if cc <= len(ano_TT)-7:
            if 11 <= ano_TT[cc] < 12:       
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12), ano_TT[cc-6:cc+7], linewidth=0.7, color='r', alpha = 0.4)
my_xticks = ['-36:00','-30:00','-24:00', '-18:00', '-12:00', '-06:00', '00:00', '06:00', '12:00', '18:00', '24:00', '30:00', '36:00']
plt.xticks((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12),my_xticks)
ax1.grid(True)
ax1.set_xlabel('$Time$ $(h)$', size='15')
ax1.set_ylabel('$Speed$ $(m/s)$', size='15')
ax1.set_title('$SPEED$ $ANOMALIES$ $(TT,$ $11.0-12.0)$', size='14')
ax1.legend(loc='best')
ax1.set_ylim(-6, 13)

#########
"PLOT PP"
#########

fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
for i in range(len(EVN_PP)):
    c = EVN_PP[i]-30+np.where(ano_PP[EVN_PP[i]-30:EVN_PP[i]+31] == np.max(ano_PP[EVN_PP[i]-30:EVN_PP[i]+31]))
    cc = c[0,0]
    if cc <= len(ano_PP)-7:
            if 8 <= ano_PP[cc] < 9:       
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12), ano_PP[cc-6:cc+7], linewidth=0.7, color='#07834c', alpha = 0.6)
my_xticks = ['-36:00','-30:00','-24:00', '-18:00', '-12:00', '-06:00', '00:00', '06:00', '12:00', '18:00', '24:00', '30:00', '36:00']
plt.xticks((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12),my_xticks)
ax1.grid(True)
ax1.set_xlabel('$Time$ $(h)$', size='15')
ax1.set_ylabel('$Speed$ $(m/s)$', size='15')
ax1.set_title('$SPEED$ $ANOMALIES$ $(PP,$ $8.0-9.0)$', size='14')
ax1.legend(loc='best')
ax1.set_ylim(-4, 9)

#########
"PLOT PN"
#########

fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
for i in range(len(EVN_PN)):
    c = EVN_PN[i]-30+np.where(ano_PN[EVN_PN[i]-30:EVN_PN[i]+31] == np.max(ano_PN[EVN_PN[i]-30:EVN_PN[i]+31]))
    cc = c[0,0]
    if cc <= len(ano_PN)-7:
            if 6 <= ano_PN[cc] < 7:       
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12), ano_PN[cc-6:cc+7], linewidth=0.7, color='#064c6a', alpha = 0.5)
my_xticks = ['-36:00','-30:00','-24:00', '-18:00', '-12:00', '-06:00', '00:00', '06:00', '12:00', '18:00', '24:00', '30:00', '36:00']
plt.xticks((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12),my_xticks)
ax1.grid(True)
ax1.set_xlabel('$Time$ $(h)$', size='15')
ax1.set_ylabel('$Speed$ $(m/s)$', size='15')
ax1.set_title('$SPEED$ $ANOMALIES$ $(PN,$ $6.0-7.0)$', size='14')
ax1.legend(loc='best')
ax1.set_ylim(-4, 8)








##################
"PLOT TT COMIENZO"
##################

fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
for i in range(len(EVN_TT[:,0])):
    if EVN_TT[i,0] != EVN_TT[i,1]:
        c = EVN_TT[i,0]+np.where(ano_TT[EVN_TT[i,0]:EVN_TT[i,1]+1] == np.max(ano_TT[EVN_TT[i,0]:EVN_TT[i,1]+1]))
        cc = c[0,0]
        if cc <= len(ano_TT)-7:        
            if 11 <= ano_TT[cc-6] < 12:       
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12) ,ano_TT[cc-6:cc+7], linewidth=0.7, color='#9437f1', alpha = 0.4)
    else:
        if EVN_TT[i,1] <= len(ano_TT)-7:        
            if 11 <= ano_TT[EVN_TT[i,1]-6]< 12:
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12), ano_TT[EVN_TT[i,1]-6:EVN_TT[i,1]+7], linewidth=0.7, color='#9437f1', alpha = 0.4)
my_xticks = ['-36:00','-30:00','-24:00', '-18:00', '-12:00', '-06:00', '00:00', '06:00', '12:00', '18:00', '24:00', '30:00', '36:00']
plt.xticks((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12),my_xticks)
ax1.grid(True)
ax1.set_xlabel('$Time$ $(h)$', size='15')
ax1.set_ylabel('$Speed$ $(m/s)$', size='15')
ax1.set_title('$SPEED$ $ANOMALIES$ $(TT,$ $9.0,$ $10.0)$', size='14')
ax1.legend(loc='best')
ax1.set_ylim(-6, 16)

##################
"PLOT PP COMIENZO"
##################

fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
for i in range(len(EVN_PP[:,0])):
    if EVN_PP[i,0] != EVN_PP[i,1]:
        c = EVN_PP[i,0]+np.where(ano_PP[EVN_PP[i,0]:EVN_PP[i,1]+1] == np.max(ano_PP[EVN_PP[i,0]:EVN_PP[i,1]+1]))
        cc = c[0,0]
        if cc <= len(ano_PP)-7:        
            if 8 <= ano_PP[cc-6] < 9:       
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12), ano_PP[cc-6:cc+7], linewidth=0.7, color='#ba4a00', alpha = 0.5)
    else:
        if EVN_PP[i,1] <= len(ano_PP)-7:        
            if 8 <= ano_PP[EVN_PP[i,1]-6]< 9:
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12), ano_PP[EVN_PP[i,1]-6:EVN_PP[i,1]+7], linewidth=0.7, color='#ba4a00', alpha = 0.5)
my_xticks = ['-36:00','-30:00','-24:00', '-18:00', '-12:00', '-06:00', '00:00', '06:00', '12:00', '18:00', '24:00', '30:00', '36:00']
plt.xticks((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), my_xticks)
ax1.grid(True)
ax1.set_xlabel('$Time$ $(h)$', size='15')
ax1.set_ylabel('$Speed$ $(m/s)$', size='15')
ax1.set_title('$SPEED$ $ANOMALIES$ $(PP,$ $7.0,$ $8.0)$', size='14')
ax1.legend(loc='best')
ax1.set_ylim(-6, 12)

##################
"PLOT PN COMIENZO"
##################

fig = plt.figure(figsize=(8,3))
ax1 = fig.add_subplot(111)
for i in range(len(EVN_PN[:,0])):
    if EVN_PN[i,0] != EVN_PN[i,1]:
        c = EVN_PN[i,0]+np.where(ano_PN[EVN_PN[i,0]:EVN_PN[i,1]+1] == np.max(ano_PN[EVN_PN[i,0]:EVN_PN[i,1]+1]))
        cc = c[0,0]
        if cc <= len(ano_PN)-7:        
            if 6 <= ano_PN[cc-6] < 7:       
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12) ,ano_PN[cc-6:cc+7], linewidth=0.7, color='#2e8b57', alpha = 0.4)
    else:
        if EVN_PN[i,1] <= len(ano_PN)-7:        
            if 6 <= ano_PN[EVN_PN[i,1]-6]< 7:
                ax1.plot((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12), ano_PN[EVN_PN[i,1]-6:EVN_PN[i,1]+7], linewidth=0.7, color='#2e8b57', alpha = 0.4)
my_xticks = ['-36:00','-30:00','-24:00', '-18:00', '-12:00', '-06:00', '00:00', '06:00', '12:00', '18:00', '24:00', '30:00', '36:00']
plt.xticks((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12),my_xticks)
ax1.grid(True)
ax1.set_xlabel('$Time$ $(h)$', size='15')
ax1.set_ylabel('$Speed$ $(m/s)$', size='15')
ax1.set_title('$SPEED$ $ANOMALIES$ $(PN,$ $6.0,$ $7.0)$', size='14')
ax1.legend(loc='best')
ax1.set_ylim(-5, 10)