from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import pandas as pd

wnd_tehuantepec = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/tehuantepec_wind_data.txt', delimiter=',')
wnd_papagayo = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/papagayo_wind_data.txt', delimiter=',')
wnd_panama = genfromtxt('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/panama_wind_data.txt', delimiter=',')               

V = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO V a 10 m.nc')
U = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO U a 10 m.nc')

v_TT = np.zeros((4383,15,11)) 
u_TT = np.zeros((4383,15,11)) 
v_PP = np.zeros((4383,13,19)) 
u_PP = np.zeros((4383,13,19)) 
v_PN = np.zeros((4383,13,9)) 
u_PN = np.zeros((4383,13,9))

af = np.array((6940, 7940,  8940,  9940,  10940,  11323)) #Intervalos de mil ya que la cantidad de datos es muy grande, y se escoge desde la posición 6940 hasta la 11323 ya que es el intervalo que corresponde a las fechas entre 01/01/1998 hasta 31/12/2009

for i in range(5):
    v_TT[i*1000:(i+1)*1000,:,:]= V.variables["v10"][af[i]:af[i+1], 56:71, 95:106]# Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de tehuantepec 
    u_TT[i*1000:(i+1)*1000,:,:]= U.variables["u10"][af[i]:af[i+1], 56:71, 95:106]# Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de tehuantepec 
    v_PP[i*1000:(i+1)*1000,:,:]= V.variables["v10"][af[i]:af[i+1], 73:86,118:137]# Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de papagayo 
    u_PP[i*1000:(i+1)*1000,:,:]= U.variables["u10"][af[i]:af[i+1], 73:86,118:137]# Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de papagayo
    v_PN[i*1000:(i+1)*1000,:,:]= V.variables["v10"][af[i]:af[i+1], 86:99,157:166]# Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de panama
    u_PN[i*1000:(i+1)*1000,:,:]= U.variables["u10"][af[i]:af[i+1], 86:99,157:166]# Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de panama

spd_TT = np.sqrt(v_TT*v_TT+u_TT*u_TT)
spd_PP = np.sqrt(v_PP*v_PP+u_PP*u_PP)
spd_PN = np.sqrt(v_PN*v_PN+u_PN*u_PN)

###################################
"PROMEDIOS DE LAS ZONAS TT, PP, PN"
###################################

med_spd_TT = np.zeros(4383)
med_spd_PP = np.zeros(4383)
med_spd_PN = np.zeros(4383)

for i in range(4383):
    med_spd_TT[i] = np.mean(spd_TT[i,:,:])
    med_spd_PP[i] = np.mean(spd_PP[i,:,:])
    med_spd_PN[i] = np.mean(spd_PN[i,:,:])

#####################
"EVENTOS TEHUANTEPEC"
#####################

fechas = pd.date_range('1998/01/01', freq='6H', periods=17532) # Serie de fechas cada 6 horas
meses = pd.date_range('1998/01/01', '2009/12/31',freq='M') # Serie de fechas cada mes
clases_TT = np.zeros(144)

evns_tehuantepec = 0
b = np.zeros(4)

# Para entender éste loop, remítase al siguiente loop de igual gerarquía.
for a in range(4):
    if wnd_tehuantepec[a] != 0: # para saber si la posición es diferente de cero
        evns_tehuantepec = evns_tehuantepec+1 # Si se cumple, el contador suma una unidad para destacar la presencia del evento
        for j, k in enumerate(meses): # Esto se hace para saber en cuál de los 144 meses del registro (1998-2009) se da el evento
            if fechas[a].month == k.month and fechas[a].year == k.year: # si el mes y el año del elemento de la serie de fechas coincide con el de el evento, entonces en la posición de ese evento se tendrá una nueva unidad
                clases_TT[j] = clases_TT[j]+1
    if evns_tehuantepec == 1: 
        break

for i in range(len(wnd_tehuantepec)):
   if i < len(wnd_tehuantepec)-4: # Esto se hace para que en la siguiente línea no se genere un error
        if wnd_tehuantepec[i+4] != 0:# para saber si la posición es diferente de cero
            if np.all(wnd_tehuantepec[i:i+4] == b) == True: # Si las 4 posiciones anteriores, a la definida en la línea anterior, son cero, se procede con una nueva instrucción
                evns_tehuantepec = evns_tehuantepec+1
                for j, k in enumerate(meses):
                    if fechas[i+4].month == k.month and fechas[i+4].year == k.year:# si el mes y el año del elemento de la serie de fechas coincide con el de el evento, entonces en la posición de ese evento se tendrá una nueva unidad
                        clases_TT[j] = clases_TT[j]+1



