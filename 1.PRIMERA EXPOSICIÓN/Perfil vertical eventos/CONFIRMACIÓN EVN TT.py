from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import netCDF4 as nc
import numpy as np


#################### 
"LECTURA DE DATOS"
#################### 

Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/PERFIL_DE_EVENTOS_DE_VIENTOS/EVENTO_TEHUANTEPEC.nc')
v_e = Archivo.variables['v'][:, :, 24:, 60:181]
u_e = Archivo.variables['u'][:, :, 24:, 60:181]
level = Archivo.variables["level"][:]
           
V = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO V a 10 m (promedio mensual).nc')
U = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO U a 10 m (promedio mensual).nc')
v = V.variables["v10"][:, 24:, 60:181]
u = U.variables["u10"][:, 24:, 60:181]
Lat = V.variables["latitude"][24:] # Se recorta de una vez el arreglo de latitudes de 0 a 24 N
Lon = V.variables["longitude"][60:181] # Se recorta de una vez el arreglo de longitudes de 255 E a 285 E

####################################### 
"ORGANIZACION DE LAS VARIABLES\
YA QUE VAN DEBEN IR EN CORDENADAS ESTE"
####################################### 

Lon = Lon-360

######################## 
"CICLO ANUAL DE VIENTOS"
########################

cic_an_u = np.zeros((12,97,121))
cic_an_v = np.zeros((12,97,121))

for i in range(12):
    for j in range(97):
        for k in range(121):
            cic_an_u[i,j,k] = np.mean(u[i::12,j,k])
            cic_an_v[i,j,k] = np.mean(v[i::12,j,k])
            
            
############################
"MEDIA NOV Y DIC DE VIENTOS"
############################

med_ND_u = np.zeros((97, 121))
med_ND_v = np.zeros((97, 121))

for j in range(97):
    for k in range(121):
        med_ND_u[j,k] = np.mean(cic_an_u[10:12,j,k])
        med_ND_v[j,k] = np.mean(cic_an_v[10:12,j,k])

################################################
"ANOMALÍA DE VIENTOS DEL EVENTO A NIVEL DEL MAR"
################################################

an_u_evn = np.zeros((6,97,121))
an_v_evn = np.zeros((6,97,121))

for i in range(6):
    for j in range(97):
        for k in range(121):
            an_u_evn[i,j,k] = u_e[i,36,j,k]-med_ND_u[j,k]
            an_v_evn[i,j,k] = v_e[i,36,j,k]-med_ND_v[j,k]

##########################################
"MEDIA DE ANOMALÍAS DE VIENTOS DEL EVENTO"
##########################################

med_an_u_evn = np.zeros((97,121))
med_an_v_evn = np.zeros((97,121))

for i in range(97):
    for j in range(121):
        med_an_u_evn[i,j] = np.mean(an_u_evn[:,i,j])
        med_an_v_evn[i,j] = np.mean(an_v_evn[:,i,j])








################################
"VELOCIDAD DE VIENTOS 1979-2016"
################################

spd = np.sqrt(u*u+v*v)

#####################################
"CICLO ANUAL DE VELOCIDAD DE VIENTOS"
#####################################

cic_an_spd = np.zeros(((12, 97, 121)))

for i in range(12):
    for j in range(97):
        for k in range(121):
            cic_an_spd[i,j,k] = np.mean(spd[i::12,j,k])
            
#########################################
"MEDIA NOV Y DIC DE VELOCIDAD DE VIENTOS"
#########################################

med_ND_spd = np.zeros((97, 121))

for j in range(97):
    for k in range(121):
        med_ND_spd[j,k] = np.mean(cic_an_spd[10:12,j,k])

#############################################################
"ANOMALÍA DE VELOCIDAD DE VIENTOS DEL EVENTO A NIVEL DEL MAR"
#############################################################

spd_evn = np.sqrt(u_e[:6,36,:,:]*u_e[:6,36,:,:]+v_e[:6,36,:,:]*v_e[:6,36,:,:]) #Velocidad del evento a nivel del mar

an_spd_evn = np.zeros((6,97,121))

for i in range(6):
    for j in range(97):
        for k in range(121):
            an_spd_evn[i,j,k] = spd_evn[i,j,k]-med_ND_spd[j,k]

##########################################################
"PROMEDIO DE ANOMALÍAS DE VELOCIDAD DE VIENTOS DEL EVENTO"
##########################################################

me_an_spd_evn = np.zeros((97,121))

for i in range(97):
    for j in range(121):
        me_an_spd_evn[i,j] = np.mean(an_spd_evn[:,i,j])





###################
"MAPA DE ANOMALÍAS"
###################

box_TT_lon = [-97, -97, -93.3, -93.3, -97]
box_TT_lat = [15.9, 11.7, 11.7, 15.9, 15.9]
lons,lats = np.meshgrid(Lon,Lat)
fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=24, llcrnrlon=-105, urcrnrlon=-75, resolution='i')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 30, 8),labels=[1,0,0,1])
map.drawmeridians(np.arange(-120,-60,15),labels=[1,0,0,1])
x, y = map(lons,lats)
x1, y1 = map(-94.5, 19.25)
x2, y2 = map(-94.75, 17.25)
x3, y3 = map(-94.75, 15)
TT_lon,TT_lat = map(box_TT_lon, box_TT_lat)
CF = map.contourf(x,y, me_an_spd_evn[:,:], np.linspace(0, 14, 20), extend='both', cmap=plt.cm.RdYlBu_r )#plt.cm.rainbow, plt.cm.RdYlBu_r    
cb = map.colorbar(CF, size="5%", pad="2%", extendrect = 'True', drawedges = 'True', format='%.1f')
cb.set_label('m/s')
Q = map.quiver(x[::2,::2], y[::2,::2], med_an_u_evn[::2,::2], med_an_v_evn[::2,::2], scale=300)
plt.quiverkey(Q, 0.95, 0.05, 10, '10 m/s' )
ax.set_title('$Anomalia$ $media$ $del$ $evento-Tehuantepec-(Nov/2002)$', size='15')
map.plot(TT_lon, TT_lat, marker=None, color='k')
map.plot(x1, y1, marker='D', color='m')
map.plot(x2, y2, marker='D', color='m')
map.plot(x3, y3, marker='D', color='m')   
map.fillcontinents(color='white')
plt.show()

