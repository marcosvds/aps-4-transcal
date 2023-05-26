import numpy as np
from funcoesTermosol import *
import math


"""
Importar dados de entrada do arquivo 'entrada.xls' e atribuir a variáveis
nn: int - Número de nós
N: numpy.ndarray - Matriz com as coordenadas dos nós (2 x nn)
nm: int - Número de elementos na treliça
Inc: numpy.ndarray - Matriz de incidência dos elementos (nm x 4)
nc: int - Número de cargas
F: numpy.ndarray - Vetor de cargas (nc x 2)
nr: int - Número de restrições
R: numpy.ndarray - Vetor de restrições (nr x 2)
"""
[nn, N, nm, Inc, nc, F, nr, R] = importa('entrada_2.xls')

def gauss_seidel(ite, tol, K, F):
    """
    Implementação do método de Gauss-Seidel para resolver um sistema de equações lineares.
    ...
    """

    n = len(F)
    x = np.zeros(n)
    x1 = np.zeros(n)

    # Iterações do método de Gauss-Seidel
    for k in range(ite):
        for i in range(n):
            x1[i] = F[i]
            for j in range(n):
                if (j != i):
                    x1[i] = x1[i] - K[i][j] * x1[j]
            x1[i] = x1[i] / K[i][i]

        # Verificar critério de convergência
        norma = 0
        for i in range(n):
            if x1[i] != 0 and x[i] != 0:
                norma = abs(x1[i] - x[i]) / abs(x1[i])

        if (norma < tol and k > 0):
            return x1

        # Atualizar x
        for i in range(n):
            x[i] = x1[i]

    return x1

def jacobi(ite, tol, K, F):
    n = len(F)
    x = np.zeros(n)
    x1 = np.zeros(n)
    for k in range(ite):
        for i in range(n):
            x1[i] = F[i]
            for j in range(n):
                if (j != i):
                    x1[i] = x1[i] - K[i][j] * x[j]
            x1[i] = x1[i] / K[i][i]
        norma = 0
        for i in range(n):
            if x1[i] != 0 and x[i] != 0:
                norma = abs(x1[i] - x[i])/abs(x1[i])
        if (norma < tol):
            return x1
        for i in range(n):
            x[i] = x1[i]
    return x1

def calcula_sen_cos(no1, no2, matriz_nos):
    """
    Calcula o seno, cosseno e o comprimento entre dois nós na treliça.
    ...
    """

    no1 = int(no1)
    no2 = int(no2)
    L = math.sqrt((matriz_nos[0][no2 - 1] - matriz_nos[0][no1 - 1]) ** 2 + (matriz_nos[1][no2 - 1] - matriz_nos[1][no1 - 1]) ** 2)
    cos = (matriz_nos[0][no2 - 1] - matriz_nos[0][no1 - 1]) / L
    sen = (matriz_nos[1][no2 - 1] - matriz_nos[1][no1 - 1]) / L
    return sen, cos, L


