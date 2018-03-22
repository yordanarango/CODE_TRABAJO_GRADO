from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/EVENTOS_950_hPa_2/VIENTOS_2/Evento_Panama_950_2.nc')

Variables = [v for v in Archivo.variables]
print Variables

Lon = Archivo.variables['longitude'][:]-360
Lat = Archivo.variables['latitude'][:]
time = Archivo.variables['time'][:]

u_PN = np.zeros((16,6))
v_PN = np.zeros((16,6))

for i in range(16):
    for j in range(6):
        u_PN[i,j] = Archivo.variables['u'][i,14+j*3,33-j]
        v_PN[i,j] = Archivo.variables['v'][i,14+j*3,33-j]

spd_PN = np.sqrt(u_PN*u_PN+v_PN*v_PN)

time = np.arange(0,16)
pos = np.arange(0,6)

x, y = np.meshgrid(pos, time)


fig = plt.figure(figsize=(10,5), edgecolor='W',facecolor='W')
ax1 = fig.add_axes([0.0,0.1,0.8,0.8])

cd = ax1.contourf(x, y, spd_PN, np.linspace(0,16, 20), cmap=plt.cm.rainbow)
ce = plt.colorbar(cd, drawedges = 'True',format='%.1f')
ce.set_label('m/s')

my_yticks = pd.date_range('1998/03/10', '1998/03/13', freq='D')
plt.yticks([0,4,8,12],my_yticks)

my_xticks = ['$78.875N$', '$79.0N$', '$79.125N$', '$79.25N$', '$79.375N$', '$79.5N$']
plt.xticks([0,1,2,3,4,5], my_xticks, size=13)
plt.grid(True)

ax1.set_title('$Vientos$ $a$ $950$ $hPa$ $(Panama)$', size='15')
ax1.set_xlabel('$Latitud$ $(\Delta N=0.325)$', size='15')
ax1.set_ylabel('$Tiempo$', size='15')




















