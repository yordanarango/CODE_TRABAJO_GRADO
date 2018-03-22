from mpl_toolkits.basemap import Basemap
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
 
#######################
"""LECTURA DE DATOS"""
#######################
           
V = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO V a 10 m (promedio mensual).nc')
U = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/VIENTO U a 10 m (promedio mensual).nc')
v_TT = V.variables["v10"][:,56:71,95:106]
u_TT = U.variables["u10"][:,56:71,95:106]
v_PP = V.variables["v10"][:,73:86,118:137]
u_PP = U.variables["u10"][:,73:86,118:137]
v_PN = V.variables["v10"][:,86:99,157:166]
u_PN = U.variables["u10"][:,86:99,157:166]

Lat = V.variables["latitude"][:] 
Lon = V.variables["longitude"][:] 
Lon = Lon-360

#####################################
"""VELOCIDAD DE VIENTOS TT, PP, PN"""
##################################### 

spd_TT = np.sqrt(v_TT*v_TT+u_TT*u_TT)
spd_PP = np.sqrt(v_PP*v_PP+u_PP*u_PP)
spd_PN = np.sqrt(v_PN*v_PN+u_PN*u_PN)

#####################################
"""COMPOSITE DE VIENTOS TT, PP, PN"""
#####################################
           
speed_TT = np.zeros(448)
speed_PP = np.zeros(448)
speed_PN = np.zeros(448)

for i in range(448):
    speed_TT[i] = np.mean(spd_TT[i,:,:])
    speed_PP[i] = np.mean(spd_PP[i,:,:])
    speed_PN[i] = np.mean(spd_PN[i,:,:])
    
####################################################
"""CICLO ANUAL DE VELOCIDAD DE VIENTOS TT, PP, PN"""
#################################################### 

cic_speed_TT = np.zeros(12) 
cic_speed_PP = np.zeros(12) 
cic_speed_PN = np.zeros(12) 

for i in range(12):
    cic_speed_TT[i] = np.mean(speed_TT[i::12])
    cic_speed_PP[i] = np.mean(speed_PP[i::12]) 
    cic_speed_PN[i] = np.mean(speed_PN[i::12]) 

#########################################################
"""MEDIA MULTIANUAL DE VELOCIDAD DE VIENTOS TT, PP, PN"""
######################################################### 

med_manual_sp_TT = np.mean(speed_TT)
med_manual_sp_PP = np.mean(speed_PP)
med_manual_sp_PN = np.mean(speed_PN)

##############################################################
"""CICLO ANUAL DE ANOMALÍAS VELOCIDAD DE VIENTOS TT, PP, PN"""
##############################################################

ano_sp_TT = cic_speed_TT-med_manual_sp_TT
ano_sp_PP = cic_speed_PP-med_manual_sp_PP
ano_sp_PN = cic_speed_PN-med_manual_sp_PN

##############################################################
"""CICLO ANUAL DE MAX Y MIN VELOCIDAD DE VIENTOS TT, PP, PN"""
############################################################## 

Mm_sp_TT = np.zeros((12,2))
Mm_sp_PP = np.zeros((12,2))
Mm_sp_PN = np.zeros((12,2))

for i in range(12):
    Mm_sp_TT[i,0] = np.max(speed_TT[i::12])
    Mm_sp_TT[i,1] = np.min(speed_TT[i::12])
    Mm_sp_PP[i,0] = np.max(speed_PP[i::12])
    Mm_sp_PP[i,1] = np.min(speed_PP[i::12])
    Mm_sp_PN[i,0] = np.max(speed_PN[i::12])
    Mm_sp_PN[i,1] = np.min(speed_PN[i::12])

#####################################################################
"""CICLO ANUAL DE MAX ANOMALÍAS DE VELOCIDAD DE VIENTOS TT, PP, PN"""
##################################################################### 

ano_Mm_sp_TT = Mm_sp_TT-med_manual_sp_TT
ano_Mm_sp_PP = Mm_sp_PP-med_manual_sp_PP
ano_Mm_sp_PN = Mm_sp_PN-med_manual_sp_PN

ano_maxsp_TT = np.zeros(12)
ano_maxsp_PP = np.zeros(12)
ano_maxsp_PN = np.zeros(12)

for i in range(12):
    if abs(ano_Mm_sp_TT[i,0]) >= abs(ano_Mm_sp_TT[i,1]):
        ano_maxsp_TT[i] = ano_Mm_sp_TT[i,0]
    else:
        ano_maxsp_TT[i] = ano_Mm_sp_TT[i,1]

for i in range(12):
    if abs(ano_Mm_sp_PP[i,0]) >= abs(ano_Mm_sp_PP[i,1]):
        ano_maxsp_PP[i] = ano_Mm_sp_PP[i,0]
    else:
        ano_maxsp_PP[i] = ano_Mm_sp_PP[i,1]


for i in range(12):
    if abs(ano_Mm_sp_PN[i,0]) >= abs(ano_Mm_sp_PN[i,1]):
        ano_maxsp_PN[i] = ano_Mm_sp_PN[i,0]
    else:
        ano_maxsp_PN[i] = ano_Mm_sp_PN[i,1]



fig = plt.figure(figsize=(7,4.8))
ax = fig.add_subplot(111)
ax.bar((0,1,2,3,4,5,6,7,8,9,10,11), ano_maxsp_PN, width=1.0, color='#0489B1', label='Max')
ax.bar((0,1,2,3,4,5,6,7,8,9,10,11), ano_sp_PN, width=1.0, color='#0431B4', label='Mean')
my_xticks = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.xticks((0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5),my_xticks)
ax.set_xlabel('$Month$', size='15')
ax.set_ylabel('$Speed$ $Anomalies$ $(m/s)$', size='15')
ax.legend(loc='best')
ax.set_ylim(ano_maxsp_PN.min()-0.5, ano_maxsp_PN.max()+0.5)
ax.set_title(u'$Annual$ $Cycle$ $of$ $Winds$ $Anomalies$ $(Panamá)$', size='15')

