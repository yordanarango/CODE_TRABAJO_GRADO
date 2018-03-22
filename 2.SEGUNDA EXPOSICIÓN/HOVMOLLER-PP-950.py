from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/EVENTOS_950_hPa_2/VIENTOS_2/Evento_Papagayo_950_2.nc')

Variables = [v for v in Archivo.variables]
print Variables


Lon = Archivo.variables['longitude'][:]-360
Lat = Archivo.variables['latitude'][:]
time = Archivo.variables['time'][:]

u_PP = np.zeros((16,11))
v_PP = np.zeros((16,11))

for i in range(16):
    for j in range(11):
        u_PP[i,j] = Archivo.variables['u'][i,14+j,38-j*3]

spd_PP = np.sqrt(u_PP*u_PP+v_PP*v_PP)

time = np.arange(0,16)
pos = np.arange(0,11)

x, y = np.meshgrid(pos, time)

fig = plt.figure(figsize=(10,5), edgecolor='W',facecolor='W')
ax1 = fig.add_axes([0.0,0.1,0.8,0.8])

cd = ax1.contourf(x, y, spd_PP, np.linspace(0,16,20), cmap=plt.cm.rainbow)
ce = plt.colorbar(cd, drawedges = 'True',format='%.1f')
ce.set_label('m/s')

my_yticks = pd.date_range('2003/03/30', '2003/04/02', freq='D')
plt.yticks([0,4,8,12], my_yticks)

my_xticks = ['$12.25N$', '$12.0N$', '$11.75N$', '$11.5N$', '$11.25N$', '$11.0N$']
plt.xticks([0,2,4,6,8,10], my_xticks, size=13)
plt.grid(True)

ax1.set_title('$Vientos$ $a$ $950$ $hPa$ $(Papagayo)$', size='15')
ax1.set_xlabel('$Latitud$ $($ $\Delta W=0.325)$', size='15')
ax1.set_ylabel('$Tiempo$', size='15')































