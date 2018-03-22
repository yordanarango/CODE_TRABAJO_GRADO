# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 20:31:23 2016

@author: yordan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from scipy import linalg as la

PR = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/PRESION-SEA-LEVEL-ERA/MSLP_1979_2016_MENSUAL_RESOL.nc')
Pr = PR.variables['msl'][:]/100.
Lat = PR.variables["latitude"][:] 
Lon = PR.variables["longitude"][:]-360

# Calculo de ciclo anual
ciclo = np.zeros((12, Pr.shape[1], Pr.shape[2]))

for i in range(12):
    for j in range(Pr.shape[1]):
        for k in range(Pr.shape[2]):
            ciclo[i,j,k] = np.mean(Pr[i::12,j,k])

#Removiendo ciclo anual
P = np.zeros((Pr.shape[0], Pr.shape[1], Pr.shape[2]))
for i in range(ciclo.shape[0]):
    for j in range(Pr.shape[1]):
        for k in range(Pr.shape[2]):
            P[i::12, j, k] = Pr[i::12, j, k]-ciclo[i,j,k]

#==============================================================================
''' Alternativa para hacer el filtro del ciclo anual '''
#==============================================================================
#PP = np.zeros((Pr.shape[0], Pr.shape[1], Pr.shape[2]))
#for i in range(Pr.shape[0]):
#    PP[i, :, :] = Pr[i, :, :]-ciclo[i%12, :, :]

#==============================================================================


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
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.plot(np.arange(1,11), var_exp[0:10], marker='o', color='r')
ax.set_xlabel('Component', size='12', style='oblique')
ax.set_ylabel('Variance [%]', size='12', style='oblique')
ax.grid(True)
ax.set_title('Explained variance', size='12')
plt.show()

# Cálculo de EOF's
PC = np.dot(e_vec.T, p_no_nan_an)

#Introduciendo nuevamente los series de np.NaN
for idx_add in idx_nan[0]:
    PC = np.insert(PC, idx_add, np.array([np.NaN] * PC.shape[0]), 1)

# Volviendo a la forma original de los datos
PC = PC.reshape(P.shape[0], P.shape[1], P.shape[2])

fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
CF = map.contourf(x,y, PC[1], np.linspace(-22, 15, 30), extend='both', cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow
cb = map.colorbar(CF, size="5%", pad="2%", extendrect = 'True', drawedges = 'True', format='%.1f')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 40, 8),labels=[1,0,0,1])
map.drawmeridians(np.arange(-120,-55,10),labels=[1,0,0,1])
ax.set_title('PC-2  [22.8%]', size='15', weight='medium')
plt.show()
