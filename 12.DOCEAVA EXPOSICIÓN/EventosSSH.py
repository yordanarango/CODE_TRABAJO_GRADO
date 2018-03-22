# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:08:32 2016

@author: yordan
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
from netcdftime import utime
import matplotlib.colors as colors
import datetime
from mpl_toolkits.basemap import Basemap


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
'''Forma de los datos'''
#==============================================================================
#Se toa cualquier archivo para saber su forma
Archivo_cualquiera = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SSH_y_ST_GLORYS/SSH/1993.nc')
forma = Archivo_cualquiera.variables['ssh'] # Forma de los datos--->(time, 81, 121) = (time, latitude, longitude)

Lon = Archivo_cualquiera.variables['longitude'][:]
Lat = Archivo_cualquiera.variables['latitude'][:]


#==============================================================================
'''Tomando los datos'''
#==============================================================================

fechas = pd.date_range('1993-01-01', '2015-12-29', freq='D')
data_TT = np.zeros((len(fechas),81, 121))
for i in range(1993,2016):  
    Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/SSH_y_ST_GLORYS/SSH/'+str(i)+'.nc')   
    #time = Archivo.variables['time'][:]    
    #cdftime = utime('hours since 1950-01-01 00:00:00', calendar='gregorian')
    #date = [cdftime.num2date(k) for k in time]
    #DATE = pd.date_range(date[0], date[1], freq='D')
    
    fecha_inicio = pd.date_range('1993-01-01', str(i)+'-01-01', freq = 'D')
    fecha_final  = pd.date_range('1993-01-01', str(i)+'-12-31', freq='D')
    
    if i == 2015:
        data_TT[len(fecha_inicio)-1:] = Archivo.variables['ssh'][:]
    else:    
        data_TT[len(fecha_inicio)-1:len(fecha_final)] = Archivo.variables['ssh'][:]

data_TT[data_TT == -32767] = np.NaN
#==============================================================================
'''Calculando ciclo anual'''
#==============================================================================
#ciclo_anual = np.zeros((12, 81, 121))
#
#for i in range(12):
#    ciclo_anual[i] = np.mean(data_TT[(fechas.month == i+1)], axis =0)

#==============================================================================
'''Calculando anomalías'''
#==============================================================================
#anom = np.zeros(data_TT.shape)
#
#for i in range(12):
#    anom[(fechas.month == i+1)] = data_TT[(fechas.month == i+1)]-ciclo_anual[i]

#==============================================================================
'''Tomando los datos'''
#==============================================================================
# Fechas TT
fechas_eventos = ['2008-01-03', '2003-03-31', '2003-11-29', '2013-03-03', '1996-02-05', '1993-03-14', '2007-03-05', '1999-02-14', '2000-12-20', '2003-12-17']
# Fechas PP
#fechas_eventos = ['1998-01-01', '1998-03-12', '2010-01-11', '2003-04-01', '2009-02-06', '2008-01-03', '2005-01-19', '2000-01-15', '1996-02-05', '1993-03-15']
# Fechas PN
#fechas_eventos = ['2009-02-06', '2005-02-06', '2015-02-15', '2013-03-04', '1998-03-12', '2014-09-02', '2010-03-08', '2006-11-23', '1998-01-01', '1993-01-29']




for i in fechas_eventos:
    #a = pd.Series(pd.to_datetime(i))
    #c = a+datetime.timedelta(days=1)
    #d = c[0].strftime('%Y-%m-%d')
    #print a, c, d
    TIME_MAX = pd.Series(pd.to_datetime(i))
    CUANDO = np.where(fechas == TIME_MAX[0])[0][0]
    #time_max = datetime.datetime.strptime(i, "%Y-%m-%d")
    #TIME_MAX = pd.DatetimeIndex(time_max)
    
    for j in range(-3, 4):
        
        time_evn = TIME_MAX+datetime.timedelta(days=j)#días previos y posteriores al evento
        #TIME_EVN = pd.Series(time_evn.format())[0]#días, pero en formato string
        TIME_EVN = time_evn[0].strftime('%Y-%m-%d')        
        cuando = np.where(fechas == time_evn[0])[0][0]
        
        lons,lats = np.meshgrid(Lon,Lat)
        fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=20, llcrnrlon=-105, urcrnrlon=-75, resolution='i')
        map.drawcoastlines(linewidth = 0.8)
        map.drawcountries(linewidth = 0.8)
        map.drawparallels(np.arange(0, 20, 5),labels=[1,0,0,1])
        map.drawmeridians(np.arange(-105,-75,10),labels=[1,0,0,1])
        x,y = map(lons,lats)
        bounds=np.linspace(np.nanmin(data_TT[CUANDO-3:CUANDO+4]), np.nanmax(data_TT[CUANDO-3:CUANDO+4]),25)
        bounds=np.around(bounds, decimals=2)
        cd = ax.contourf(x, y, data_TT[cuando], 25, norm=MidpointNormalize(midpoint=0), cmap=plt.cm.RdYlBu_r, levels=bounds)
        cbar=plt.colorbar(cd, orientation='vertical', pad=0.05, shrink=0.8, boundaries=bounds)
        cbar.set_label('m')
        ax.set_title('SSH - '+TIME_EVN, size='15')  
        plt.savefig('/home/yordan/Escritorio/EVN_SSH/TT/'+i+'/'+TIME_EVN+'.png', dpi=100,bbox_inches='tight')
