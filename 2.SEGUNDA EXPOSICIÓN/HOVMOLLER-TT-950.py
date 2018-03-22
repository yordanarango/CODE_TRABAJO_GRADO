from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/EVENTOS_950_hPa_2/VIENTOS_2/Evento_Tehuantepec_950_2.nc')

Variables = [v for v in Archivo.variables]
print Variables



Lon = Archivo.variables['longitude'][:]-360
Lat = Archivo.variables['latitude'][:]
time = Archivo.variables['time'][:]

u_TT = np.zeros((16,35))
v_TT = np.zeros((16,35))

for i in range(16):
    for j in range(35):
        u_TT[i,j] = Archivo.variables['u'][i,14+j,18]
        v_TT[i,j] = Archivo.variables['v'][i,14+j,18]

spd_TT = np.sqrt(u_TT*u_TT+v_TT*v_TT)

time = np.arange(0,16)
pos = np.arange(0,35)

x, y = np.meshgrid(pos, time)

fig = plt.figure(figsize=(10,5), edgecolor='W',facecolor='W')
ax1 = fig.add_axes([0.0,0.1,0.8,0.8])

cd = ax1.contourf(x, y, spd_TT, np.linspace(0,34, 30), cmap=plt.cm.rainbow)
ce = plt.colorbar(cd, drawedges = 'True',format='%.1f')
ce.set_label('m/s')

my_yticks = pd.date_range('2007/03/03', '2007/03/06', freq='D')
plt.yticks([0,4,8,12],my_yticks)

my_xticks = ['$19.25N$', '$18.625N$', '$18.0N$', '$17.375N$', '$16.75N$', '$16.125N$', '$15.5N$', '$15.0N$']
plt.xticks([0,5,10,15,20,25,30,34], my_xticks, size=13)
plt.grid(True)

ax1.set_title('$Vientos$ $a$ $950$ $hPa$ $(Tehuantepec)$', size='15')
ax1.set_xlabel('$Latitud-$ $(94.75W)$', size='15')
ax1.set_ylabel('$Tiempo$', size='15')