#########                     ###########
         "EVENTOS PAPAGAYO"
#########                     ###########

fechas = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses = pd.date_range('1998/01/01', '2009/12/31',freq='M')
clases_PP = np.zeros(144)

evns_papagayo = 0
pos_evns_papagayo = []
b = np.zeros(4)

for a in range(4):
    if wnd_papagayo[a] != 0:
        evns_papagayo = evns_papagayo+1
#        pos_evns_papagayo.append(a)
        for j, k in enumerate(meses):
            if fechas[a].month == k.month and fechas[a].year == k.year:
                clases_PP[j] = clases_PP[j]+1
    if evns_papagayo == 1:
        break
        
for i in range(len(wnd_papagayo)):
   if i < len(wnd_papagayo)-4:
        if wnd_papagayo[i+4] != 0:
            if np.all(wnd_papagayo[i:i+4] == b) == True:
                evns_papagayo = evns_papagayo+1
#                pos_evns_papagayo.append(i+4)
                for j, k in enumerate(meses):
                    if fechas[i+4].month == k.month and fechas[i+4].year == k.year:
                        clases_PP[j] = clases_PP[j]+1

                

#########                     ###########
         "EVENTOS PANAMA"
#########                     ###########
fechas = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses = pd.date_range('1998/01/01', '2009/12/31',freq='M')
clases_PN = np.zeros(144)

evns_panama = 0
pos_evns_panama = [] 
b = np.zeros(4)

for a in range(4):
    if wnd_panama[a] != 0:
        evns_panama = evns_panama+1
#        pos_evns_panama.append(a)
        for j, k in enumerate(meses):
            if fechas[a].month == k.month and fechas[a].year == k.year:
                clases_PN[j] = clases_PN[j]+1
    if evns_panama == 1:
        break
        
for i in range(len(wnd_panama)): 
   if i < len(wnd_panama)-4:
        if wnd_panama[i+4] != 0:
            if np.all(wnd_panama[i:i+4] == b) == True:
                evns_panama = evns_panama+1
#                pos_evns_panama.append(i+4)
                for j, k in enumerate(meses):
                    if fechas[i+4].month == k.month and fechas[i+4].year == k.year:
                        clases_PN[j] = clases_PN[j]+1


SOI = [-2.53,-1.97,-3.31,-2.80, 0.17, 1.05, 1.49, 0.83, 1.04, 1.01, 1.01, 1.32 
 , 1.58, 0.58, 0.78, 2.10, 0.44, 0.00, 0.52,-0.03,-0.07, 0.95, 1.22, 1.37 
 , 0.47, 1.24, 0.88, 1.76, 0.42,-0.87,-0.34, 0.48, 0.97, 0.87, 2.02, 0.77 
 , 0.78, 1.00, 0.46,-0.18,-0.84,-0.19,-0.27,-1.01, 0.11,-0.38, 0.64,-1.06 
 , 0.20, 0.64,-0.81,-0.48,-1.54,-1.02,-0.70,-1.62,-0.66,-0.79,-0.60,-1.30 
 ,-0.30,-0.90,-0.91,-0.48,-0.85,-1.75, 0.26,-0.35,-0.18,-0.26,-0.32, 0.92 
 ,-1.31, 0.77,-0.11,-1.91, 1.22,-1.91,-0.72,-0.90,-0.31,-0.42,-1.05,-0.94 
 , 0.20,-2.99,-0.26,-1.22,-1.46, 0.11, 0.06,-0.97, 0.34, 1.12,-0.42, 0.01 
 , 1.29,-0.26, 1.93, 1.17,-0.96,-0.98,-0.90,-1.75,-0.60,-1.52, 0.05,-0.39
 ,-0.83,-0.38,-0.30,-0.35,-0.30, 0.14,-0.44, 0.01, 0.12, 0.44, 0.82, 1.49
 , 1.54, 2.05, 1.04, 0.56,-0.25, 0.34, 0.20, 0.64, 1.26, 1.52, 1.64, 1.43
 , 0.85, 1.37,-0.21, 1.06,-0.86,-0.45, 0.18,-0.59, 0.35,-1.66,-0.67,-0.95]

soi = np.array((SOI))

##########################
"PLOT EVENTOS DE CADA MES"
##########################