def solve_trelica(num_nos, matriz_nos, num_elementos, matriz_incid, num_c, vetor_cargas, num_r, vetor_restricoes):
    """
    Resolve o problema da treliça.
    ...
    """

    matriz_global = np.zeros((num_nos * 2, num_nos * 2))
    gdl = {}
    

    # Mapear graus de liberdade de cada nó
    for i in range(1, num_nos + 1):
        gdl[i] = [i * 2 - 2, i * 2 - 1]

    # Montar a matriz global de rigidez
    for array_nos in (matriz_incid):
        K = np.zeros((4, 4))
        s, c, l = calcula_sen_cos(array_nos[0], array_nos[1], matriz_nos)
        gdls = gdl[array_nos[0]] + gdl[array_nos[1]]
        E = array_nos[2]
        A = array_nos[3]
        # Montar a matriz de rigidez local
        K[0][0] = c ** 2
        K[0][1] = c * s
        K[0][2] = -c ** 2
        K[0][3] = -c * s
        K[2][0] = -c ** 2
        K[2][1] = -c * s
        K[2][2] = c ** 2
        K[2][3] = c * s
        K[1][0] = c * s
        K[1][1] = s * s
        K[1][2] = -c * s
        K[1][3] = -s * s
        K[3][0] = -c * s
        K[3][1] = -s * s
        K[3][2] = c * s
        K[3][3] = s * s

        K = (E * A / l) * K
        matriz_global[np.ix_(gdls, gdls)] += K

    # Remover restrições da matriz global e vetor de cargas
    vetor_restricoes_novo = []
    vetor_cargas_novo = []

    for a in vetor_restricoes:
        vetor_restricoes_novo.append(int(a[0]))

    for a in vetor_cargas:
        vetor_cargas_novo.append(int(a[0]))

    matriz_restita = np.delete(np.delete(matriz_global, vetor_restricoes_novo, 0), vetor_restricoes_novo, 1)
    cargas_restita = np.delete(vetor_cargas_novo, vetor_restricoes_novo, 0)

    # Resolver o sistema de equações lineares
    deslocamentos = gauss_seidel(1000, 1e-10, matriz_restita, cargas_restita)

    # Calcular deformações, forças internas e reações de apoio
    deformacoes = []
    tensoes = []
    forcas_internas = []

    d_tot = np.zeros(num_nos * 2)
    j = 0
    for i in range(len(d_tot)):
        if i not in vetor_restricoes_novo:
            d_tot[i] = deslocamentos[j]
            j += 1

    reacoes = np.dot(matriz_global, d_tot)

    for array_nos in (matriz_incid):
        K = np.zeros(4)
        s, c, l = calcula_sen_cos(array_nos[0], array_nos[1], matriz_nos)
        gdls = gdl[array_nos[0]] + gdl[array_nos[1]]

        K[0] = -c
        K[1] = -s
        K[2] = c
        K[3] = s

        deformacoes.append(np.dot(K, d_tot[gdls]) / l)
        tensoes.append(E * deformacoes[-1])
        forcas_internas.append(A * tensoes[-1])

    deformacoes = np.array(deformacoes)
    tensoes = np.array(tensoes)
    forcas_internas = np.array(forcas_internas)

    return (
        reacoes[vetor_restricoes_novo].reshape(-1, 1),
        d_tot.reshape(-1, 1),
        deformacoes.reshape(-1, 1),
        forcas_internas.reshape(-1, 1),
        tensoes.reshape(-1, 1),
    )

# Chamar a função solve_trelica com os argumentos apropriados
reacoes, deslocamento, deformacoes, forcas_internas, tensoes = solve_trelica(nn, N, nm, Inc, nc, F, nr, R)

def plota(N,Inc, reacoes, deslocamento, deformacoes, forcas_internas, tensoes):
    # Numero de membros
    nm = len(Inc[:,0])
    import matplotlib as mpl
    import matplotlib.pyplot as plt

#    plt.show()
    fig = plt.figure()
    N_deslocado = N + deslocamento.reshape(2,-1)
    # Passa por todos os membros
    for i in range(nm):
        print(i)
        # encontra no inicial [n1] e final [n2] 
        n1 = int(Inc[i,0])
        n2 = int(Inc[i,1])        
        if i == 0:
            plt.plot([N[0,n1-1],N[0,n2-1]],[N[1,n1-1],N[1,n2-1]],color='r',linewidth=3, label='Original')
            plt.plot([N_deslocado[0,n1-1],N_deslocado[0,n2-1]],[N_deslocado[1,n1-1],N_deslocado[1,n2-1]],color='b',linewidth=3, linestyle='--', label='Deformado')
        else:
            plt.plot([N[0,n1-1],N[0,n2-1]],[N[1,n1-1],N[1,n2-1]],color='r',linewidth=3)
            plt.plot([N_deslocado[0,n1-1],N_deslocado[0,n2-1]],[N_deslocado[1,n1-1],N_deslocado[1,n2-1]],color='b',linewidth=3, linestyle='--')
    plt.legend()
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

plota(N,Inc, reacoes, deslocamento, deformacoes, forcas_internas, tensoes)