from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc

wnd_tehuantepec = genfromtxt('/home/yordan/YORDAN/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/tehuantepec_wind_data.txt', delimiter=',')
wnd_papagayo = genfromtxt('/home/yordan/YORDAN/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/papagayo_wind_data.txt', delimiter=',')
wnd_panama = genfromtxt('/home/yordan/YORDAN/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTOS_RASI/papagayo_wind_data.txt', delimiter=',')               

V = nc.Dataset('/home/yordan/YORDAN/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO V a 10 m.nc')
U = nc.Dataset('/home/yordan/YORDAN/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO U a 10 m.nc')

v_TT = np.zeros((4383,15,11)) # Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de tehuantepec 
u_TT = np.zeros((4383,15,11)) # Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de tehuantepec
v_PP = np.zeros((4383,13,19)) # Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de papagayo 
u_PP = np.zeros((4383,13,19)) # Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de papagayo
v_PN = np.zeros((4383,13,9)) # Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de panama 
u_PN = np.zeros((4383,13,9)) # Se escogen los datos para el período 1998-2009, para la zona de promedio de vientos de panama

af = np.array((1000,  2000,  3000,  4000,  4383))   

for i, j in enumerate(af):
    v_TT[i*1000:j,:,:]= V.variables["v10"][i*1000:j, 56:71, 95:106]
    u_TT[i*1000:j,:,:]= U.variables["u10"][i*1000:j, 56:71, 95:106] 
    v_PP[i*1000:j,:,:]= V.variables["v10"][i*1000:j, 73:86,118:137]
    u_PP[i*1000:j,:,:]= U.variables["u10"][i*1000:j, 73:86,118:137]
    v_PN[i*1000:j,:,:]= V.variables["v10"][i*1000:j, 86:99,157:166]
    u_PN[i*1000:j,:,:]= U.variables["u10"][i*1000:j, 86:99,157:166]

spd_TT = np.sqrt(v_TT*v_TT+u_TT*u_TT)
spd_PP = np.sqrt(v_PP*v_PP+u_PP*u_PP)
spd_PN = np.sqrt(v_PN*v_PN+u_PN*u_PN)

###################################
"PROMEDIOS DE LAS ZONAS TT, PP, PN"
###################################

med_spd_TT = np.zeros(4383)
med_spd_PP = np.zeros(4383)
med_spd_PN = np.zeros(4383)

for i in range(4383):
    med_spd_TT[i] = np.mean(spd_TT[i,:,:])
    med_spd_PP[i] = np.mean(spd_PP[i,:,:])
    med_spd_PN[i] = np.mean(spd_PN[i,:,:])

#####################
"EVENTOS TEHUANTEPEC"
#####################
         
evns_tehuantepec = 0
pos_evns_tehuantepec = []
b = np.zeros(28)

for a in range(28):
    if wnd_tehuantepec[a] != 0:
        evns_tehuantepec = evns_tehuantepec+1
        pos_evns_tehuantepec.append(a)
    if evns_tehuantepec == 1:
        break

for i in range(len(wnd_tehuantepec)):
   if i < len(wnd_tehuantepec)-28:
        if wnd_tehuantepec[i+28] != 0:
            if np.all(wnd_tehuantepec[i:i+28] == b) == True:
                evns_tehuantepec = evns_tehuantepec+1
                pos_evns_tehuantepec.append(i+28)

pos_tehuantepec = np.array((pos_evns_tehuantepec)) #conviertiendo la lista de posiciones en un arreglo de numpy

#########                     ###########
         "EVENTOS PAPAGAYO"
#########                     ###########
evns_papagayo = 0
pos_evns_papagayo = []
b = np.zeros(28)

for a in range(28):
    if wnd_papagayo[a] != 0:
        evns_papagayo = evns_papagayo+1
        pos_evns_papagayo.append(a)
    if evns_papagayo == 1:
        break
        
for i in range(len(wnd_papagayo)):
   if i < len(wnd_papagayo)-28:
        if wnd_papagayo[i+28] != 0:
            if np.all(wnd_papagayo[i:i+28] == b) == True:
                evns_papagayo = evns_papagayo+1
                pos_evns_papagayo.append(i+28)

pos_papagayo = np.array((pos_evns_papagayo)) #conviertiendo la lista de posiciones en un arreglo de numpy
                

#########                     ###########
         "EVENTOS PANAMA"
#########                     ###########
evns_panama = 0
pos_evns_panama = [] 
b = np.zeros(28)

for a in range(28):
    if wnd_panama[a] != 0:
        evns_panama = evns_panama+1
        pos_evns_panama.append(a)
    if evns_panama == 1:
        break
        
for i in range(len(wnd_panama)): 
   if i < len(wnd_panama)-28:
        if wnd_panama[i+28] != 0:
            if np.all(wnd_panama[i:i+28] == b) == True:
                evns_panama = evns_panama+1
                pos_evns_panama.append(i+28)

pos_panama = np.array((pos_evns_panama)) #conviertiendo la lista de posiciones en un arreglo de numpy










xc = np.zeros(len(pos_tehuantepec)+len(pos_papagayo)+len(pos_panama))

xc[0:len(pos_tehuantepec)] = pos_tehuantepec
xc[len(pos_tehuantepec):len(pos_papagayo)+len(pos_tehuantepec)] = pos_papagayo
xc[len(pos_papagayo)+len(pos_tehuantepec):len(pos_panama)+len(pos_papagayo)+len(pos_tehuantepec)] = pos_panama

zxc = np.sort(xc)

