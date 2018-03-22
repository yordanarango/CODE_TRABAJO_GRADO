import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc

############# 
"HOVMOLLER"
#############

Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/PERFIL_DE_EVENTOS_DE_VIENTOS/EVENTO_TEHUANTEPEC.nc')

v_e1 = Archivo.variables['v'][0:6, 19:, 43, 102]
v_e2 = Archivo.variables['v'][0:6, 19:, 51, 101]
v_e3 = Archivo.variables['v'][0:6, 19:, 60, 101]

u_e1 = Archivo.variables['u'][0:6, 19:, 43, 102]
u_e2 = Archivo.variables['u'][0:6, 19:, 51, 101]
u_e3 = Archivo.variables['u'][0:6, 19:, 60, 101]

spd1 = np.sqrt(v_e1*v_e1+u_e1*u_e1)
spd2 = np.sqrt(v_e2*v_e2+u_e2*u_e2)
spd3 = np.sqrt(v_e3*v_e3+u_e3*u_e3)

lat = Archivo.variables['latitude'][:]
lon = Archivo.variables['longitude'][:]
level = Archivo.variables["level"][19:]
time = np.arange(17,23)

x,y = np.meshgrid(time, level)

evn_TT1 = np.zeros((18,6))
evn_TT2 = np.zeros((18,6))
evn_TT3 = np.zeros((18,6))
for i in range(6):
    evn_TT1[:,i] = spd1[i,:]    
    evn_TT2[:,i] = spd2[i,:]    
    evn_TT3[:,i] = spd3[i,:]
    
    
fig = plt.figure(figsize=(10,5), edgecolor='W',facecolor='W')
ax1 = fig.add_axes([0.0,0.1,0.27,0.75])
ax2 = fig.add_axes([0.32,0.1,0.27,0.75])
ax3 = fig.add_axes([0.64,0.1,0.27,0.75])
ax4 = fig.add_axes([0.95,0.1,0.03,0.75])

cd = ax1.contourf(x, y, evn_TT1, np.linspace(0,30, 18), cmap=plt.cm.rainbow)
#ax1.contour(x,y, evn_TT1, np.linspace(0,35,10))
ca = plt.colorbar(cd, cax=ax4, drawedges = 'True',format='%.1f')
ca.set_label('m/s')
ax1.set_title('$Caribe$', size='13')
ax1.set_ylabel('$Altura$ $(mbar)$', size='15')
ax1.invert_yaxis()


ce = ax2.contourf(x, y, evn_TT2, np.linspace(0,30, 18), cmap=plt.cm.rainbow)
#ax2.contour(x,y, evn_TT2, np.linspace(0,35,10))
ax2.set_title('$En$ $tierra$', size='13')
ax2.set_xlabel('$Noviembre-2002-$ $(dia)$', size='15')
ax2.invert_yaxis()


cf = ax3.contourf(x, y, evn_TT3, np.linspace(0,30, 18), cmap=plt.cm.rainbow)
#ax1.contour(X,Y, evn_TT3, np.linspace(0,35,10))
ax3.set_title('$Pacifico$', size='13')
ax3.invert_yaxis()

plt.suptitle('$Perfil$ $vertical$ $de$ $vientos$ $(Tehuantepec)$', x=0.45, fontsize=17)
plt.show()