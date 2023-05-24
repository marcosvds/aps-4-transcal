import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir os dados dos nós
x = np.array([0, 0, 0.3])
y = np.array([0, 0.4, 0.4])
z = np.zeros_like(x)

# Definir os dados de deslocamento (inicialmente todos zero)
dx = np.zeros_like(x)
dy = np.zeros_like(y)
dz = np.zeros_like(z)

# Definir os dados de carga
carga_x = np.array([0, 0, 0])
carga_y = np.array([0, 150, -100])
carga_z = np.zeros_like(z)

# Definir os nós restritos
# restricoes_x = np.array([0, 0, 0])
# restricoes_y = np.array([1, 1, 2])
# restricoes_z = np.zeros_like(z)
restricoes_x = np.array([1, 1, 0])
restricoes_y = np.array([0, 1, 0])
restricoes_z = np.zeros_like(z)

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
