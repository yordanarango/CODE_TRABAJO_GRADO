# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 03:01:52 2016

@author: yordan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from scipy import linalg as la
import pandas as pd
import pickle
import xlrd
from scipy.stats.stats import pearsonr
import matplotlib.colors as colors
from scipy.stats.stats import pearsonr

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y)) 

#==============================================================================
'''box para indices '''
#==============================================================================

lat1 = [16, 12, 12, 16, 16]
lon1 = [-81, -81, -70, -70, -81]

fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=40, llcrnrlon=-120, urcrnrlon=-55, resolution='i')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 40, 10),labels=[1,0,0,1])
map.drawmeridians(np.arange(-120,-55,10),labels=[1,0,0,1])

LON1, LAT1 = map(lon1, lat1)

map.plot(LON1, LAT1, marker=None, color='k', linewidth=1.5)
   
ax.set_title('$Ubicacion$ $Indices$', size='15')    
map.fillcontinents(color='white')
    
plt.show()

#==============================================================================
'''Selección de fechas en las que se va a hacer correlaciones '''
#==============================================================================

fechas = pd.date_range('1979/01/01 00:00:00', '1988-12-31 23:00:00', freq='6H')

#==============================================================================
'''Selección de series para formar indices '''
#==============================================================================

PR = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/PRESION-SEA-LEVEL-ERA/MSLP_025x025_0x40N_120_55W.nc')
Variables = [v for v in PR.variables]
print Variables
lonPR = PR.variables['longitude'][:]-360
latPR = PR.variables['latitude'][:]

MASK = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/mascara_025x025.nc')
mask = MASK.variables['lsm'][:]
mask = np.array(mask)
mask = mask.reshape((mask.shape[1], mask.shape[2]))
mask[mask == 1] = np.NaN
mask[mask == 0] = 1

up1    = np.where(latPR == 16)[0][0]
down1  = np.where(latPR == 12)[0][0]
left1  = np.where(lonPR == -81)[0][0]
right1 = np.where(lonPR == -70)[0][0]

INDICE = pd.DataFrame(index=fechas, columns=['serie1', 'serie2', 'indice'])
for i, j in enumerate(INDICE.index):
    serie1 = PR.variables['msl'][i, up1:down1+1, left1:right1+1]/100
    serie1 = serie1*mask[up1:down1+1, left1:right1+1]
    SERIE1 = np.nanmean(serie1)
     
    INDICE['serie1'][j] = SERIE1
    INDICE['indice'][j] = SERIE1

#==============================================================================
'''Datos para correlaciones '''
#==============================================================================

UyV = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/CORRELACIONES_SST-SSP_vsCPs/UyV-025x025-6h.nc')
Variables = [v for v in UyV.variables]

Lat = UyV.variables["latitude"][:]
Lon = UyV.variables["longitude"][:]-360

#==============================================================================
'''MAPAS DE CORRELACIONES'''
#==============================================================================

def mapa_corr(NC, serie, fechas):
    mapa = NC.variables['u10'][0, :, :] # la idea en ésta línea es captar la forma que tendrá el mapa final de correlaciones. Por eso es indistinto el uso de u10 o v10
    MAPA   = np.zeros((mapa.shape[0], mapa.shape[1]))
    MAPAv  = np.zeros((mapa.shape[0], mapa.shape[1]))
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            u = NC.variables['u10'][:len(fechas), i, j]
            v = NC.variables['v10'][:len(fechas), i, j]
            spd = np.sqrt(u*u+v*v)            
            MAPA[i,j] = pearsonr(spd, serie)[0]
            MAPAv[i, j] = pearsonr(v, serie)[0]
    return MAPA, MAPAv

corr_spd, corr_meridional = mapa_corr(UyV, INDICE.indice, fechas)

#==============================================================================
'''PLOTEANDO MAPAS'''
#==============================================================================

def plot_mapa(mapa, variable, LAT, LON):
    fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    map = Basemap(projection='merc', llcrnrlat = LAT[-1], urcrnrlat = LAT[0], llcrnrlon = LON[0], urcrnrlon = LON[-1], resolution='i')
    map.drawcoastlines(linewidth = 0.8)
    map.drawcountries(linewidth = 0.8)
    map.drawparallels(np.arange(LAT[-1], LAT[0], 10),labels=[1,0,0,1])
    map.drawmeridians(np.arange(LON[0],LON[-1],10),labels=[1,0,0,1])
    
    
    lons,lats = np.meshgrid(LON,LAT)
    x,y = map(lons,lats)
    
    bounds=np.linspace( np.min(mapa) ,np.max(mapa), 25) 
    bounds=np.around(bounds, decimals=2) 
    CF = map.contourf(x,y, mapa, 25, norm=MidpointNormalize(midpoint=0), cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow cmap=plt.cm.RdYlBu_r
    cb = plt.colorbar(CF, orientation='vertical', pad=0.05, shrink=0.8, boundaries=bounds, format='%.2f')
    ax.set_title('Field Correlations (INDEX'+'-'+variable+')', size='15')    
    map.fillcontinents(color='white')
    plt.show()

plot_mapa(corr_meridional, 'Speed Meridional', Lat, Lon)