bnm = []
l = 0
while l < (len(zxc)-(3)):
    if (zxc[l+1]-zxc[l])<28 and (zxc[l+2]-zxc[l])<28:
        bnm.append((zxc[l], zxc[l+1], zxc[l+2]))
        l = l+3
    elif (zxc[l+1]-zxc[l])<28 and (zxc[l+2]-zxc[l])>=28:
        bnm.append((zxc[l], zxc[l+1], 99999))
        l = l+2
    else:
        bnm.append((zxc[l], 99999, 99999))
        l = l +1

eventos = np.array((bnm))



fig = plt.figure(figsize = (6,12))

ax1 = fig.add_subplot(311)
ax1.set_xlim([0,6])
ax1.set_ylim([0,20])
ax1.set_ylabel('$Velocidad$ $(m/s)$', size='13')

ax2 = fig.add_subplot(312)
ax2.set_xlim([0,7])
ax2.set_ylim([0,15])
ax2.set_ylabel('$Velocidad$ $(m/s)$', size='13')

ax3 = fig.add_subplot(313)
ax3.set_xlim([0,14])
ax3.set_ylim([0,12])
ax3.set_xlabel('$dia$', size= '15')
ax3.set_ylabel('$Velocidad$ $(m/s)$',size='13')

for i,j in enumerate(eventos):
    if np.any(pos_tehuantepec == j[0]) == True:
        pos1 = j[0]/4 #como j[i] da un npumero de tipo entero, la división es una división entera
        ttpc = med_spd_TT[pos1:pos1+7]
        ax1.plot(ttpc, color='gray')
        if j[1] == 99999:
            pass
        else:
            if np.any(pos_papagayo == j[1]) == True:
                pos2 = j[1]/4                
                pgyo = med_spd_PP[pos2:pos2+7]
                ax2.plot(np.arange(pos2-pos1, pos2-pos1+7),pgyo, color='b')
                if j[2] == 99999:
                    pass
                else:
                    pos3 = j[2]/4                    
                    pnma = med_spd_PN[pos3:pos3+7]
                    ax3.plot(np.arange(pos3-pos1, pos3-pos1+7),pnma, color='g')                           
            else:
                pos2 = j[1]/4
                pnma = med_spd_PN[pos2:pos2+7]
                ax2.plot(np.arange(pos2-pos1, pos2-pos1+7),pnma, color='g')
                if j[2] == 99999:
                    pass
                else:
                    pos3 = j[2]/4
                    pgyo = med_spd_PP[pos3:pos3+7]
                    ax3.plot(np.arange(pos3-pos1, pos3-pos1+7),pgyo, color='b')
    elif np.any(pos_papagayo == j[0]) == True:
        pos1 = j[0]/4        
        pgyo = med_spd_PP[pos1:pos1+7]
        ax1.plot(pgyo, color='b')
        if j[1] == 99999:
            pass
        else:         
            if np.any(pos_panama == j[1]) == True:
                pos2 = j[1]/4
                pnma = med_spd_PN[pos2:pos2+7]
                ax2.plot(np.arange(pos2-pos1, pos2-pos1+7),pnma, color='g')
                if j[2] == 99999:
                    pass
                else:
                    pos3 = j[2]/4                    
                    ttpc = med_spd_TT[pos3:pos3+7]
                    ax3.plot(np.arange(pos3-pos1, pos3-pos1+7),ttpc, color='gray')                           
            else:
                pos2 = j[1]/4
                ttpc = med_spd_TT[pos2:pos2+7]
                ax2.plot(np.arange(pos2-pos1, pos2-pos1+7),ttpc, color='gray')
                if j[2] == 99999:
                    pass
                else:
                    pos3 = j[2]/4
                    pnma = med_spd_PN[pos3:pos3+7]
                    ax3.plot(np.arange(pos3-pos1, pos3-pos1+7),pnma, color='g')
    else:
        pos1 = j[0]/4
        pnma = med_spd_PN[pos1:pos1+7]
        ax1.plot(pnma, color='g')
        if j[1] == 99999:
            pass
        else:
            if np.any(pos_tehuantepec == j[1]) == True:
                pos2 = j[1]/4                    
                ttpc = med_spd_TT[pos2:pos2+7]
                ax2.plot(np.arange(pos2-pos1, pos2-pos1+7),ttpc, color='gray')
                if j[2] == 99999:
                    pass
                else:
                    pos3 = j[2]/4                    
                    pgyo = med_spd_PP[pos3:pos3+7]
                    ax3.plot(np.arange(pos3-pos1, pos3-pos1+7),pgyo, color='b')
            else:
                pos2 = j[1]/4
                pgyo = med_spd_PP[pos2:pos2+7]
                ax2.plot(np.arange(pos2-pos1, pos2-pos1+7),pgyo, color='b')
                if j[2] == 99999:
                    pass
                else:
                    pos3 = j[2]/4                    
                    ttpc = med_spd_TT[pos3:pos3+7]
                    ax3.plot(np.arange(pos3-pos1, pos3-pos1+7),ttpc, color='gray')

ax1.plot(0, 21, color='gray', label = 'TT')
ax1.plot(0, 21, color='b', label = 'PP')
ax1.plot(0, 21, color='g', label = 'PN')
ax2.plot(0, 21, color='gray', label = 'TT')
ax2.plot(0, 21, color='b', label = 'PP')
ax2.plot(0, 21, color='g', label = 'PN')
ax3.plot(0, 21, color='gray', label = 'TT')
ax3.plot(0, 21, color='b', label = 'PP')
ax3.plot(0, 21, color='g', label = 'PN')

ax1.legend(loc='best')
ax2.legend(loc='best')
ax3.legend(loc='best')

ax1.set_title('$Activacion$ $del$ $evento$', size='13')
ax2.set_title('$Activacion$ $segundo$ $chorro$', size='13')
ax3.set_title('$Activacion$ $tercer$ $chorro$', size='13')