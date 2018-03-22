# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 22:12:51 2016

@author: yordan
"""

import numpy as np

a = np.array(((15,20,33,46,589),(62,75,81,96,1001),(1461,122,163,124,158)))

mean_x = np.mean(a[0,:])
mean_y = np.mean(a[1,:])
mean_z = np.mean(a[2,:])
mean_vector = np.array([[mean_x],[mean_y],[mean_z]])

scatter_matrix1 = np.zeros((3,3)) # Se supone que ésta es la manera correcta
for i in range(a.shape[1]):
    scatter_matrix1 += (a[:,i].reshape(3,1) - mean_vector).dot((a[:,i].reshape(3,1) - mean_vector).T)

aa = a-mean_vector

scatter_matrix2 = np.dot(aa,aa.T) # Ésta es la matriz hipótesis. Si es igual a la matriz anterior, este procedimiento también sería válido

scatter_matrix3 = scatter_matrix2/4 # Otra forma de probar. La matriz de covarianza que se calcula en la siguiente línea, es otra forma de llevar a cabo  EOF's. Se supone que a partir de la matriz scatter, se puede llegar a la matríz de covarianza, simplemente dividiendo cada elemento entre n-1.
                                    # Luego, si al hacer ésto obtengo la matríz de covrianza, significa que he calculado bien la matriz scatter
scatter_matrix4 = np.cov([aa[0,:], aa[1,:], aa[2,:]])
