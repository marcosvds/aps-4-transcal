import numpy as np
from funcoesTermosol import *
import math

[nn,N,nm,Inc,nc,F,nr,R] = importa('entrada.xls')

def gauss_seidel(ite, tol, K, F):
    n = len(F)
    x = np.zeros(n)
    x1 = np.zeros(n)
    for k in range(ite):
        for i in range(n):
            x1[i] = F[i]
            for j in range(n):
                if (j != i):
                    x1[i] = x1[i] - K[i][j] * x1[j]
            x1[i] = x1[i] / K[i][i]
        norma = 0
        for i in range(n):
            if x1[i] != 0 and x[i] != 0:
                norma = abs(x1[i] - x[i])/abs(x1[i])
                print(x1[i], x[i])
        if (norma < tol and k > 0):
            return x1
        for i in range(n):
            x[i] = x1[i]
    return x1

def calcula_sen_cos(no1,no2, matriz_nos):
    no1 = int(no1)
    no2 = int(no2)
    L = math.sqrt((matriz_nos[0][no2-1] -  matriz_nos[0][no1-1])**2 + (matriz_nos[1][no2-1] -  matriz_nos[1][no1-1])**2)
    cos = (matriz_nos[0][no2-1] -  matriz_nos[0][no1-1])/L
    sen = (matriz_nos[1][no2-1] -  matriz_nos[1][no1-1])/L
    return sen,cos,L  

def solve_trelica(num_nos, matriz_nos, num_elementos, matriz_incid, num_c, vetor_cargas, num_r, vetor_restricoes):
    matriz_global = np.zeros((num_nos*2, num_nos*2))
    gdl = {}
    E = matriz_incid[0][2]
    A = matriz_incid[0][3]
    for i in range(1, num_nos+1):
        gdl[i] = [i*2-2, i*2-1]
    for array_nos in (matriz_incid):
        K = np.zeros((4,4))
        s,c,l = calcula_sen_cos(array_nos[0],array_nos[1], matriz_nos)
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
    vetor_restricoes_novo = []
    vetor_cargas_novo = []
    for a in vetor_restricoes:
        vetor_restricoes_novo.append(int(a[0]))
    for a in vetor_cargas:
        vetor_cargas_novo.append(int(a[0]))
    matriz_restita = np.delete(np.delete(matriz_global, vetor_restricoes_novo, 0), vetor_restricoes_novo, 1)
    cargas_restita = np.delete(vetor_cargas_novo, vetor_restricoes_novo, 0)
    deslocamentos = gauss_seidel(1000, 1e-10, matriz_restita, cargas_restita)
    deformacoes = []
    tensoes = []
    forcas_internas = []

    d_tot = np.zeros(num_nos*2)
    j = 0
    for i in range(len(d_tot)):
        if i not in vetor_restricoes_novo:
            d_tot[i] = deslocamentos[j]
            j += 1
    reacoes = np.dot(matriz_global, d_tot)
    for array_nos in (matriz_incid):
        K = np.zeros(4)
        s,c,l = calcula_sen_cos(array_nos[0],array_nos[1], matriz_nos)
        gdls = gdl[array_nos[0]]+gdl[array_nos[1]]
        K[0] = -c
        K[1] = -s
        K[2] = c
        K[3] = s
        deformacoes.append(np.dot(K,d_tot[gdls])/l)
        tensoes.append(E*deformacoes[-1])
        forcas_internas.append(A*tensoes[-1])

    return reacoes[vetor_restricoes_novo], d_tot, deformacoes, forcas_internas, tensoes
solve_trelica(nn, N, nm, Inc, nc, F, nr, R)