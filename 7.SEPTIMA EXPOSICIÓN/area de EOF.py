# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:35:49 2016

@author: yordan
"""

#from mpl_toolkits.basemap import Basemap
#import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
#from scipy import linalg as la
import pandas as pd
#import pickle
#import xlrd
#from scipy.stats.stats import pearsonr
import matplotlib.colors as colors



class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

#==============================================================================
'''LECTURA DE DATOS'''
#==============================================================================

V = nc.Dataset('/home/yordan/YORDAN/UNAL/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO V a 10 m (promedio mensual).nc')
U = nc.Dataset('/home/yordan/YORDAN/UNAL/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO U a 10 m (promedio mensual).nc')
v = V.variables["v10"][:, 24:, 60:181]
u = U.variables["u10"][:, 24:, 60:181]
Lat = V.variables["latitude"][24:] # Se recorta de una vez el arreglo de latitudes de 0 a 24 N
Lon = V.variables["longitude"][60:181]-360 # Se recorta de una vez el arreglo de longitudes de 255 E a 285 E

#==============================================================================
'''SERIE DE VIENTOS PROMEDIO MENSUAL'''
#==============================================================================

spd = np.sqrt(u*u+v*v)

#==============================================================================
'''CICLO ANUAL DE VELOCIDAD DE VIENTOS'''
#==============================================================================

cic_an_speed = np.zeros((12, 97, 121))

for i in range(12):
    for j in range(97):
        for k in range(121):
            cic_an_speed[i,j,k] = np.mean(spd[i::12,j,k])

#==============================================================================
'''REMOCIÓN DE CICLO ANUAL'''
#==============================================================================

spd_ano = np.zeros((spd.shape[0], spd.shape[1], spd.shape[2]))
for i in range(12):
    for j in range(spd_ano.shape[1]):
        for k in range(spd_ano.shape[2]):
            spd_ano[i::12, j, k] = spd[i::12, j, k]-cic_an_speed[i, j, k]

#==============================================================================
'''DOMINIO PARA EOF's'''
#==============================================================================

aux = np.zeros((len(Lat), len(Lon)))
a = len(Lon[:37]) # La posición de la coordenada longitudinal -95.75
b = len(Lat[:29]) # La posición de la coordenada latitudinal 16.75
d = 0
e = 0
for i, j in enumerate(Lon[37:110]):
    if j <= -79.5:
        if i%2 == 0:
            aux[b+i-(i//2):b+i-(i//2)+19,a+i] = 1
        else:
            aux[b+i-((i//2)+1):b+i-((i//2)+1)+19,a+i] = 1
    else:
        if i%2 == 0:
            aux[b+i-(i//2):b+i-(i//2)+17-(5*d),a+i] = 1
            d = d+1
        else:
            aux[b+i-((i//2)+1):b+i-((i//2)+1)+15-(5*e),a+i] = 1
            e = e+1

f = len(Lon[:30]) # La posición de la coordenada longitudinal -97.5
g = len(Lat[:43]) # La posición de la coordenada latitudinal 13.25
for k, l in enumerate(Lon[30:38]):
    if k%2 == 0:
        aux[g+k-(k//2)-(1+(5*(k//2))):g+k-(k//2)+1,f+k] = 1
    else:
        aux[g+k-(k//2)-((k//2)+(4*((k//2)+1))):g+k-(k//2)+1,f+k] = 1

aux[ aux==0 ] = np.NAN
area = spd[0]*aux

#==============================================================================
'''SELECCIÓN DE LAS SERIES'''
#==============================================================================

wh = np.where(aux == 1)
ar = []
for i in range(len(wh[0])):
    ar.append(spd_ano[:,wh[0][i],wh[1][i]])

spd_EOF = np.array(ar)
spd_EOF = spd_EOF.T

#==============================================================================
'''FOURIER Y FILTRADO'''
#==============================================================================

# def Fourier_month(serie):
#     F_TT = np.fft.fft(serie) #FFT de la serie de anomalías
#     fr_TT = np.fft.fftfreq(len(serie), 1) # frrecuencias
#     Periodo = 1/fr_TT[1:len(serie)/2]
#     amplitud = np.abs(F_TT[1:len(serie)/2])
#     potencia = np.abs(F_TT[1:len(serie)/2])**2
#
#     #potencia[36] = 0.0 #Remueve ciclo anual
#     #potencia[73] = 0.0 #Remueve ciclo semianual
#
#     total = np.sum(potencia)
#     var = potencia*100/total
#
#     return var, Periodo
#
# var, periodo = Fourier_month(spd_EOF[:0])
#
# figure = plt.figure(figsize=(10,4))
# ax1 = figure.add_subplot(111)
# ax1.plot(periodo, var, 'g', linewidth = 2)
# ax1.set_title('% of Variance Explained (A)', size='15')
# ax1.set_xlabel('Period (months)', size='14')
# ax1.set_ylabel('% Variance', size='14')
# ax1.set_ylim(0, 12)
# ax1.set_xlim(-10, 150)
# plt.show()
#
# for i in range(len(var)):
#     if periodo == 12 or periodo == 6:
#         print var[i], periodo[i], i

#==============================================================================
'''MATRIZ DE COVARIANZA'''
#==============================================================================

matrix_cov = np.dot(spd_EOF, spd_EOF.T)

#==============================================================================
'''Extracción de valores y vectores propios'''
#==============================================================================

e_values, e_vect = np.linalg.eig(matrix_cov)

e_val = e_values.real; e_vec = e_vect.real

#==============================================================================
'''Varianza Explicada'''
#==============================================================================

sum_evals = np.sum(e_val.real)
var_exp = (e_val.real/sum_evals) * 100

#==============================================================================
'''Gráfica de Varianza explicada'''
#==============================================================================

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.plot(np.arange(1,11), var_exp[0:10], marker='o', color='r')
ax.set_xlabel('Component', size='12', style='oblique')
ax.set_ylabel('Variance [%]', size='12', style='oblique')
ax.grid(True)
ax.set_title('Explained variance', size='12')
plt.show()

#==============================================================================
'''Cálculo de EOF's'''
#==============================================================================

PC = np.dot(e_vec.T, spd_EOF)

#==============================================================================
'''Volviendo a la forma original'''
#==============================================================================

PrCo = np.zeros((spd_ano.shape[0], spd_ano.shape[1], spd_ano.shape[2]))
for i in range(len(wh[0])):
    PrCo[:, wh[0][i], wh[1][i]] = PC[:,i].real


#==============================================================================
'''PLOTEA EOF'''
#==============================================================================

fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
box_lon = [-97.5, -79.5, -77.75, -95.75, -97.5]
box_lat = [13.25, 4.25, 7.75, 16.75, 13.25]
map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=24, llcrnrlon=-105, urcrnrlon=-75, resolution='i')
lons,lats = np.meshgrid(Lon,Lat)
x,y = map(lons,lats)
bounds=np.linspace( np.min(PrCo[2]) ,np.max(PrCo[2]),20)
bounds=np.around(bounds, decimals=2)
csf=map.contourf(x,y, PrCo[2], 20, norm=MidpointNormalize(midpoint=0), cmap=plt.cm.seismic,levels=bounds)
cbar=plt.colorbar(csf,orientation='horizontal', pad=0.05, shrink=0.8, boundaries=bounds)
cbar.set_label('$Amplitud$', fontsize='15')
TT_lon,TT_lat = map(box_lon, box_lat)
map.plot(TT_lon, TT_lat, marker=None, color='k')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 24, 8),labels=[1,0,0,1])
map.drawmeridians(np.arange(-105,-75,10),labels=[1,0,0,1])
ax.set_title('EOF-3 [11.54.%]', size='15', weight='medium')
plt.show()

#==============================================================================
'''Series PC1, PC2, e índices'''
#==============================================================================
A = open('/home/yordan/Escritorio/EXPOSICION 7/INDICES/SOI.bin','rb')
B = open('/home/yordan/Escritorio/EXPOSICION 7/INDICES/MEI.bin','rb')
D = open('/home/yordan/Escritorio/EXPOSICION 7/INDICES/AMO.bin','rb')
E = open('/home/yordan/Escritorio/EXPOSICION 7/INDICES/NAO.bin','rb')

C = xlrd.open_workbook(u'/home/yordan/Escritorio/EXPOSICION 7/INDICES/ONI.xls')
sheet = C.sheet_by_index(0)
oni = np.array(sheet.col_values(0,0))

F = xlrd.open_workbook(u'/home/yordan/Escritorio/EXPOSICION 7/INDICES/indices.xlsx')
sheet1 = F.sheet_by_index(0)
car = np.array(sheet1.col_values(7,0))


ONI = np.zeros(len(oni))
for i in range(len(ONI)):
    ONI[i] = float(oni[i])

CAR = np.zeros(len(car))
for i in range(len(CAR)):
    CAR[i] = float(car[i])

NAO = pickle.load(E)
AMO = pickle.load(D)
MEI = pickle.load(B)
SOI = pickle.load(A)

#==============================================================================
'''Ploteo Series PC1, PC2, e índices'''
#==============================================================================

date = pd.DatetimeIndex(pd.date_range('1979-01','2016-05', freq="M"))
fig = plt.figure(figsize=(15,4.8))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.plot(date, e_vec.T[1], linewidth=1, color='K', label='PC-2')
ax2.plot(date, NAO, color='#23835B', linewidth=1.4, label='NAO')
ax1.set_xlabel('$Time$', size='15')
ax1.set_ylabel('$Amplitude$', size='15')
ax1.legend(loc='upper right')
ax1.set_ylim(-0.15, 0.18)
ax1.set_title('$PC2$ $and$ $NAO$ $index$', size='15')
ax2.grid(True)
ax2.legend(loc='upper center')

cor1 = pearsonr(e_vec.T[0], NAO)[0]
cor2 = pearsonr(e_vec.T[1], NAO)[0]

#==============================================================================
'''MAPA AREA EOF's'''
#==============================================================================

box_lon = [-97.5, -79.5, -77.75, -95.75, -97.5]
box_lat = [13.25, 4.25, 7.75, 16.75, 13.25]
#lat = V.variables["latitude"][59:92] # Para generar la línea que atraviesa los tres puntos
#lon = V.variables["longitude"][99:164:2]-360 # Para generar la línea que atraviesa los tres puntos
lons,lats = np.meshgrid(Lon,Lat)
fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=24, llcrnrlon=-105, urcrnrlon=-75, resolution='i')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 24, 8),labels=[1,0,0,1])
map.drawmeridians(np.arange(-105,-75,10),labels=[1,0,0,1])
#x0, y0 = map(-95.25, 15.25)
#x1, y1 = map(-94.75, 15) # Para generar los tres puntos
#x2, y2 = map(-86.75,11)  # Para generar los tres puntos
#x3, y3 = map(-79.75, 7.5)# Para generar los tres puntos
#x4, y4 = map(-79.25, 7.25)
x,y = map(lons,lats)
TT_lon,TT_lat = map(box_lon, box_lat)
llon, llat = map(lon, lat)
CF = map.contourf(x,y, area[:,:], np.linspace(0, 10, 20), extend='both', cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow
cb = map.colorbar(CF, size="5%", pad="2%", extendrect = 'True', drawedges = 'True', format='%.1f')
cb.set_label('m/s')
ax.set_title('$Linea$ $Hovmoller$', size='15')
#map.plot(TT_lon, TT_lat, marker=None, color='k')
#map.plot(llon, llat, marker=None, color='k')
#map.plot(x0, y0, marker='D', color='m')
#map.plot(x1, y1, marker='D', color='m')
#map.plot(x2, y2, marker='D', color='m')
#map.plot(x3, y3, marker='D', color='m')
#map.plot(x4, y4, marker='D', color='m')
#map.fillcontinents(color='white')
plt.show()
