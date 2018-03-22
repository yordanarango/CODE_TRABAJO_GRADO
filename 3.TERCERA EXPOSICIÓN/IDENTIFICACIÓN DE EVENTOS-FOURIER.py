import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pylab import hist, show
import pylab as pl
from numpy import genfromtxt

Archivo = nc.Dataset('/home/yordan/YORDAN/UNAL/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/U y V, 6 horas, 10 m, 1979-2016.nc')


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

#########################
"TRANSFORMADA DE FOURIER"    
#########################    
            
A_TT = np.fft.fft(ano_TT) #FFT de la serie de anomalías
fr_TT = np.fft.fftfreq(len(ano_TT),6) # frrecuencias

for i in range(len(fr_TT)): # Filtrado
    if fr_TT[149]<abs(fr_TT[i])<=fr_TT[6576]: # La frecuencia fr[149], es la frecuencia más cercana a la frecuencia de los dos días (48 horas), es decir 1/48h es casi igual fr[149]. Y la frecuencia fr[6576] corresponde a la frecuencia de los 90 días (2160 horas), es decir 1/2160 = fr[6576]
        pass
    else:
        A_TT[i]=0



A_PP = np.fft.fft(ano_PP) #FFT de la serie de anomalías
fr_PP = np.fft.fftfreq(len(ano_PP),6) # frrecuencias

for i in range(len(fr_PP)): # Filtrado
    if fr_PP[149]<abs(fr_PP[i])<=fr_PP[6576]: # La frecuencia fr[149], es la frecuencia más cercana a la frecuencia de los 90 días (2160 horas), es decir 1/2160h es casi igual a fr[149]. Y la frecuencia fr[6576] corresponde a la frecuencia de los dos días (48 horas), es decir 1/48 = fr[6576]
        pass
    else:
        A_PP[i]=0



A_PN = np.fft.fft(ano_PN) #FFT de la serie de anomalías
fr_PN = np.fft.fftfreq(len(ano_PN),6) # frrecuencias

for i in range(len(fr_PN)): # Filtrado
    if fr_PN[149]<abs(fr_PN[i])<=fr_PN[6576]: # La frecuencia fr[149], es la frecuencia más cercana a la frecuencia de los dos días (48 horas), es decir 1/48h es casi igual fr[149]. Y la frecuencia fr[6576] corresponde a la frecuencia de los 90 días (2160 horas), es decir 1/2160 = fr[6576]
        pass
    else:
        A_PN[i]=0
        
######################
"TRANSFORMADA INVERSA"    
######################  
serfilt_TT = np.fft.ifft(A_TT)
serfilt_PP = np.fft.ifft(A_PP)
serfilt_PN = np.fft.ifft(A_PN)

#fig=pl.figure(figsize=(7,5))
#ax = fig.add_subplot(1,1,1)
#hN,bN,pN = hist(serfilt.real, bins=40, normed=True, color='b', lw=1, alpha=0.2)
#ax.set_xlabel('$Speed$ $(m/s)$', size='15')
#ax.set_ylabel('$Relative$ $frecuence$', size='15')
#ax.set_title('$Histogram$ $(PN)$', size='15')
#des = np.std(serfilt.real)
#plt.axvline(x=2*des, linewidth=1.5, color='r')
#plt.axvline(x=-2*des, linewidth=1.5, color='g')

##############################################################################
"IDENTIFICACIÓN DE FECHAS QUE SUPERAN UMBRAL DE LAS DOS DESVIACIONES ESTANDAR"
##############################################################################

Ser_TT = np.zeros(len(spd_TT))
Ser_PP = np.zeros(len(spd_PP))
Ser_PN = np.zeros(len(spd_PN))

###### TT ######
for i in range(len(Ser_TT)):
    if serfilt_TT.real[i] > 2*np.std(serfilt_TT.real):
        Ser_TT[i] = spd_TT[i]

##### PP ######
for i in range(len(Ser_PP)):
    if serfilt_PP.real[i] > 2*np.std(serfilt_PP.real):
        Ser_PP[i] = spd_PP[i]

#### PN ######
for i in range(len(Ser_PN)):
    if serfilt_PN.real[i] > 2*np.std(serfilt_PN.real):
        Ser_PN[i] = spd_PN[i]

##################################################################
"NÚMERO  DE EVENTOS DE CADA MES EN TT (BASE DE DATOS ERA INTERIM)"
##################################################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
cont_TT = np.zeros(144)
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
        for jj, kk in enumerate(meses1):
            if fechas1[i].month == kk.month and fechas1[i].year == kk.year: 
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
cont_PP = np.zeros(144)
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
        for jj, kk in enumerate(meses1):
            if fechas1[i].month == kk.month and fechas1[i].year == kk.year: 
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
cont_PN = np.zeros(144)
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
        for jj, kk in enumerate(meses1):
            if fechas1[i].month == kk.month and fechas1[i].year == kk.year: 
                cont_PN[jj] = cont_PN[jj]+1
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar
cont6 = cont_PN

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
cont_TT2 = np.zeros(144)
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
                cont_TT2[jj] = cont_TT2[jj]+1
        i = j+4 # ésta sería la nueva posición donde comienza todo el bucle     
    else:
        i = i+1 # Siguiente posicion a examinar

cont1 = cont_TT2

##########################################
"NÚMERO DE EVENTOS DE CADA MES PP EN RASI"
##########################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
cont_PP2 = np.zeros(144)
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
                cont_PP2[jj] = cont_PP2[jj]+1
        i = j+4        
    else:
        i = i+1

cont2 = cont_PP2

##########################################
"NÚMERO DE EVENTOS DE CADA MES PN EN RASI"
##########################################

fechas1 = pd.date_range('1998/01/01', freq='6H', periods=17532)
meses1 = pd.date_range('1998/01/01', '2009/12/31',freq='M')
cont_PN2 = np.zeros(144)
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
                cont_PN2[jj] = cont_PN2[jj]+1
        i = j+4
    else:
        i = i+1
cont3 = cont_PN2

##########################
"PLOT EVENTOS DE CADA MES"
##########################

fig = plt.figure(figsize=(15,4.8))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(0,144), cont3, marker='o', color='#e53935', label='RASI Events')
ax1.plot(np.arange(0,144), cont6, marker='D', color='#00796b', label='ERA Events')
my_xticks = ['Jan/98','Jul','Jan/99','Jul','Jan/00','Jul','Jan/01','Jul','Jan/02','Jul','Jan/03','Jul','Jan/04','Jul','Jan/05','Jul','Jan/06','Jul','Jan/07','Jul','Jan/08','Jul','Jan/09','Jul']
plt.xticks(np.arange(0,144,6), my_xticks, rotation=90)
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Events$', size='15')
ax1.legend(loc='best')
ax1.set_ylim(cont6.min()-0.5, 7.5)
ax1.set_xlim(0, 145)
ax1.set_title('$RASI$ $and$ $ERA$ $events$ $(PN)$', size='15')
ax1.grid(True)