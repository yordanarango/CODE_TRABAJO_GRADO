# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 04:43:59 2016

@author: yordan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from scipy import linalg as la
import pandas as pd
from scipy.stats.stats import pearsonr

#==============================================================================
'''Extrayendo las series de viento'''
#==============================================================================

#Esta parte del código es para TT,PP y PN
UyV = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/UyV_1979_2016_res025.nc') #Este archivo tiene un dominio útil para las datos de viento de los chorros de TT, PP y PN
Variables = [v for v in UyV.variables]
print Variables

Lon = UyV.variables['longitude'][:]-360
Lat = UyV.variables['latitude'][:]

posiciones = ['TT','PP','PN','G','C', 'A']
longitudes = [-95.25, -87.75, -79.5, -93.0, -75.0, -60.0]
latitudes = [14.25, 10.5, 7.5, 21.0, 12.75, 27.0]

datep = pd.date_range('1979-01-01 00:00:00', '2015-12-31 18:00:00', freq='6H')
date = pd.DatetimeIndex(datep)
Serie = pd.DataFrame(index=date, columns=['spdTT','meridionalTT','spdPP','meridionalPP','spdPN','meridionalPN','spdG','meridionalG','spdC','meridionalC','spdA','meridionalA']) 

for i, j, k in zip(longitudes,latitudes, posiciones):
    LoN = np.where(i == Lon)[0][0]
    LaT = np.where(j == Lat)[0][0]
    u = UyV.variables['u10'][:len(datep), LaT, LoN]
    v = UyV.variables['v10'][:len(datep), LaT, LoN]
    spd = np.sqrt(u*u+v*v)
    Serie['spd'+k] = spd
    Serie['meridional'+k] = v

#==============================================================================
'''Extrayendo las series de Presión'''
#==============================================================================

SSP = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SSP_1979_2016_res025.nc') 
Variables = [v for v in SSP.variables]
print Variables

Lon = SSP.variables['longitude'][:]-360
Lat = SSP.variables['latitude'][:]

posiciones = ['TT','PP','PN','G','C', 'A']
longitudes = [-95.25, -87.75, -79.5, -93.0, -75.0, -60.0]
latitudes = [14.25, 10.5, 7.5, 21.0, 12.75, 27.0]

datep = pd.date_range('1979-01-01 00:00:00', '2015-12-31 18:00:00', freq='6H')

for i,j,k in zip(longitudes,latitudes, posiciones):
    LoN = np.where(i == Lon)[0][0]
    LaT = np.where(j == Lat)[0][0]
    ssp = SSP.variables['msl'][:len(datep), LaT, LoN]/100
    Serie['ssp'+k] = ssp

#==============================================================================
'''Extrayendo las series de invierno de Temperatura'''
#==============================================================================

SST = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SST_1979_2016_res025.nc') 
Variables = [v for v in SST.variables]
print Variables

Lon = SST.variables['longitude'][:]-360
Lat = SST.variables['latitude'][:]

posiciones = ['TT','PP','PN','G','C', 'A']
longitudes = [-95.25, -87.75, -79.5, -93.0, -75.0, -60.0]
latitudes = [14.25, 10.5, 7.5, 21.0, 12.75, 27.0]

datep = pd.date_range('1979-01-01 00:00:00', '2015-12-31 18:00:00', freq='6H')

for i,j,k in zip(longitudes,latitudes, posiciones):
    LoN = np.where(i == Lon)[0][0]
    LaT = np.where(j == Lat)[0][0]
    sst = SST.variables['sst'][:len(datep), LaT, LoN]
    Serie['sst'+k] = sst

#==============================================================================
'''Extrayendo los meses de invierno'''
#==============================================================================

indices4 = np.where(Serie.index.month == 4)[0]
indices5 = np.where(Serie.index.month == 5)[0]
indices6 = np.where(Serie.index.month == 6)[0]
indices7 = np.where(Serie.index.month == 7)[0]
indices8 = np.where(Serie.index.month == 8)[0]
indices9 = np.where(Serie.index.month == 9)[0]
indices10 = np.where(Serie.index.month == 10)[0]

SERIE = Serie.drop(Serie.index[indices4])
SERIE = Serie.drop(Serie.index[indices5])
SERIE = Serie.drop(Serie.index[indices6])
SERIE = Serie.drop(Serie.index[indices7])
SERIE = Serie.drop(Serie.index[indices8])
SERIE = Serie.drop(Serie.index[indices9])
SERIE = Serie.drop(Serie.index[indices10])


#==============================================================================
'''Ploteando correlogramas y Calculando correlaciones'''
#==============================================================================

serie1 = ['spdTT','meridionalTT','spdPP','meridionalPP','spdPN','meridionalPN']
serie2 = ['G', 'C', 'A']
serie3 = ['spd', 'meridional', 'ssp', 'sst']

path = '/home/yordan/Escritorio/EXPOSICION_9/CORRELACIONES'

correl = pd.DataFrame(index = ['spdG','meridionalG','sspG','sstG','spdC','meridionalC','sspC','sstC','spdA','meridionalA','sspA','sstA'],
                                  columns = ['spdTT','meridionalTT','spdPP','meridionalPP','spdPN','meridionalPN'])

for l in serie1:
    for m in serie2:
        for n in serie3:
            corr = pearsonr(Serie[l], Serie[n+m])[0]
            correl.set_value(n+m, l, corr)
            fig=plt.figure(figsize=(7,5), facecolor='w', edgecolor='w')
            ax1 = fig.add_subplot(111)
            ax2 = ax1.twinx()
            ax1.plot(Serie[l]['2014-01-01':'2014-12-31'], linewidth=1, color='k', label=l)
            ax1.set_xlabel('$Time$', size='15')
            ax1.set_ylabel('$Volocity$ $(m/s)$', size='15')
            ax1.legend(loc='upper center')
            ax2.plot(Serie[n+m]['2014-01-01':'2014-12-31'], color='r', linewidth=1, label=n+m)
            if n == 'spd':
                ax2.set_ylabel('$Velocity$ $(m/s)$', size='15')
            elif n == 'meridional':
                ax2.set_ylabel('$Velocity$ $(m/s)$', size='15')
            elif n == 'ssp':
                ax2.set_ylabel('$Presure$ $(hPa)$', size='15')
            else:
                ax2.set_ylabel('$Temperature$ $(k)$', size='15')
            ax2.grid(True) 
            ax1.legend(loc='upper right')
            ax2.legend(loc='upper left')
            ax1.set_title(l+' and '+n+m, size='15')
            plt.savefig(path +'/'+l+'_'+n+m+'.png',dpi=100,bbox_inches='tight')
            plt.close('all')
