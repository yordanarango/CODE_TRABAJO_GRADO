# -*- coding: utf-8 -*-

from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd

spd_TT_ALT = []
spd_PP_ALT = []
spd_PN_ALT = []

for i in range(1979, 2016): # De 0 a 37, porque sólo se va a hacer hasta el 2015 

    V = nc.Dataset('/media/jaimeignaciovelez/TOSHIBA EXT/MERIDIONAL/MERIDIONAL-alt/'+str(i)+'alt.nc')
    U = nc.Dataset('/media/jaimeignaciovelez/TOSHIBA EXT/ZONAL/ZONAL-pr/'+str(i)+'alt.nc')

	################################################################# 
	#"ZONAS DE ALTA INFLUENCIA EN TT, PP, PN (Con NAN's enmascarados)"
	#################################################################

    v_TT = np.ma.masked_invalid(V.variables["V"][:, 50:65, 35:46])
    u_TT = np.ma.masked_invalid(U.variables["U"][:, 50:65, 35:46])
    v_PP = np.ma.masked_invalid(V.variables["V"][:, 35:48, 58:77])
    u_PP = np.ma.masked_invalid(U.variables["U"][:, 35:48, 58:77])
    v_PN = np.ma.masked_invalid(V.variables["V"][:, 22:35, 97:106])
    u_PN = np.ma.masked_invalid(U.variables["U"][:, 22:35, 97:106])

	########################
	#"VEOCIDAD EN CADA PIXEL"
	########################

    velTT = np.sqrt(u_TT*u_TT+v_TT*v_TT) 
    velPP = np.sqrt(u_PP*u_PP+v_PP*v_PP)
    velPN = np.sqrt(u_PN*u_PN+v_PN*v_PN)

	###################### 
	#"COMPOSITE TT, PP, PN"
	######################

    spd_TT_alt = np.zeros(len(velTT[:,1,1]))
    spd_PP_alt = np.zeros(len(velPP[:,1,1]))
    spd_PN_alt = np.zeros(len(velPN[:,1,1]))

    for i in range(len(spd_PN_alt)):
        spd_TT_alt[i] = np.mean(velTT[i,:,:])
        spd_PP_alt[i] = np.mean(velPP[i,:,:])
        spd_PN_alt[i] = np.mean(velPN[i,:,:])

    spd_TT_ALT.append(spd_TT_alt)
    spd_PP_ALT.append(spd_PP_alt)
    spd_PN_ALT.append(spd_PN_alt)
    
    del V
    del U
    del v_TT
    del u_TT
    del v_PP
    del u_PP
    del v_PN
    del u_PN
    del velTT
    del velPP
    del velPN
    del spd_TT_alt
    del spd_PP_alt
    del spd_PN_alt

spd_TT = np.array(spd_TT_ALT)
spd_PP = np.array(spd_PP_ALT)
spd_PN = np.array(spd_PN_ALT)


ano = pd.date_range('1979/01/01 00:00:00','2015/12/31 21:00:00', freq='3H')

spd_TT_new = np.zeros(len(ano)) 
spd_PP_new = np.zeros(len(ano))
spd_PN_new = np.zeros(len(ano))

r = range(1979,2016)
for i, j in enumerate(r):
    if j%4 == 0:
        spd_TT_new[i*2920+((i+2)//4)*8:i*2920+((i+2)//4)*8+2928] = spd_TT[i]
        spd_PP_new[i*2920+((i+2)//4)*8:i*2920+((i+2)//4)*8+2928] = spd_PP[i]
        spd_PN_new[i*2920+((i+2)//4)*8:i*2920+((i+2)//4)*8+2928] = spd_PN[i]
    else:
        spd_TT_new[i*2920+((i+2)//4)*8:i*2920+((i+2)//4)*8+2920] = spd_TT[i]
        spd_PP_new[i*2920+((i+2)//4)*8:i*2920+((i+2)//4)*8+2920] = spd_PP[i]
        spd_PN_new[i*2920+((i+2)//4)*8:i*2920+((i+2)//4)*8+2920] = spd_PN[i]
	








