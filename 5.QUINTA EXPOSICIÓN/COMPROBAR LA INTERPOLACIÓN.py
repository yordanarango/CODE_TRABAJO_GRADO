from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

#################### 
"LECTURA DE DATOS"
#################### 
           
V = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS NARR/MERIDIONAL/MERIDIONAL-alt/1979alt.nc')
U = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS NARR/ZONAL/ZONAL-pr/1979alt.nc')
v = V.variables["V"][:, :, :]
u = U.variables["U"][:, :, :]
Lat = V.variables["LAT"][:] # Se recorta de una vez el arreglo de latitudes de 0 a 24 N
Lon = V.variables["LON"][:]-360 # Se recorta de una vez el arreglo de longitudes de 255 E a 285 E

####################################### 
"ORGANIZACION DE LAS VARIABLES\
YA QUE VAN DEBEN IR EN CORDENADAS ESTE"
####################################### 

speed = np.sqrt(v*v+u*u)

################### 
"MAPAS VIENTOS"
####################
box_TT_lon = [-96.25, -96.25, -93.75, -93.75, -96.25]
box_TT_lat = [16, 12.5, 12.5, 16, 16]
box_PP_lon = [-90.5, -90.5, -86.0, -86.0, -90.5]
box_PP_lat = [11.75, 8.75, 8.75, 11.75, 11.75]
box_PN_lon = [-80.75, -80.75, -78.75, -78.75, -80.75]
box_PN_lat = [8.5, 5.5, 5.5, 8.5, 8.5]
lons,lats = np.meshgrid(Lon,Lat)
fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=24, llcrnrlon=-105, urcrnrlon=-75, resolution='i')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 24, 8),labels=[1,0,0,1])
map.drawmeridians(np.arange(-105,-75,10),labels=[1,0,0,1])
x,y = map(lons,lats)
TT_lon,TT_lat = map(box_TT_lon, box_TT_lat)
PP_lon,PP_lat = map(box_PP_lon, box_PP_lat)
PN_lon,PN_lat = map(box_PN_lon, box_PN_lat)
CF = map.contourf(x,y,speed[24,:,:], np.linspace(0, 23, 20), extend='both', cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow
cb = map.colorbar(CF, size="5%", pad="2%", extendrect = 'True', drawedges = 'True', format='%.1f')
cb.set_label('m/s')
Q = map.quiver(x[::2,::2], y[::2,::2], u[24,::2,::2], v[24,::2,::2], scale=400)
plt.quiverkey(Q, 0.95, 0.05, 10, '10 m/s' )
ax.set_title('$NARR$ $DOMAIN$', size='15')
map.plot(TT_lon, TT_lat, marker=None, color='k', linewidth = 1.6)
map.plot(PP_lon, PP_lat, marker=None, color='k', linewidth = 1.6)
map.plot(PN_lon, PN_lat, marker=None, color='k', linewidth = 1.6)   
map.fillcontinents(color='white')
plt.show()
