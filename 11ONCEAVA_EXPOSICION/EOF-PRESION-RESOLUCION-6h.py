# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 08:24:58 2016

@author: yordan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from scipy import linalg as la
import pandas as pd
import pickle
import xlrd
from scipy.stats.stats import pearsonr
import matplotlib.colors as colors
from scipy.stats.stats import pearsonr

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y)) 
        


MASK = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/mascara_1x1.nc')
mask = MASK.variables['lsm'][:]
mask = np.array(mask)
mask = mask.reshape((mask.shape[1], mask.shape[2]))
mask[mask == 1] = np.NaN
mask[mask == 0] = 1
LonM = MASK.variables['longitude'][:]-360
LatM = MASK.variables['latitude'][:]

PR = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/PRESION-SEA-LEVEL-ERA/MSLP_1979_2016.nc')
Variables = [v for v in PR.variables]
print Variables
Pr = PR.variables['msl'][:]/100.
Lat = PR.variables["latitude"][:] 
Lon = PR.variables["longitude"][:]-360

#==============================================================================
'''Se define una sóla variable 'fechas' para todo el código'''
#==============================================================================
# fechas en las que se quiere hacer las EOF's
FECHAS = pd.date_range('1979/01/01 00:00:00', '1979-12-31 23:00:00', freq='6H')
# fechas para calcular ciclos diurno y anual
fechas = pd.date_range('1979/01/01 00:00:00', '2015-12-31 23:00:00', freq='6H')

#==============================================================================
'''Removiendo ciclo diurno y anual SSP'''
#==============================================================================

#def remov_ciclo(mapa, fechas, FECHAS):
#    MAPA = np.zeros((len(FECHAS), mapa.shape[1], mapa.shape[2]))
#    DATA = pd.DataFrame(index=fechas, columns=['datos'])
#    for l in range(mapa.shape[1]):
#        for m in range(mapa.shape[2]):
#            serie = mapa[:len(fechas), l, m]
#            media = np.zeros((12,4)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
#            
#            for i in range(1,13): # Se recorre cada mes
#                for j in range(0, 19, 6): # Se recorre cada horario
#                    selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
#                    for k in range(len(serie)): # Se recorre toda la serie la cuál tiene la misma longitud que fechas
#                        if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
#                            if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
#                                selec.append(serie[k]) # Si cumple, se adiciona a la lista
#                    media[i-1, j/6] = np.mean(selec) # Se guarda el valor de la media
#
#            ano = np.zeros(len(FECHAS))
#            DATA['datos'] = serie
#            SERIE = DATA['datos'][FECHAS[0]:FECHAS[-1]]
#            for n in range(len(ano)):
#                ano[n] = SERIE[n]-media[SERIE.index[n].month-1, SERIE.index[n].hour/6]
#            
#            MAPA[:, l, m] = ano
#    return MAPA
#
#Pr = PR.variables['msl'][:]/100.
#
#P = remov_ciclo(Pr, fechas, FECHAS) 

#==============================================================================
''' Enmascarando datos en terreno continental '''
#==============================================================================

left  =  np.where(LonM == Lon[0])[0][0]
right =  np.where(LonM == Lon[-1])[0][0]
up    =  np.where(LatM == Lat[0])[0][0]
down  =  np.where(LatM == Lat[-1])[0][0]

P = np.zeros((Pr.shape[0], Pr.shape[1], Pr.shape[2]))

for i in range(P.shape[0]): # Se multiplica cada lámina de la serie de presiones por la matríz r, de tal manera que los puntos en tierra no tendrán presiones (nan), mientras que los del océano sí lo harán
    P[i] = Pr[i]*mask[up:down+1, left:right+1]

#==============================================================================
''' Retirando datos enmascarados '''
#==============================================================================

p = P.reshape(P.shape[0], P.shape[1] * P.shape[2]) # Se forma una matríz con las series de presión de cada pixel, en una columna diferente. Será una matríz de dos dimensiones

