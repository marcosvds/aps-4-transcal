from funcoesTermosol import importa
import math
import numpy as np
[nn,N,nm,Inc,nc,F,nr,R] = importa('entrada.xls')
lista_params = [nn,N,nm,Inc,nc,F,nr,R]


def calcula_sen_cos(no1,no2):
    no1 = int(no1)
    no2 = int(no2)
    # print(N)
    L = math.sqrt((N[0][no2-1] -  N[0][no1-1])**2 + (N[1][no2-1] -  N[1][no1-1])**2)
    cos = (N[0][no2-1] -  N[0][no1-1])/L
    sen = (N[1][no2-1] -  N[1][no1-1])/L
    return sen,cos,L  


def calcula_K_local(Inc):
    E = Inc[0][2]
    A = Inc[0][3]
    i = 0
    array_K =[]
    for array_nos in (Inc):
        K = np.zeros((4,4))
        s,c,l = calcula_sen_cos(array_nos[0],array_nos[1])
        print(f'valor do seno {s} valor do cosseno {c}')
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
        array_K.append(K)       
    print(array_K)
    return 0

print(calcula_K_local(Inc))

