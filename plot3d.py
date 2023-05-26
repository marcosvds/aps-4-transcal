import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from funcoesTermosol import plota, importa, geraSaida




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
dados_estrutura = importa('entrada.xls')  # Importa todas as informações da estrutura do arquivo Excel
nn, N, nm, Inc, nc, F, nr, R = dados_estrutura

print("Número de nós (nn):", nn)


print("Matriz com as coordenadas dos nós (N):\n", N)
print("Número de elementos na treliça (nm):", nm)
print("Matriz de incidência dos elementos (Inc):\n", Inc)
print("Número de cargas (nc):", nc)
print("Vetor de cargas (F[0]):\n", F[0])
print("Vetor de cargas (F[1]):\n", F[1])
print("Vetor de cargas (F[2]):\n", F[2])

print("Número de restrições (nr):", nr)
print("Vetor de restrições (R):\n", R)


# Definir os dados dos nós
x = np.array(N[0])
y = np.array(N[1])
z = np.zeros_like(x)

# Definir os dados de deslocamento (inicialmente todos zero)
dx = np.zeros_like(x)
dy = np.zeros_like(y)
dz = np.zeros_like(z)

# Definir os dados de carga
# Definir os dados de carga
carga_x = np.array([F[0], F[1], F[2]])
carga_y = np.array([F[3], F[4], F[5]])
carga_z = np.zeros_like(z)

carga_z = np.zeros_like(z)

# Definir os nós restritos
# restricoes_x = np.array([0, 0, 0])
# restricoes_y = np.array([1, 1, 2])
# restricoes_z = np.zeros_like(z)

restricoes_x = np.array([0, 0, 0])
restricoes_y = np.array([1, 1, 0])
restricoes_z = np.zeros_like([1,1,1])

restricoes = [restricoes_x,restricoes_y,restricoes_z]


print("restricoes_x: ",restricoes_x)

# Criar uma figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotar os pontos dos nós
ax.scatter(x, y, z, color='red', label='Nós')

# Plotar as barras
ax.plot([x[0], x[1]], [y[0], y[1]], [z[0], z[1]], color='black')
ax.plot([x[1], x[2]], [y[1], y[2]], [z[1], z[2]], color='black')
ax.plot([x[2], x[0]], [y[2], y[0]], [z[2], z[0]], color='black')

# Plotar os vetores de deslocamento
ax.quiver(x, y, z, dx, dy, dz, length=0.1, color='blue', label='Deslocamentos')

# Plotar as cargas
ax.quiver(x, y, z, carga_x, carga_y, carga_z, length=0.1, color='green', label='Cargas')

# Plotar as restrições
ax.quiver(x, y, z, restricoes_x, restricoes_y, restricoes_z, length=0.1, color='orange', label='Restrições')

# Definir os rótulos dos eixos
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.set_zlabel('Eixo Z')

# Definir o título do gráfico
ax.set_title('Esforços na Treliça')

# Definir a legenda
ax.legend()

# Mostrar o gráfico
plt.show()