fig = plt.figure(figsize=(15,4.8))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(np.arange(0,144), clases_PN, linewidth=1.5, color='m', label='Events PN')
my_xticks = ['Jan/98','Jul','Jan/99','Jul','Jan/00','Jul','Jan/01','Jul','Jan/02','Jul','Jan/03','Jul','Jan/04','Jul','Jan/05','Jul','Jan/06','Jul','Jan/07','Jul','Jan/08','Jul','Jan/09','Jul']
plt.xticks(np.arange(0,144,6), my_xticks, rotation=90)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Events$', size='15')
ax1.legend(loc='upper center')
ax1.set_ylim(0, clases_PN.max()+0.5)
ax2.set_ylim(-4, 3)
ax1.set_xlim(0, 145)
ax1.set_title('$Events$ $and$ $SOI$ $index$ $(PN)$', size='15')
ax2.plot(np.arange(0,144), soi, color='k', linewidth=1.5, label='SOI')
ax2.set_ylabel('$SOI$ $index$', size='15')
ax1.grid(True)
ax2.grid(True)
ax2.legend(loc='best')


########################
"EVENTOS DE INVIERNO TT"
########################

n_even_inv_TT = []
soi_inv = []

for i, j in enumerate(meses):
    if j.month == 1 or j.month == 2 or j.month == 3 or j.month == 11 or j.month == 12:
        n_even_inv_TT.append(clases_TT[i])
        soi_inv.append(soi[i])
        
soi_inv_alt = np.array((soi_inv))
n_even_inv_TT_alt = np.array((n_even_inv_TT))

########################
"EVENTOS DE INVIERNO PP"
########################

n_even_inv_PP = []
soi_inv = []

for i, j in enumerate(meses):
    if j.month == 1 or j.month == 2 or j.month == 3 or j.month == 11 or j.month == 12:
        n_even_inv_PP.append(clases_PP[i])
        soi_inv.append(soi[i])
        
soi_inv_alt = np.array((soi_inv))
n_even_inv_PP_alt = np.array((n_even_inv_PP))

########################
"EVENTOS DE INVIERNO PN"
########################

n_even_inv_PN = []
soi_inv = []

for i, j in enumerate(meses):
    if j.month == 1 or j.month == 2 or j.month == 3 or j.month == 11 or j.month == 12:
        n_even_inv_PN.append(clases_PN[i])
        soi_inv.append(soi[i])
        
soi_inv_alt = np.array((soi_inv))
n_even_inv_PN_alt = np.array((n_even_inv_PN))

###########################
"PLOT EVENTOS DE INVIERNO"
###########################

fig = plt.figure(figsize=(15,4.8))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(np.arange(0,60), n_even_inv_PN_alt, linewidth=1.5, color='m', label='Events PN')
my_xticks = ['Jan/98','Jan/99','Jan/00','Jan/01','Jan/02','Jan/03','Jan/04','Jan/05','Jan/06','Jan/07','Jan/08','Jan/09']
plt.xticks(np.arange(0,60,5), my_xticks, rotation=90)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Events$', size='15')
ax1.legend(loc='upper center')
ax1.set_ylim(n_even_inv_PN_alt.min()-0.5, n_even_inv_PN_alt.max()+0.5)
ax1.set_xlim(0, 60)
ax1.set_title('$Events$ $and$ $SOI$ $index$ $(PN)$', size='15')
ax2.plot(np.arange(0,60), soi_inv_alt, color='k', linewidth=1.5, label='SOI')
ax2.set_ylabel('$SOI$ $index$', size='15')
ax1.grid(True)
ax2.grid(True)
ax2.legend(loc='best')


