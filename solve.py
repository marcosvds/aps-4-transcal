import numpy as np
from funcoesTermosol import *
import math

[nn,N,nm,Inc,nc,F,nr,R] = importa('entrada.xls')

def calcula_sen_cos(no1,no2):
    no1 = int(no1)
    no2 = int(no2)
    L = math.sqrt((N[0][no2-1] -  N[0][no1-1])**2 + (N[1][no2-1] -  N[1][no1-1])**2)
    cos = (N[0][no2-1] -  N[0][no1-1])/L
    sen = (N[1][no2-1] -  N[1][no1-1])/L
    return sen,cos,L  

def solve_trelica(num_nos, matriz_nos, num_elementos, matriz_incid, num_c, vetor_cargas, num_r, vetor_restricoes):
    matriz_global = np.zeros((num_nos*2, num_nos*2))
    gdl = {}
    E = Inc[0][2]
    A = Inc[0][3]
    for i in range(1, num_nos+1):
        gdl[i] = [i*2-2, i*2-1]
    for array_nos in (Inc):
        K = np.zeros((4,4))
        s,c,l = calcula_sen_cos(array_nos[0],array_nos[1])
        gdls = gdl[array_nos[0]]+gdl[array_nos[1]]
        K[0][0] = c**2
        K[0][1] = c*s
        K[0][2] = -c**2
        K[0][3] = -c*s
        K[2][0] = -c**2
        K[2][1] = -c*s
        K[2][2] = c**2
        K[2][3] = c*s
        K[1][0] = c*s
        K[1][1] = s*s
        K[1][2] = -c*s
        K[1][3] = -s*s
        K[3][0] = -c*s
        K[3][1] = -s*s
        K[3][2] = c*s
        K[3][3] = s*s
        K = (E*A/l)*K
        matriz_global[np.ix_(gdls,gdls)] += K
        print(K)
        print(gdls)
    print(matriz_global)

    return matriz_global
solve_trelica(nn, N, nm, Inc, nc, F, nr, R)