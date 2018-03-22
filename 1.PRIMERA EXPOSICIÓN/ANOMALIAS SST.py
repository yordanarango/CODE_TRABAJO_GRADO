from mpl_toolkits.basemap import Basemap
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

################## 
"LECTURA DE DATOS"
################## 
           
T = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SST (promedio mensual).nc')
t = T.variables['sst'][:, 24:, 60:181]
Lat = T.variables["latitude"][24:] # Se recorta de una vez el arreglo de latitudes de 0 a 24 N
Lon = T.variables["longitude"][60:181] # Se recorta de una vez el arreglo de longitudes de 255 E a 285 E

####################################### 
"ORGANIZACION DE LAS VARIABLES\
YA QUE DEBEN IR EN CORDENADAS ESTE"
####################################### 

Lon = Lon-360

#################### 
"CICLO ANUAL DE SST"
#################### 

cic_an_T = np.zeros((12,97,121))

for i in range(12):
    for j in range(97):
        for k in range(121):
            cic_an_T[i,j,k] = np.mean(t[i::12,j,k])


####################### 
"MEDIA INVERNAL DE SST"
####################### 

med_NDEFM_T = np.zeros((97, 121))

for j in range(97):
    for k in range(121):
        med_NDEFM_T[j,k] = (cic_an_T[10,j,k]+cic_an_T[11,j,k]+cic_an_T[0,j,k]+cic_an_T[1,j,k]+cic_an_T[2,j,k])/5

################################# 
"MEDIA MULTIANUAL DE SST MENSUAL"
#################################

med_manual_T = np.zeros((97, 121))

for i in range(97):
    for j in range(121):
        med_manual_T[i,j] = np.mean(t[:,i,j])

########################### 
"ANOMALÍAS DE SST INVERNAL"
###########################

anom_NDEFM_T = med_NDEFM_T-med_manual_T

############# 
"MAPA DE SST"
#############

#box_TT_lon = [-96.5, -96.5, -93.75, -93.75, -96.5]
#box_TT_lat = [16, 12.5, 12.5, 16, 16]
#box_PP_lon = [-91, -91, -86.25, -86.25, -91]
#box_PP_lat = [11.5, 8, 8, 11.5, 11.5]
#box_PN_lon = [-80, -80, -78, -78, -80]
#box_PN_lat = [8.5, 5, 5, 8.5, 8.5]
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
CF = map.contourf(x,y,anom_NDEFM_T[:,:], np.linspace(-2, 2, 25), cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow
cb = plt.colorbar(CF, orientation='horizontal', pad=0.05, shrink=0.8, boundaries= np.linspace(-2, 2, 25))
#cb = map.colorbar(CF, size="5%", pad="2%", extendrect = 'True', drawedges = 'True', format='%.1f')
cb.set_label('$C$')
ax.set_title('$SST$ $-$ $Winter$ $Anomalies$', size='15')
map.plot(TT_lon, TT_lat, marker=None, color='k')
map.plot(PP_lon, PP_lat, marker=None, color='k')
map.plot(PN_lon, PN_lat, marker=None, color='k')    
plt.show()

