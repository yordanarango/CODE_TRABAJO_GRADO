# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 21:59:37 2016

@author: yordan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from scipy import linalg as la
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

posiciones = ['TT','PP','PN','G','C']
longitudes = [-95.0, -87.5, -79.75, -93.0, -75.0]
latitudes = [14.5, 10.25, 7.5, 21.0, 13.0]

datep = pd.date_range('1979-01-01 00:00:00', '2015-12-31 23:00:00', freq='3H')
date = pd.DatetimeIndex(datep)
Serie = pd.DataFrame(index=date, columns=['TT','PP', 'PN','G','C']) 

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
TT = MA[:,0]
PP = MA[:,1]
PN = MA[:,2]
G = MA[:,3]
C = MA[:,4]

#def ser_anom(serie):
#    ciclo = np.zeros(12)
#    datep = pd.date_range('1979-01-01 00:00:00', '2015-12-31 23:00:00', freq='3H')
#    for i in range(12):
#        aux_cic = []
#        for j in range(len(serie)):
#            if datep[j].month == i+1:
#                aux_cic.append(serie[j])
#        ciclo[i] = np.mean(aux_cic)
#    
#    anom = np.zeros(len(serie))
#    for k in range(12):
#        for l in range(len(anom)):
#            if datep[l].month == k+1:  
#                anom[l] = serie[l]-ciclo[k]
#    
#    return anom
#
#TT_anom = ser_anom(TT)
#PP_anom = ser_anom(PP)
#PN_anom = ser_anom(PN)
#G_anom = ser_anom(G)
#C_anom = ser_anom(C)

#==============================================================================
'''TRANSFORMADA DE FOURIER HORARIO'''
#==============================================================================

def Fourier(serie):
    F_TT = np.fft.fft(serie) #FFT de la serie de anomalías
    fr_TT = np.fft.fftfreq(len(serie), 3) # frrecuencias
    Periodo = 1/(fr_TT[1:len(serie)/2]*24)
    amplitud = np.abs(F_TT[1:len(serie)/2])
    potencia = np.abs(F_TT[1:len(serie)/2])**2
    
    potencia[36]    = 0.0 #Removiendo el ciclo anual    
    potencia[73]    = 0.0 #Removiendo el ciclo semianual   
    potencia[13513] = 0.0 #Removiendo el ciclo diurno   
    potencia[27027] = 0.0 #Removiendo el ciclo semidiurno   
    #potencia[13476] = 0.0 #Removiendo banda del ciclo diurno, sólo para PP   
    #potencia[13550] = 0.0 #Removiendo banda del ciclo diurno, sólo para PP
    
    total = np.sum(potencia)
    var = potencia*100/total
    
    return var, Periodo

var, periodo = Fourier(C)

figure = plt.figure(figsize=(10,4))
ax1 = figure.add_subplot(111)
ax1.plot(periodo, var, 'b', linewidth = 2) 
ax1.set_title('% of Variance Explained (C) / 122 days-2.8% ', size='15')
ax1.set_xlabel('Period (days)', size='14')
ax1.set_ylabel('% Variance', size='14')
ax1.set_ylim(0, 3.0)
ax1.set_xlim(-10, 500)
plt.show()

for i in range(len(var)):
    if var[i] >= 2.:
        print var[i], periodo[i], i
        
