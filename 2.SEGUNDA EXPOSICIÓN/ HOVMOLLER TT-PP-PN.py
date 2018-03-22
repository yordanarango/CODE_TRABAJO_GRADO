from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

V = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO V a 10 m.nc')
U = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO U a 10 m.nc')

a = 152

v_pru = np.zeros((a, 33))
u_pru = np.zeros((a, 33))

for i in range(a):
    for j in range(33):
        v_pru[i,j] = V.variables['v10'][13453+i,59+j,99+2*j] #desde 15.25N-95.25W, hasta 7.25N-79.25W
        u_pru[i,j] = U.variables['u10'][13453+i,59+j,99+2*j]
        
spd_pru = np.sqrt(v_pru*v_pru+u_pru*u_pru)

time = np.arange(0,a)
pos = np.arange(0,33)

x, y = np.meshgrid(pos, time)

fig = plt.figure(figsize=(5,6), edgecolor='W',facecolor='W')
ax1 = fig.add_axes([0.0,0.1,0.8,0.8])

cd = ax1.contourf(x, y, spd_pru, np.linspace(6.5,20, 20), cmap=plt.cm.rainbow)
ce = plt.colorbar(cd, drawedges = 'True',format='%.1f')
ce.set_label('m/s')

my_yticks = pd.date_range('2015/11/01', '2016/03/31', freq='15D')
plt.yticks([0,15,30,45,60,75,90,105,120,135,150], my_yticks) #0,12,24,36,48,60

my_xticks = ['$TT$ $(15N,$ $94.75W)$','$PP$ $(11N,$ $86.75W)$','$PN$ $(7.5N,$ $79.75W)$']
plt.xticks((1,17,31), my_xticks, size=11)
plt.grid(True)

ax1.set_title('$Hovmoller$ $Vientos$ $2015-2016$', size='15')
ax1.set_xlabel('$Posicion$', size='15')
ax1.set_ylabel('$Tiempo$', size='15')