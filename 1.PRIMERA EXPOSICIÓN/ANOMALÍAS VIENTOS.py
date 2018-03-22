from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.colors as colors

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y)) 

#################### 
"LECTURA DE DATOS"
#################### 
           
V = nc.Dataset('/home/yordan/YORDAN/UNAL/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO V a 10 m (promedio mensual).nc')
U = nc.Dataset('/home/yordan/YORDAN/UNAL/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO U a 10 m (promedio mensual).nc')
v = V.variables["v10"][:, 24:, 60:181]
u = U.variables["u10"][:, 24:, 60:181]
Lat = V.variables["latitude"][24:] # Se recorta de una vez el arreglo de latitudes de 0 a 24 N
Lon = V.variables["longitude"][60:181] # Se recorta de una vez el arreglo de longitudes de 255 E a 285 E

####################################### 
"ORGANIZACION DE LAS VARIABLES\
YA QUE VAN DEBEN IR EN CORDENADAS ESTE"
####################################### 

Lon = Lon-360

##############################################################################
##############################################################################
##                   PARA LECTURA DE DATOS DIARIOS                          ##
##                                                                          ##
##    Ya que la cantidad de datos a ingresar en las variables v y u es muy  ##
##    grande, la siguiente, es otra forma de ingresar los datos a dichas    ##
##    variables sin que el computador sufra o se toste.                     ##
##    El procedimiento se basa en el ingreso de las matrices pero por grupos##
##    de 1000 matrices, de manera que el trabajo de ingresar la información ##
##    se hace de manera dosificada y no tan abruptamente.                   ##
##                                                                          ##
##  v = np.zeros((13635,121,241))                                           ##
##  u = np.zeros((13635,121,241))                                           ##
##  a = np.array((1000,  2000,  3000,  4000,  5000,  6000,  7000,  8000,    ##
##                9000, 10000, 11000, 12000, 13000, 13635))                 ##   
##  for i, j in enumerate(a):                                               ##
##      v[i*1000:j,:,:]= V.variables["v10"][i*1000:j]                       ##
##      u[i*1000:j,:,:]= U.variables["u10"][i*1000:j]                       ##
##                                                                          ##
##############################################################################
##############################################################################

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
            
########################### 
"MEDIA INVERNAL DE VIENTOS"
###########################

med_NDEFM_u = np.zeros((97, 121))
med_NDEFM_v = np.zeros((97, 121))

for j in range(97):
    for k in range(121):
        med_NDEFM_u[j,k] = (cic_an_u[10,j,k]+cic_an_u[11,j,k]+cic_an_u[0,j,k]+cic_an_u[1,j,k]+cic_an_u[2,j,k])/5
        med_NDEFM_v[j,k] = (cic_an_v[10,j,k]+cic_an_v[11,j,k]+cic_an_v[0,j,k]+cic_an_v[1,j,k]+cic_an_v[2,j,k])/5
        
####################################### 
"MEDIA MULTIANUAL DE VIENTOS MENSUALES"
#######################################

med_manual_u = np.zeros((97, 121))
med_manual_v = np.zeros((97, 121))

for i in range(97):
    for j in range(121):
        med_manual_u[i,j] = np.mean(u[:,i,j])
        med_manual_v[i,j] = np.mean(v[:,i,j])

################################# 
"ANOMALÍAS DE VIENTOS INVERNALES"
#################################

anom_NDEFM_u = med_NDEFM_u-med_manual_u
anom_NDEFM_v = med_NDEFM_v-med_manual_v

##################################### 
"CICLO ANUAL DE VELOCIDAD DE VIENTOS"
#####################################

spd = np.sqrt(u*u+v*v)

cic_an_speed = np.zeros((12, 97, 121))

for i in range(12):
    for j in range(97):
        for k in range(121):
            cic_an_speed[i,j,k] = np.mean(spd[i::12,j,k])

######################################## 
"MEDIA INVERNAL DE VELOCIDAD DE VIENTOS"
########################################

med_NDEFM_speed = np.zeros((97, 121))

for i in range(97):
    for j in range(121):
        med_NDEFM_speed[i,j] = (cic_an_speed[10,i,j]+cic_an_speed[11,i,j]+cic_an_speed[0,i,j]+cic_an_speed[1,i,j]+cic_an_speed[2,i,j])/5 
        
#################################################### 
"MEDIA MULTIANUAL DE VELOCIDAD DE VIENTOS MENSUALES"
####################################################

med_manual_speed = np.zeros((97, 121))

for i in range(97):
    for j in range(121):
        med_manual_speed[i,j] = np.mean(spd[:,i,j])

############################################### 
"ANOMALÍAS DE VELOCIDAD DE VIENTOS INVERNALES"
###############################################

anom_NDEFM_speed = med_NDEFM_speed-med_manual_speed

################### 
"MAPAS VIENTOS"
####################
p_TT_lon = -95.0
p_PP_lon = -87.5
p_PN_lon = -79.75
p_TT_lat = 14.5
p_PP_lat = 10.25
p_PN_lat = 7.5

box_TT_lon = [-96.25, -96.25, -93.75, -93.75, -96.25]
box_TT_lat = [16, 12.5, 12.5, 16, 16]
box_PP_lon = [-90.5, -90.5, -86.0, -86.0, -90.5]
box_PP_lat = [11.75, 8.75, 8.75, 11.75, 11.75]
box_PN_lon = [-80.75, -80.75, -78.75, -78.75, -80.75]
box_PN_lat = [8.5, 5.5, 5.5, 8.5, 8.5]

fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])

map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=24, llcrnrlon=-105, urcrnrlon=-75, resolution='i')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 24, 8),labels=[1,0,0,1])
map.drawmeridians(np.arange(-105,-75,10),labels=[1,0,0,1])

lons,lats = np.meshgrid(Lon,Lat)
x,y = map(lons,lats)
P_TT_lon, P_TT_lat = map(p_TT_lon, p_TT_lat) 
P_PP_lon, P_PP_lat = map(p_PP_lon, p_PP_lat)  
P_PN_lon, P_PN_lat = map(p_PN_lon, p_PN_lat)   
TT_lon,TT_lat = map(box_TT_lon, box_TT_lat)
PP_lon,PP_lat = map(box_PP_lon, box_PP_lat)
PN_lon,PN_lat = map(box_PN_lon, box_PN_lat)

bounds=np.linspace( np.min(anom_NDEFM_speed) ,np.max(anom_NDEFM_speed),20) 
bounds=np.around(bounds, decimals=2) 
CF = map.contourf(x,y,anom_NDEFM_speed[:,:], 20, norm=MidpointNormalize(midpoint=0), cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow
cb = plt.colorbar(CF, orientation='horizontal', pad=0.05, shrink=0.8, boundaries=bounds)
cb.set_label('m/s')
Q = map.quiver(x[::2,::2], y[::2,::2], anom_NDEFM_u[::2,::2], anom_NDEFM_v[::2,::2], scale=150)
plt.quiverkey(Q, 0.93, 0.05, 10, '10 m/s' )
ax.set_title('$Wind$ $Field$ $-$ $Winter$ $Anomalies$', size='15')

#map.plot(P_TT_lon, P_TT_lat, marker='D', color='w')
#map.plot(P_PP_lon, P_PP_lat, marker='D', color='w')
#map.plot(P_PN_lon, P_PN_lat, marker='D', color='w')
map.plot(TT_lon, TT_lat, marker=None, color='k')
map.plot(PP_lon, PP_lat, marker=None, color='k')
map.plot(PN_lon, PN_lat, marker=None, color='k')      
map.fillcontinents(color='white')
plt.show()
