# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 04:33:14 2016

@author: yordan
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pylab as pl
import numpy as np
import netCDF4 as nc
from netcdftime import utime
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
'''Tomando los datos'''
#==============================================================================
fechas = pd.date_range('1993-01-01', '2015-12-29', freq='D')
data_TT = np.zeros((len(fechas),24))
for i in range(1993,2016):  
    #Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SSH_y_ST_GLORYS/Tehuantepec/'+str(i)+'.nc') #TT
    #Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SSH_y_ST_GLORYS/Papagayos/'+str(i)+'.nc') #PP     
    Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SSH_y_ST_GLORYS/Panama/'+str(i)+'.nc') #PN   
    time = Archivo.variables['time'][:]    
    cdftime = utime('hours since 1950-01-01 00:00:00', calendar='gregorian')
    date = [cdftime.num2date(k) for k in time]
    DATE = pd.date_range(date[0], date[1], freq='D')
    
    fecha_inicio = pd.date_range('1993-01-01', str(i)+'-01-01', freq = 'D')
    fecha_final  = pd.date_range('1993-01-01', str(i)+'-12-31', freq='D')
    
    if i == 2015:
        data_TT[len(fecha_inicio)-1:] = Archivo.variables['temperature'][:,:,1,1]
    else:    
        data_TT[len(fecha_inicio)-1:len(fecha_final)] = Archivo.variables['temperature'][:,:,1,1]

#==============================================================================
'''Calculando ciclo anual'''
#==============================================================================
ciclo_anual = np.zeros((12, 24))

for i in range(24):
    for j in range(12):
        ciclo_anual[j, i] = np.mean(data_TT[(fechas.month == j+1),i])
        
#==============================================================================
'''Calculando anomalías'''
#==============================================================================
anom_TT = np.zeros(data_TT.shape)

for i in range(24):
    for j in range(len(fechas)):
        anom_TT[j, i] = data_TT[j, i] - ciclo_anual[fechas[j].month-1, i]
    
#==============================================================================
'''Tomando datos de los eventos'''
#==============================================================================
# Fechas TT
#fechas_eventos = ['2008-01-03', '2003-03-31', '2003-11-29', '2013-03-03', '1996-02-05', '1993-03-14', '2007-03-05', '1999-02-14', '2000-12-20', '2003-12-17']
# Fechas PP
#fechas_eventos = ['1998-01-01', '1998-03-12', '2010-01-11', '2003-04-01', '2009-02-06', '2008-01-03', '2005-01-19', '2000-01-15', '1996-02-05', '1993-03-15']
# Fechas PN
fechas_eventos = ['2009-02-06', '2005-02-06', '2015-02-15', '2013-03-04', '1998-03-12', '2014-09-02', '2010-03-08', '2006-11-23', '1998-01-01', '1993-01-29']

for i in fechas_eventos:
    fecha_evns = np.where(fechas == i)[0][0]
    time_evn   = fechas[fecha_evns-3:fecha_evns+4]
    depth = Archivo.variables['depth'][:]
    
    evn_st_TT = anom_TT[fecha_evns-3:fecha_evns+4,:].T
    
    TIME = np.arange(len(time_evn))
    x,y = np.meshgrid(TIME, depth)

    #==============================================================================
    '''Ploteando datos'''
    #==============================================================================

    fig = plt.figure(figsize=(10,5), edgecolor='W',facecolor='W')
    ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
    
    bounds=np.linspace(np.nanmin(evn_st_TT), np.nanmax(evn_st_TT),25) 
    bounds=np.around(bounds, decimals=2)
    cd = ax1.contourf(x, y, evn_st_TT, 25, norm=MidpointNormalize(midpoint=0), cmap=plt.cm.RdYlBu_r, levels=bounds)#rainbow
    cbar=plt.colorbar(cd, orientation='horizontal', pad=0.05, shrink=0.8, boundaries=bounds)
    
    plt.xticks(TIME, time_evn, size=7)
    
    cbar.set_label('C')
    ax1.set_title('Temporal evolution of temperature anomaly profile (PN-'+i+')', size='13')
    ax1.set_ylabel('$Depth$ $(m)$', size='15')
    ax1.set_xlabel('$Time$', size='15')
    ax1.invert_yaxis()
    
    plt.grid(True)
    plt.savefig('/home/yordan/Escritorio/EVNS-ST/PN/'+i+'.png', dpi=100,bbox_inches='tight')





