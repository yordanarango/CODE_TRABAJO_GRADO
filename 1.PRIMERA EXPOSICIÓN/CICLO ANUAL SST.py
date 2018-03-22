# -*- coding: utf-8 -*-
from mpl_toolkits.basemap import Basemap
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

################## 
"LECTURA DE DATOS"
################## 
           
T = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SST (promedio mensual).nc')
T_TT = T.variables['sst'][:, 56:71, 94:106]
T_PP = T.variables['sst'][:, 74:89, 116:136]
T_PN = T.variables['sst'][:, 86:101, 160:169]


Lat = T.variables["latitude"][:]
Lon = T.variables["longitude"][:]
Lon = Lon-360

##############################
"COMPOSITE DE SST TT, PP, PN"
############################## 

TTT = np.zeros(448)
TPP = np.zeros(448)
TPN = np.zeros(448)

for i in range(448):
    TTT[i] = np.mean(T_TT[i,:,:])
    TPP[i] = np.mean(T_PP[i,:,:])
    TPN[i] = np.mean(T_PN[i,:,:])
    
############################### 
"CICLO ANUAL DE SST TT, PP, PN"
############################### 

cic_T_TT = np.zeros(12) 
cic_T_PP = np.zeros(12) 
cic_T_PN = np.zeros(12) 

for i in range(12):
    cic_T_TT[i] = np.mean(TTT[i::12])
    cic_T_PP[i] = np.mean(TPP[i::12])
    cic_T_PN[i] = np.mean(TPN[i::12])


#################################### 
"MEDIA MULTIANUAL DE SST TT, PP, PN"
#################################### 

med_manual_T_TT = np.mean(TTT)
med_manual_T_PP = np.mean(TPP)
med_manual_T_PN = np.mean(TPN)

################################### 
"CICLO ANUAL DE MAX SST TT, PP, PN"
################################### 

Mm_T_TT = np.zeros((12,2))
Mm_T_PP = np.zeros((12,2))
Mm_T_PN = np.zeros((12,2))

for i in range(12):
    Mm_T_TT[i,0] = np.max(TTT[i::12])
    Mm_T_TT[i,1] = np.min(TTT[i::12])        
    Mm_T_PP[i,0] = np.max(TPP[i::12])
    Mm_T_PP[i,1] = np.min(TPP[i::12])
    Mm_T_PN[i,0] = np.max(TPN[i::12])
    Mm_T_PN[i,1] = np.min(TPN[i::12])

ano_Mm_T_TT = Mm_T_TT-med_manual_T_TT
ano_Mm_T_PP = Mm_T_PP-med_manual_T_PP
ano_Mm_T_PN = Mm_T_PN-med_manual_T_PN


############################################ 
"CICLO ANUAL DE ANOMALÍAS DE SST TT, PP, PN"
############################################ 
          
ano_T_TT = cic_T_TT-med_manual_T_TT
ano_T_PP = cic_T_PP-med_manual_T_PP
ano_T_PN = cic_T_PN-med_manual_T_PN

################################################ 
"CICLO ANUAL DE MAX ANOMALÍAS DE SST TT, PP, PN"
################################################ 

ano_maxT_TT = np.zeros(12)
ano_maxT_PP = np.zeros(12)
ano_maxT_PN = np.zeros(12)

for i in range(12):
    if abs(ano_Mm_T_TT[i,0]) >= abs(ano_Mm_T_TT[i,1]):
        ano_maxT_TT[i] = ano_Mm_T_TT[i,0]
    else:
        ano_maxT_TT[i] = ano_Mm_T_TT[i,1]

for i in range(12):
    if abs(ano_Mm_T_PP[i,0]) >= abs(ano_Mm_T_PP[i,1]):
        ano_maxT_PP[i] = ano_Mm_T_PP[i,0]
    else:
        ano_maxT_PP[i] = ano_Mm_T_PP[i,1]
        
for i in range(12):
    if abs(ano_Mm_T_PN[i,0]) >= abs(ano_Mm_T_PN[i,1]):
        ano_maxT_PN[i] = ano_Mm_T_PN[i,0]
    else:
        ano_maxT_PN[i] = ano_Mm_T_PN[i,1]
        

fig = plt.figure(figsize=(7,4.8))
ax = fig.add_subplot(111)
ax.bar((0,1,2,3,4,5,6,7,8,9,10,11), ano_maxT_TT, width=1.0, color='#DF0101', label='Max')
ax.bar((0,1,2,3,4,5,6,7,8,9,10,11), ano_T_TT, width=1.0, color='#8A0808', label='Mean')
my_xticks = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.xticks((0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5),my_xticks)
ax.set_xlabel('$Month$', size='15')
ax.set_ylabel(u'$Temperature$ $Anomalies$ $($'+u'\xb0'+u'$C)$', size='15')
ax.legend(loc='best')
ax.set_ylim(ano_maxT_TT.min()-0.5, ano_maxT_TT.max()+0.5)
ax.set_title(u'$Annual$ $cycle$ $of$ $SST$ $Anomalies$ $(Tehuantepec)$', size='15')
