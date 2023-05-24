import numpy as np
import matplotlib.pyplot as plt

# Definir os dados da matriz
data = np.array([[3.0240e+07, 4.0320e+07, 0.0000e+00, 0.0000e+00, -3.0240e+07, -4.0320e+07],
                 [4.0320e+07, 1.5876e+08, 0.0000e+00, -1.0500e+08, -4.0320e+07, -5.3760e+07],
                 [0.0000e+00, 0.0000e+00, 1.4000e+08, 0.0000e+00, -1.4000e+08, 0.0000e+00],
                 [0.0000e+00, -1.0500e+08, 0.0000e+00, 1.0500e+08, 0.0000e+00, 0.0000e+00],
                 [-3.0240e+07, -4.0320e+07, -1.4000e+08, 0.0000e+00, 1.7024e+08, 4.0320e+07],
                 [-4.0320e+07, -5.3760e+07, 0.0000e+00, 0.0000e+00, 4.0320e+07, 5.3760e+07]])

# Criar a figura e o eixo
fig, ax = plt.subplots()

# Aumentar o tamanho das células no mapa de calor
cellsize = 0.5

# Criar o mapa de calor (heatmap) com os dados da matriz
heatmap = ax.imshow(data, cmap='coolwarm', aspect='auto', extent=[0, data.shape[1], 0, data.shape[0]], vmin=data.min(), vmax=data.max(), interpolation='nearest')

# Ajustar o tamanho das células
ax.set_xticks(np.arange(data.shape[1])+0.5)
ax.set_yticks(np.arange(data.shape[0])+0.5)
ax.set_xticklabels(['Col 0', 'Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5'])
ax.set_yticklabels(['Row 0', 'Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])

# Adicionar os valores da matriz no centro de cada célula do heatmap
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        text = ax.text(j+0.5, i+0.5, f'{data[i, j]:.2e}', ha='center', va='center', color='black')

# Adicionar um título
ax.set_title("Matriz Global")

# Mostrar a figura
plt.show()
