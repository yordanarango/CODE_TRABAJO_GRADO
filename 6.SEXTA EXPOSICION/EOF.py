# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 11:36:24 2016

@author: yordan
"""

#from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
#from scipy import linalg as la

PR = nc.Dataset('/home/yordan/YORDAN/UNAL/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/PRESION-SEA-LEVEL-ERA/MSLP_1979_2016.nc')
P = PR.variables['msl'][:1000]/100.
Lat = PR.variables["latitude"][:]
Lon = PR.variables["longitude"][:]-360


lons,lats = np.meshgrid(Lon,Lat) # Se calcula 2 grillas, una que contiene la longitud y la otra la latitud de cada punto

map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=30, llcrnrlon=-110, urcrnrlon=-65, resolution='h')
x, y = map(lons,lats) # Se cambian de las coordenadas angulares a las de la proyeccion

r = np.zeros((x.shape[0], x.shape[1])) # Se creo un array de zeros con el mismo tamaño de malla de x o y

for i in range(x.shape[0]): # Se evalúa si cada punto, está o no en tierra. De serlo, la función "is_land" da como resultado True, cambiando el valor de 0 a 1. Si es False, deja el valor en cero
    for j in range(x.shape[1]):
        xx = x[i, j]
        yy = y[i, j]
        r[i, j] = map.is_land(xx, yy)

for i in range(r.shape[0]): # Se necesita que los valores en tierra sean cero, y los puntos en el océano sean uno.
    for j in range(r.shape[1]):
        if r[i, j] == 1:
            r[i, j] = 0
        else:
            r[i, j] = 1

r[r == 0] = np.NaN # Los puntos asignados con 0, se cambian por NaN

for i in range(P.shape[0]): # Se multiplica cada lámina de la serie de presiones por la matríz r, de tal manera que los puntos en tierra no tendrán presiones (nan), mientras que los del océano sí lo harán
    P[i] = P[i]*r


p = P.reshape(P.shape[0], P.shape[1] * P.shape[2]) # Se forma una matríz con las series de presión de cada pixel, en una columna diferente. Será una matríz de dos dimensiones

idx_nan = np.where(np.isnan(p[0])) # Se identifican las posiciones de las columnas o series con Nan
p_no_nan = np.delete(p, idx_nan, 1) # Se elimina de la matriz las columnas o series con NaN

# Removiendo la media de cada variable
p_no_nan_an = np.zeros((p_no_nan.shape[0],p_no_nan.shape[1]))
for i in range(p_no_nan_an.shape[0]):
    p_no_nan_an[i] = p_no_nan[i,:]-np.mean(p_no_nan[i,:])

matrix_cov = np.dot(p_no_nan_an, p_no_nan_an.T)

# Extracción de valores y vectores propios
e_val, e_vec = np.linalg.eig(matrix_cov)

# Varianza Explicada
sum_evals = np.sum(e_val)
var_exp = (e_val/sum_evals) * 100

# Gráfica de Varianza explicada
plt.plot (var_exp[0:10])
plt.show()

# Cálculo de EOF's
PC = np.dot(e_vec.T, p_no_nan)

#Introduciendo nuevamente los series de np.NaN
for idx_add in idx_nan[0]:
    PC = np.insert(PC, idx_add, np.array([np.NaN] * PC.shape[0]), 1)

# Volviendo a la forma original de los datos
PC = PC.reshape(P.shape[0], P.shape[1], P.shape[2])


fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 30, 8),labels=[1,0,0,1])
map.drawmeridians(np.arange(-110,-65,10),labels=[1,0,0,1])
plt.show()
CF = map.contourf(x,y, PC[1], np.linspace(-3800, -3590, 20), extend='both', cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow
cb = map.colorbar(CF, size="5%", pad="2%", extendrect = 'True', drawedges = 'True', format='%.1f')
cb.set_label('m/s')
plt.show()