##==============================================================================
#'''SELECCIÓN DE SERIES RESOLUCIÓN MENSUAL'''
##==============================================================================
#
#Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/PRESION-SEA-LEVEL-ERA/MSLP_1979_2016_MENSUAL.nc')
#Variables = [v for v in Archivo.variables]
#PR = Archivo.variables['msl'][:-7]/100
#
#LON = Archivo.variables['longitude'][:]-360
#LAT = Archivo.variables['latitude'][:]
#
##posiciones = ['TT','PP','PN','G','C', 'A']
#posiciones = [0, 1, 2, 3, 4, 5]
#longitudes = [-95.25, -87.75, -79.5, -93.0, -75.0, -60.0]
#latitudes = [14.25, 10.5, 7.5, 21.0, 12.75, 27.0]
#
#Serie = np.zeros((PR.shape[0], 6))
#
#for i, j, k in zip(longitudes,latitudes, posiciones):
#        lOn = np.where(LON == i)[0][0]
#        lAt = np.where(LAT == j)[0][0]
#        Serie[:,k] = PR[:, lAt, lOn]
#        
#TT_month = Serie[:,0]
#PP_month = Serie[:,1]
#PN_month = Serie[:,2]
#G_month = Serie[:,3]
#C_month = Serie[:,4]
#A_month = Serie[:,5]
#
#def anom_month(serie):
#    ciclo = np.zeros(12)
#    for i in range(12):
#        ciclo[i] = np.mean(serie[i::12])
#
#    month_anom = np.zeros(len(serie))
#
#    for j in range(12):
#        month_anom[j::12] = serie[j::12]-ciclo[j]
#    
#    return month_anom
#
#TT_anom_month = anom_month(TT_month)
#PP_anom_month = anom_month(PP_month)
#PN_anom_month = anom_month(PN_month)
#G_anom_month  = anom_month(G_month)
#C_anom_month  = anom_month(C_month)
#A_anom_month  = anom_month(A_month)
#
##==============================================================================
#'''TRANSFORMADA DE FOURIER MENSUAL'''
##==============================================================================
#
#def Fourier_month(serie):
#    F_TT = np.fft.fft(serie) #FFT de la serie de anomalías
#    fr_TT = np.fft.fftfreq(len(serie), 1) # frrecuencias
#    Periodo = 1/fr_TT[1:len(serie)/2]
#    amplitud = np.abs(F_TT[1:len(serie)/2])
#    potencia = np.abs(F_TT[1:len(serie)/2])**2
#
#    potencia[36] = 0.0 #Remueve ciclo anual    
#    potencia[73] = 0.0 #Remueve ciclo semianual
#    
#    total = np.sum(potencia)
#    var = potencia*100/total
#    
#    return var, Periodo
#
#var, periodo = Fourier_month(A_month)
#
#figure = plt.figure(figsize=(10,4))
#ax1 = figure.add_subplot(111)
#ax1.plot(periodo, var, 'g', linewidth = 2) 
#ax1.set_title('% of Variance Explained (A)', size='15')
#ax1.set_xlabel('Period (months)', size='14')
#ax1.set_ylabel('% Variance', size='14')
#ax1.set_ylim(0, 12)
#ax1.set_xlim(-10, 150)
#plt.show()
#
#for i in range(len(var)):
#    if var[i] >= 2.0:
#        print var[i], periodo[i], i
#
#print var[110], periodo[110]
#print var[73], periodo[73]
#print var[36], periodo[36]
#print var[14], periodo[14]
#print var[9], periodo[9]
#print var[7], periodo[7]
#
##==============================================================================
#'''TRANSFORMADA DE FORMA ALTERNA'''
##==============================================================================
#
#freq,Yf=Fourier(A) # Función en carpeta "Códigos útiles"
#semi,anual,inter,var_coefs=varianzas_monthlyseries(A)
#
#figure = plt.figure(figsize=(15,7))
#ax1 = figure.add_subplot(111)
#ax1.plot(freq, var_coefs, 'k', linewidth = 2) 
#ax1.set_title('% of Variance Explained (A)', size='15')
#ax1.set_xlabel('Period (months)', size='15')
#ax1.set_ylabel('% Variance', size='15')
#plt.show()
#
#ones = []
#
#for i in range(len(freq)):
#    if var_coefs[i]>=2:
#        ones.append((freq[i], var_coefs[i]))
#
##==============================================================================
#
#p_TT_lon = -95.0
#p_TT_lat = 14.5
#p_PP_lon = -87.5
#p_PP_lat = 10.25
#p_PN_lon = -79.75
#p_PN_lat = 7.5
#
#p_G_lon = -93.0
#p_G_lat = 21.0
#p_C_lon = -75.0
#p_C_lat = 13.0
#p_A_lon = -60.0
#p_A_lat = 27.0
#
#box_TT_lon = [-96.25, -96.25, -93.75, -93.75, -96.25]
#box_TT_lat = [16, 12.5, 12.5, 16, 16]
#box_PP_lon = [-90.5, -90.5, -86.0, -86.0, -90.5]
#box_PP_lat = [11.75, 8.75, 8.75, 11.75, 11.75]
#box_PN_lon = [-80.75, -80.75, -78.75, -78.75, -80.75]
#box_PN_lat = [8.5, 5.5, 5.5, 8.5, 8.5]
#
#fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
#ax = fig.add_axes([0.1,0.1,0.8,0.8])
#map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=24, llcrnrlon=-105, urcrnrlon=-75, resolution='i')
#map.drawcoastlines(linewidth = 0.8)
#map.drawcountries(linewidth = 0.8)
#map.drawparallels(np.arange(0, 24, 8),labels=[1,0,0,1])
#map.drawmeridians(np.arange(-105,-75,10),labels=[1,0,0,1])
#lons,lats = np.meshgrid(LON,LAT)
#x, y = map(lons,lats)
#
#P_TT_lon, P_TT_lat = map(p_TT_lon, p_TT_lat) 
#P_PP_lon, P_PP_lat = map(p_PP_lon, p_PP_lat)  
#P_PN_lon, P_PN_lat = map(p_PN_lon, p_PN_lat)
#P_G_lon, P_G_lat = map(p_G_lon, p_G_lat)
#P_C_lon, P_C_lat = map(p_C_lon, p_C_lat)
#P_A_lon, P_A_lat = map(p_A_lon, p_A_lat)
#TT_lon,TT_lat = map(box_TT_lon, box_TT_lat)
#PP_lon,PP_lat = map(box_PP_lon, box_PP_lat)
#PN_lon,PN_lat = map(box_PN_lon, box_PN_lat)
#
#bounds=np.linspace( np.min(PR) ,np.max(PR), 30) 
#bounds=np.around(bounds, decimals=2) 
#CF = map.contourf(x,y, PR, bounds, cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow
#cb = plt.colorbar(CF, orientation='verticalal', pad=0.05, shrink=0.8, boundaries=bounds)
#cb.set_label('hPa')
#ax.set_title('SLP Anomalies', size='15', weight='medium')
#
#map.plot(P_TT_lon, P_TT_lat, marker='D', color='k')
#map.plot(P_PP_lon, P_PP_lat, marker='D', color='k')
#map.plot(P_PN_lon, P_PN_lat, marker='D', color='k')
#
#map.plot(P_G_lon, P_G_lat, marker='D', color='k')
#map.plot(P_C_lon, P_C_lat, marker='D', color='k')
#map.plot(P_A_lon, P_A_lat, marker='D', color='k')
#
#map.plot(TT_lon, TT_lat, marker=None, color='k')
#map.plot(PP_lon, PP_lat, marker=None, color='k')
#map.plot(PN_lon, PN_lat, marker=None, color='k')      
#
#map.fillcontinents(color='white')
#
#plt.show()
