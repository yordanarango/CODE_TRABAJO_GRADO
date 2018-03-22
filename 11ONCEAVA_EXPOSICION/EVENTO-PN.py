# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 04:09:45 2016

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

Archivo = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/EVENTOS CHORROS ERA/EVN-PN-SSHyST-2009-02-06.nc')
Variables = [v for v in Archivo.variables]
Variables

lat = Archivo.variables['lat'][:]
lon = Archivo.variables['lon'][:]
depth = Archivo.variables['depth'][:]
st = Archivo.variables['water_temp'][:]
time = Archivo.variables['time'][:]

lat_indx = 3 # 8.23999977
lon_indx = 6 # -79.5
depth_indx = np.where(depth == 100)[0][0]

lat_evn = lat[lat_indx]
lon_evn = lon[lon_indx]
depth_evn = depth[:depth_indx+1]
st_evn = st[:, :depth_indx+1, lat_indx, lon_indx]

ST_EVN = st_evn.T


TIME = np.arange(len(time))
x,y = np.meshgrid(TIME, depth_evn)


fig = plt.figure(figsize=(10,5), edgecolor='W',facecolor='W')
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])

bounds=np.linspace(np.nanmin(ST_EVN), np.nanmax(ST_EVN),25) 
bounds=np.around(bounds, decimals=2)
cd = ax1.contourf(x, y, ST_EVN, bounds, cmap=plt.cm.YlOrRd)#rainbow
ca = plt.colorbar(cd, drawedges = 'True',format='%.1f')

my_xticks = pd.date_range('2009-02-04', '2009-02-08', freq='D')
Time = np.arange(0,len(TIME), 8)
plt.xticks(Time, my_xticks, size=7)#rotation=90

ca.set_label('C')
ax1.set_title('Temporal evolution of temperature profile (PN)', size='13')
ax1.set_ylabel('$Depth$ $(m)$', size='15')
ax1.set_xlabel('$Time$', size='15')
ax1.invert_yaxis()

plt.grid(True)
plt.show()