idx_nan = np.where(np.isnan(p[0])) # Se identifican las posiciones de las columnas o series con Nan
P_no_nan = np.delete(p, idx_nan, 1) # Se elimina de la matriz las columnas o series con NaN

#==============================================================================
'''Removiendo ciclo diurno y anual SSP'''
#==============================================================================

def remov_ciclo(pixeles, fechas, FECHAS):
    PIXELES = np.zeros((len(FECHAS), pixeles.shape[1]))
    DATA = pd.DataFrame(index=fechas, columns=['datos'])
    for l in range(pixeles.shape[1]):
        #for m in range(mapa.shape[2]):
            serie = pixeles[:len(fechas), l]
            media = np.zeros((12,4)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
            
            for i in range(1,13): # Se recorre cada mes
                for j in range(0, 19, 6): # Se recorre cada horario
                    selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
                    for k in range(len(serie)): # Se recorre toda la serie la cuál tiene la misma longitud que fechas
                        if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                            if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                                selec.append(serie[k]) # Si cumple, se adiciona a la lista
                    media[i-1, j/6] = np.mean(selec) # Se guarda el valor de la media

            ano = np.zeros(len(FECHAS))
            DATA['datos'] = serie
            SERIE = DATA['datos'][FECHAS[0]:FECHAS[-1]]
            for n in range(len(ano)):
                ano[n] = SERIE[n]-media[SERIE.index[n].month-1, SERIE.index[n].hour/6]
            
            PIXELES[:, l] = ano
    return PIXELES

p_no_nan = remov_ciclo(P_no_nan, fechas, FECHAS) 

#==============================================================================
'''MATRIZ DE COVARIANZA'''
#==============================================================================

matrix_cov = np.dot(p_no_nan, p_no_nan.T)

#==============================================================================
'''Extracción de valores y vectores propios'''
#==============================================================================

e_val, e_vec = np.linalg.eig(matrix_cov)
e_val = e_val.real; e_vec = e_vec.real

#==============================================================================
'''Varianza Explicada'''
#==============================================================================

sum_evals = np.sum(e_val)
var_exp = (e_val/sum_evals) * 100

#==============================================================================
'''Gráfica de Varianza explicada'''
#==============================================================================

fig = plt.figure(figsize=(8,6))
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

PC = np.dot(e_vec.T, p_no_nan)

#==============================================================================
'''Introduciendo nuevamente las series de np.NaN'''
#==============================================================================

for idx_add in idx_nan[0]:
    PC = np.insert(PC, idx_add, np.array([np.NaN] * PC.shape[0]), 1)

#==============================================================================
'''Volviendo a la forma original de los datos'''
#==============================================================================

PC = PC.reshape(len(FECHAS), Pr.shape[1], Pr.shape[2])

#==============================================================================
'''PLOTEA EOF'''
#==============================================================================

fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
lons,lats = np.meshgrid(Lon,Lat) # Se calcula 2 grillas, una que contiene la longitud y la otra la latitud de cada punto
map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=30, llcrnrlon=-110, urcrnrlon=-65, resolution='i')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 30, 10),labels=[1,0,0,1])
map.drawmeridians(np.arange(-110,-65, 10),labels=[1,0,0,1])
x, y = map(lons,lats) # Se cambian de las coordenadas angulares a las de la proyeccion
bounds=np.linspace(np.nanmin(PC[0]), np.nanmax(PC[0]),25) 
bounds=np.around(bounds, decimals=2) 
csf=map.contourf(x,y, PC[0], 25, norm=MidpointNormalize(midpoint=0), cmap=plt.cm.RdYlBu_r,levels=bounds)
cbar=plt.colorbar(csf,orientation='horizontal', pad=0.05, shrink=0.8, boundaries=bounds)
ax.set_title('PC-1 [50.54%]', size='15', weight='medium')
plt.show()
