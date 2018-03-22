# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 09:25:32 2016

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
'''LECTURA DE DATOS'''
#==============================================================================
           
UyV = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/CORRELACIONES_SST-SSP_vsCPs/UyV-025x025-6h.nc')
Variables = [v for v in UyV.variables]

Lat = UyV.variables["latitude"][:]
Lon = UyV.variables["longitude"][:]-360
#time = UyV.variables["time"][:]
    
#============================================================================= 
'''DOMINIO PARA EOF's'''
#==============================================================================

aux = np.zeros((len(Lat), len(Lon)))

a = np.where(Lon == -95.75)[0][0] # La posición de la coordenada longitudinal -95.75
b = np.where(Lat == 16.75) [0][0] # La posición de la coordenada latitudinal 16.75
lon_95_75 = np.where(Lon == -95.75)[0][0]
lon_77_75 = np.where(Lon == -75.75)[0][0]


d = 0
e = 0
for i, j in enumerate(Lon[lon_95_75:lon_77_75+1]):
    if j <= -79.5:
        if i%2 == 0:
            aux[b+i-(i//2):b+i-(i//2)+19,a+i] = 1
        else:
            aux[b+i-((i//2)+1):b+i-((i//2)+1)+19,a+i] = 1
    else:
        if i%2 == 0:
            aux[b+i-(i//2):b+i-(i//2)+17-(5*d),a+i] = 1
            d = d+1
        else:
            aux[b+i-((i//2)+1):b+i-((i//2)+1)+15-(5*e),a+i] = 1
            e = e+1
        
f = np.where(Lon == -97.5)[0][0] # La posición de la coordenada longitudinal -97.5
g = np.where(Lat == 13.25)[0][0] # La posición de la coordenada latitudinal 13.25
lon_97_5 = np.where(Lon == -97.5)[0][0]
lon_95_75 = np.where(Lon == -95.75)[0][0]


for k, l in enumerate(Lon[lon_97_5:lon_95_75+1]):
    if k%2 == 0:
        aux[g+k-(k//2)-(1+(5*(k//2))):g+k-(k//2)+1,f+k] = 1
    else:
        aux[g+k-(k//2)-((k//2)+(4*((k//2)+1))):g+k-(k//2)+1,f+k] = 1

aux[ aux==0 ] = np.NAN
wh = np.where(aux == 1)

#==============================================================================
'''Se define una sóla variable 'fechas' para todo el código'''
#==============================================================================

# fechas en las que se quiere hacer las EOF's
FECHAS = pd.date_range('1979/01/01 00:00:00', '2015-12-31 23:00:00', freq='6H')
# fechas para calcular ciclos diurno y anual
fechas = pd.date_range('1979/01/01 00:00:00', '2015-12-31 23:00:00', freq='6H')

#==============================================================================
'''Removiendo Ciclo diurno y anual de la velocidad del viento'''
#==============================================================================

#def remov_ciclo_v(UyV, LAT, LON,wh, fechas):   
#    MAPA = np.zeros((len(fechas), len(LAT), len(LON)))
#    for l in range(len(wh[0])):
#            u = UyV.variables['u10'][:len(fechas), wh[0][l], wh[1][l]] # Se mete dentro de la función, para sólo ingresar a las series de interés, de lo contrario habría que hacer una lectura de todos los pixeles, procedimiento que es muy pesado para el computador.
#            v = UyV.variables['v10'][:len(fechas), wh[0][l], wh[1][l]]
#            serie = np.sqrt(u*u+v*v)
#            media = np.zeros((12,4)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
#            
#            for i in range(1,13): # Se recorre cada mes
#                for j in range(0, 19, 6): # Se recorre cada horario
#                    selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
#                    for k in range(len(serie)): # Se recorre toda la serie
#                        if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
#                            if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
#                                selec.append(serie[k]) # Si cumple, se adiciona a la lista
#                    media[i-1, j/6] = np.mean(selec) # Se guarda el valor de la media
#
#            ano = np.zeros(len(serie))
#            for n in range(len(serie)):
#                ano[n] = serie[n]-media[fechas[n].month-1, fechas[n].hour/6]
#            
#            MAPA[:, wh[0][l], wh[1][l]] = ano
#    
#    return MAPA
#
#spd_ano = remov_ciclo_v(UyV, Lat, Lon, wh, fechas)

#==============================================================================
'''Removiendo ciclo diurno y anual de la componente meridional del viento'''
#==============================================================================

def remov_ciclo_meridional(UyV, LAT, LON,wh, fechas, FECHAS):   
    MAPA = np.zeros((len(FECHAS), len(LAT), len(LON)))
    DATA = pd.DataFrame(index=fechas, columns=['datos'])
    MEDIA = np.zeros((len(wh[0]), 12, 4))
    for l in range(len(wh[0])):
            v = UyV.variables['v10'][:len(fechas), wh[0][l], wh[1][l]]
            serie = v
            media = np.zeros((12,4)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
            
            for i in range(1,13): # Se recorre cada mes
                for j in range(0, 19, 6): # Se recorre cada horario
                    selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
                    for k in range(len(serie)): # Se recorre toda la serie
                        if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                            if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                                selec.append(serie[k]) # Si cumple, se adiciona a la lista
                    media[i-1, j/6] = np.mean(selec) # Se guarda el valor de la media

            MEDIA[l] = media 
            ano = np.zeros(len(FECHAS))
            DATA['datos'] = serie
            SERIE = DATA['datos'][FECHAS[0]:FECHAS[-1]]            

            for n in range(len(ano)):
                ano[n] = SERIE[n]-media[SERIE.index[n].month-1, SERIE.index[n].hour/6]
            
            MAPA[:, wh[0][l], wh[1][l]] = ano
    
    return MAPA, MEDIA

meridional_ano, meridional_media = remov_ciclo_meridional(UyV, Lat, Lon, wh, fechas, FECHAS)

#==============================================================================
'''SELECCIÓN DE LAS SERIES'''
#==============================================================================

wh = np.where(aux == 1)

def seleccion(wh, serie): #Selección de los datos que están en el dominio de interés de las EOF
    ar = []
    for i in range(len(wh[0])):
        ar.append(serie[:,wh[0][i],wh[1][i]])
        
    serie_seleccionada = np.array(ar)
    serie_seleccionada = serie_seleccionada.T
    
    return serie_seleccionada

#spd_EOF = seleccion(wh, spd_ano) # Selección de datos de velocidad
meridional_EOF = seleccion(wh, meridional_ano) # Selección de datos de componente meridional de la velocidad

#==============================================================================
'''MATRIZ DE COVARIANZA'''
#==============================================================================

#matrix_cov = np.dot(spd_EOF, spd_EOF.T) # Matríz de covarianza para los datos de velocidad
matrix_cov = np.dot(meridional_EOF, meridional_EOF.T) # Matríz de covarianza para los datos de componente meridional del viento

#==============================================================================
'''Extracción de valores y vectores propios'''
#==============================================================================

e_values, e_vect = np.linalg.eig(matrix_cov)

e_val = e_values.real; e_vec = e_vect.real

#==============================================================================
'''Extracción de componentes principales'''
#==============================================================================

PC1 = e_vec.T[0]
PC2 = e_vec.T[1]
PC3 = e_vec.T[2]
PC4 = e_vec.T[3]

#==============================================================================
'''Varianza Explicada'''
#==============================================================================

sum_evals = np.sum(e_val.real)
var_exp = (e_val.real/sum_evals) * 100

#==============================================================================
'''Gráfica de Varianza explicada'''
#==============================================================================

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(np.arange(1,11), var_exp[0:10], marker='o', color='r')
ax.set_xlabel('Component', size='12', style='oblique')
ax.set_ylabel('Variance [%]', size='12', style='oblique')
ax.grid(True)
ax.set_title('Explained variance', size='12')
plt.savefig('/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/EOF-MERIDIONAL'+'/'+'Varianza explicada'+'.png',dpi=100,bbox_inches='tight')
plt.close('all')

#==============================================================================
'''Cálculo de EOF's'''
#==============================================================================

#PC = np.dot(e_vec.T, spd_EOF) # Cálculo de PC's para datos de velocidad del viento
PC = np.dot(e_vec.T, meridional_EOF) # Cálculo de PC's para datos de componente meridional del viento 

#==============================================================================
'''Volviendo a la forma original de los datos'''
#==============================================================================

# Se utiliza cualquiera uno de los dos PrCo, según la serie que se esté utilizando: meridional_ano ó spd_ano
# PrCo = np.zeros((spd_ano.shape[0], spd_ano.shape[1], spd_ano.shape[2]))
PrCo = np.zeros((meridional_ano.shape[0], meridional_ano.shape[1], meridional_ano.shape[2]))
for i in range(len(wh[0])):
    PrCo[:, wh[0][i], wh[1][i]] = PC[:,i].real


#==============================================================================
'''PLOTEA EOF'''
#==============================================================================

fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
box_lon = [-97.5, -79.5, -77.75, -95.75, -97.5]
box_lat = [13.25, 4.25, 7.75, 16.75, 13.25]
map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=24, llcrnrlon=-105, urcrnrlon=-75, resolution='i')
lons,lats = np.meshgrid(Lon,Lat)
x,y = map(lons,lats)
bounds=np.linspace( np.min(PrCo[3]) ,np.max(PrCo[3]),20) 
bounds=np.around(bounds, decimals=2) 
csf=map.contourf(x,y, PrCo[3], 20, norm=MidpointNormalize(midpoint=0), cmap=plt.cm.RdYlBu_r,levels=bounds)
cbar=plt.colorbar(csf,orientation='horizontal', pad=0.05, shrink=0.8, boundaries=bounds)
cbar.set_label('$Amplitud$', fontsize='15')
TT_lon,TT_lat = map(box_lon, box_lat)
map.plot(TT_lon, TT_lat, marker=None, color='k')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 24, 8),labels=[1,0,0,1])
map.drawmeridians(np.arange(-105,-75,10),labels=[1,0,0,1])
ax.set_title('EOF-4 [5.95%]', size='15', weight='medium')
plt.show()

#==============================================================================
'''MAPA AREA EOF's'''
#==============================================================================

area = UyV.variables['v10'][0]*aux

box_lon = [-97.5, -79.5, -77.75, -95.75, -97.5]
box_lat = [13.25, 4.25, 7.75, 16.75, 13.25]
lons,lats = np.meshgrid(Lon,Lat)
fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
ax = fig.add_axes([0.1,0.1,0.8,0.8])
map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=20, llcrnrlon=-100, urcrnrlon=-75, resolution='i')
map.drawcoastlines(linewidth = 0.8)
map.drawcountries(linewidth = 0.8)
map.drawparallels(np.arange(0, 20, 7),labels=[1,0,0,1])
map.drawmeridians(np.arange(-100,-75,10),labels=[1,0,0,1])
x,y = map(lons,lats)
TT_lon,TT_lat = map(box_lon, box_lat)
CF = map.contourf(x,y, area[:,:], np.linspace(-7, 5, 20), extend='both', cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow
cb = map.colorbar(CF, size="5%", pad="2%", extendrect = 'True', drawedges = 'True', format='%.1f')
cb.set_label('m/s')
ax.set_title('$Meridional$ $Speed$ $(1979-01-01)$', size='15', weight='medium')
map.plot(TT_lon, TT_lat, marker=None, color='k')
map.fillcontinents(color='white')
plt.show()

#==============================================================================
'''leyendo datos SSP y SST'''
#==============================================================================

SSP = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/CORRELACIONES_SST-SSP_vsCPs/SSP-1x1-6h.nc')
VariablesSSP = [v for v in SSP.variables]
print VariablesSSP
lonSSP = SSP.variables['longitude'][:]-360
latSSP = SSP.variables['latitude'][:]

SST = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/CORRELACIONES_SST-SSP_vsCPs/SST-1x1-6h.nc')
VariablesSST = [v for v in SST.variables]
print VariablesSST
lonSST = SST.variables['longitude'][:]-360
latSST = SST.variables['latitude'][:]

MASK = nc.Dataset('/home/yordan/Escritorio/TRABAJO_DE_GRADO/DATOS_Y_CODIGOS/DATOS/mascara_1x1.nc')
mask = MASK.variables['lsm'][:]
mask = np.array(mask)
mask = mask.reshape((mask.shape[1], mask.shape[2]))
mask[mask == 1] = np.NaN
mask[mask == 0] = 1
LonM = MASK.variables['longitude'][:]-360
LatM = MASK.variables['latitude'][:]

#==============================================================================
'''Ciclo diurno y anual SSP y SST'''
#==============================================================================

def remov_ciclo(NC, var, LAT, LON, fechas, FECHAS):
    MAPA = np.zeros((len(FECHAS), len(LAT), len(LON)))
    DATA = pd.DataFrame(index=fechas, columns=['datos'])
    prueba = NC.variables[var][0, :, :]*mask
    for l in range(len(LAT)):
        for m in range(len(LON)):
            if np.isnan(prueba[ l, m]) == False: 
                serie = NC.variables[var][:len(fechas), l, m] 
                media = np.zeros((12,4)) # Las filas representan los meses, y las columnas los cuatro horarios dentro de un día
                
                for i in range(1,13): # Se recorre cada mes
                    for j in range(0, 19, 6): # Se recorre cada horario
                        selec = [] # Cada horario de cada mes, se debe vovler a crear la lista, que es donde se guardarán los datos de horario de cada mes
                        for k in range(len(serie)): # Se recorre toda la serie
                            if fechas[k].month == i: # Se verifica que la fecha que corresponde al valor de la serie, cumpla la condición
                                if fechas[k].hour == j: # Se verifica que el horario que corresponde al valor de la serie, cumpla la condición
                                    selec.append(serie[k]) # Si cumple, se adiciona a la lista
                        media[i-1, j/6] = np.mean(selec) # Se guarda el valor de la media
    
                ano = np.zeros(len(FECHAS))
                DATA['datos'] = serie
                SERIE = DATA['datos'][FECHAS[0]:FECHAS[-1]]
                
                for n in range(len(ano)):
                    ano[n] = SERIE[n]-media[SERIE.index[n].month-1, SERIE.index[n].hour/6]                
                MAPA[:, l, m] = ano
    return MAPA

SsP = remov_ciclo(SSP, 'sp', latSSP, lonSSP, fechas, FECHAS)
SsT = remov_ciclo(SST, 'sst', latSSP, lonSSP, fechas, FECHAS)

#==============================================================================
'''MAPAS DE CORRELACIONES'''
#==============================================================================

def mapa_corr(serie, mapa):
    MAPA = np.zeros((mapa.shape[1], mapa.shape[2]))
    for i in range(mapa.shape[1]):
        for j in range(mapa.shape[2]):
            MAPA[i,j] = pearsonr(mapa[:, i, j], serie)[0] 
    return MAPA

#CORRELACIONES CON SSP
PC1_SSP = mapa_corr(PC1, SsP)
PC2_SSP = mapa_corr(PC2, SsP)
PC3_SSP = mapa_corr(PC3, SsP)
PC4_SSP = mapa_corr(PC4, SsP)

#CORRELACIONES CON SST
PC1_SST = mapa_corr(PC1, SsT)
PC2_SST = mapa_corr(PC2, SsT)
PC3_SST = mapa_corr(PC3, SsT)
PC4_SST = mapa_corr(PC4, SsT)

#==============================================================================
'''PLOTEANDO MAPAS'''
#==============================================================================

def plot_mapa(mapa, variable, componente, path, LAT, LON):
    fig = plt.figure(figsize=(8,8), edgecolor='W',facecolor='W')
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=40, llcrnrlon=-120, urcrnrlon=-55, resolution='i')
    map.drawcoastlines(linewidth = 0.8)
    map.drawcountries(linewidth = 0.8)
    map.drawparallels(np.arange(0, 40, 10),labels=[1,0,0,1])
    map.drawmeridians(np.arange(-120,-55,10),labels=[1,0,0,1])
    
    
    lons,lats = np.meshgrid(LON,LAT)
    x,y = map(lons,lats)
    
    bounds=np.linspace( np.min(mapa) ,np.max(mapa), 50) 
    bounds=np.around(bounds, decimals=2) 
    CF = map.contourf(x,y, mapa, 50, norm=MidpointNormalize(midpoint=0), cmap=plt.cm.RdYlBu_r)#plt.cm.rainbow cmap=plt.cm.RdYlBu_r
    cb = plt.colorbar(CF, orientation='vertical', pad=0.05, shrink=0.8, boundaries=bounds, format='%.2f')
    ax.set_title('Field Correlations (PC'+str(componente)+'-'+variable+')', size='15')    
    map.fillcontinents(color='white')
    plt.savefig(path +'/PC'+str(componente)+'-'+variable+'.png',dpi=100, bbox_inches='tight')
    
    plt.close('all')
    
#MAPAS CON SSP
plot_mapa(PC1_SSP, 'SSP', 1, '/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/IMAGENES_CORRELACIONES_PCs(meridional)_SSTySSP', latSSP, lonSSP)
plot_mapa(PC2_SSP, 'SSP', 2, '/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/IMAGENES_CORRELACIONES_PCs(meridional)_SSTySSP', latSSP, lonSSP)
plot_mapa(PC3_SSP, 'SSP', 3, '/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/IMAGENES_CORRELACIONES_PCs(meridional)_SSTySSP', latSSP, lonSSP)
plot_mapa(PC4_SSP, 'SSP', 4, '/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/IMAGENES_CORRELACIONES_PCs(meridional)_SSTySSP', latSSP, lonSSP)

#MAPAS CON SST
plot_mapa(PC1_SST, 'SST', 1, '/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/IMAGENES_CORRELACIONES', latSST, lonSST)
plot_mapa(PC2_SST, 'SST', 2, '/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/IMAGENES_CORRELACIONES', latSST, lonSST)
plot_mapa(PC3_SST, 'SST', 3, '/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/IMAGENES_CORRELACIONES', latSST, lonSST)
plot_mapa(PC4_SST, 'SST', 4, '/home/yordan/Escritorio/TRABAJO_DE_GRADO/EXPOSICIONES/EXPOSICION_11/IMAGENES_CORRELACIONES', latSST, lonSST)