############################
"PROMEDIO DE CADA MES TT"
############################
sum_month_TT = np.zeros(144)
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
        med_evn_TT = np.mean(med_spd_TT[i//4:(j//4)+1]) # Como se sabe la posición hasta donde llega el evento, se procede a calcular el promedio de velocidad en dicho evento
        for jj, kk in enumerate(meses):
            if fechas[i].month == kk.month and fechas[i].year == kk.year: 
                sum_month_TT[jj] = sum_month_TT[jj]+med_evn_TT
                cont_TT[jj] = cont_TT[jj]+1
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar

cont1 = cont_TT
cont_TT[cont_TT==0]=1 # para que la no se de división por cero en la próxima línea
med_evn_TT = sum_month_TT/cont_TT # Promedio en cada mes


############################
"PROMEDIO DE CADA MES PP"
############################
sum_month_PP = np.zeros(144)
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
        med_evn_PP = np.mean(med_spd_PP[i//4:(j//4)+1]) # Como se sabe la posición hasta donde llega el evento, se procede a calcular el promedio de velocidad en dicho evento
        for jj, kk in enumerate(meses):
            if fechas[i].month == kk.month and fechas[i].year == kk.year: 
                sum_month_PP[jj] = sum_month_PP[jj]+med_evn_PP
                cont_PP[jj] = cont_PP[jj]+1
        i = j+4        
    else:
        i = i+1

cont2 = cont_PP
cont_PP[cont_PP==0]=1
med_evn_PP = sum_month_PP/cont_PP

############################
"PROMEDIO DE CADA MES PN"
############################
sum_month_PN = np.zeros(144)
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
        med_evn_PN = np.mean(med_spd_PN[i//4:(j//4)+1]) # Como se sabe la posición hasta donde llega el evento, se procede a calcular el promedio de velocidad en dicho evento
        for jj, kk in enumerate(meses):
            if fechas[i].month == kk.month and fechas[i].year == kk.year: 
                sum_month_PN[jj] = sum_month_PN[jj]+med_evn_PN
                cont_PN[jj] = cont_PN[jj]+1
        i = j+4
    else:
        i = i+1

cont3 = cont_PN
cont_PN[cont_PN==0]=1
med_evn_PN = sum_month_PN/cont_PN

########################
"PLOT MEDIA DE CADA MES"
########################

fig = plt.figure(figsize=(15,4.8))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(np.arange(0,144), med_evn_PN, linewidth=1.5, color='m', label='Mean PN')
my_xticks = ['Jan/98','Jul','Jan/99','Jul','Jan/00','Jul','Jan/01','Jul','Jan/02','Jul','Jan/03','Jul','Jan/04','Jul','Jan/05','Jul','Jan/06','Jul','Jan/07','Jul','Jan/08','Jul','Jan/09','Jul']
plt.xticks(np.arange(0,144,6), my_xticks, rotation=90)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Monthly$ $Mean $ $(m/s)$', size='15')
ax1.legend(loc='upper center')
ax1.set_ylim(0, 10)
ax2.set_ylim(-4, 3)
ax1.set_xlim(0, 145)
ax1.set_title('$Monthly$ $Mean$ $and$ $SOI$ $index$ $(PN)$', size='15')
ax2.plot(np.arange(0,144), soi, color='k', linewidth=1.5, label='SOI')
ax2.set_ylabel('$SOI$ $index$', size='15')
ax1.grid(True)
ax2.grid(True)
ax2.legend(loc='best')


########################
"MEDIA DE INVIERNO TT"
########################

med_evn_inv_TT = []
soi_inv = []

for i, j in enumerate(meses):
    if j.month == 1 or j.month == 2 or j.month == 3 or j.month == 11 or j.month == 12:
        med_evn_inv_TT.append(med_evn_TT[i])
        soi_inv.append(soi[i])
        
soi_inv_alt = np.array((soi_inv))
med_evn_inv_TT_alt = np.array((med_evn_inv_TT))

########################
"MEDIA DE INVIERNO PP"
########################

med_evn_inv_PP = []
soi_inv = []

for i, j in enumerate(meses):
    if j.month == 1 or j.month == 2 or j.month == 3 or j.month == 11 or j.month == 12:
        med_evn_inv_PP.append(med_evn_PP[i])
        soi_inv.append(soi[i])
        
soi_inv_alt = np.array((soi_inv))
med_evn_inv_PP_alt = np.array((med_evn_inv_PP))

########################
"MEDIA DE INVIERNO PN"
########################

med_evn_inv_PN = []
soi_inv = []

for i, j in enumerate(meses):
    if j.month == 1 or j.month == 2 or j.month == 3 or j.month == 11 or j.month == 12:
        med_evn_inv_PN.append(med_evn_PN[i])
        soi_inv.append(soi[i])
        
soi_inv_alt = np.array((soi_inv))
med_evn_inv_PN_alt = np.array((med_evn_inv_PN))

###########################
"PLOT MEDIAS DE INVIERNO"
###########################

fig = plt.figure(figsize=(15,4.8))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(np.arange(0,60), med_evn_inv_PN_alt, linewidth=1.5, color='m', label='Events PN')
my_xticks = ['Jan/98','Jan/99','Jan/00','Jan/01','Jan/02','Jan/03','Jan/04','Jan/05','Jan/06','Jan/07','Jan/08','Jan/09']
plt.xticks(np.arange(0,60,5), my_xticks, rotation=90)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Monthly$ $Mean$ $(m/s)$', size='15')
ax1.legend(loc='upper center')
ax1.set_ylim(0, 9.5)
ax2.set_ylim(-4, 3)
ax1.set_xlim(0, 60)
ax1.set_title('$Monthly$ $Mean$ $and$ $SOI$ $index$ $(PN)$', size='15')
ax2.plot(np.arange(0,60), soi_inv_alt, color='k', linewidth=1.5, label='SOI')
ax2.set_ylabel('$SOI$ $index$', size='15')
ax1.grid(True)
ax2.grid(True)
ax2.legend(loc='best')
