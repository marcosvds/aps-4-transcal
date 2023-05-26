import numpy as np
from solve import *
import math


# Chamar a função solve_trelica com os argumentos apropriados
resultados = solve_trelica(nn, N, nm, Inc, nc, F, nr, R)

reacoes_apoio = resultados[0]
deslocamentos = resultados[1]
deformacoes = resultados[2]
forcas_internas = resultados[3]
tensoes_internas = resultados[4]

# Formatar os resultados
reacoes_apoio_str = "Reacoes de apoio [N]\n" + np.array2string(reacoes_apoio, formatter={'float_kind': lambda x: "%.8f" % x})
deslocamentos_str = "Deslocamentos [m]\n" + np.array2string(deslocamentos, formatter={'float_kind': lambda x: "%.8f" % x})
deformacoes_str = "Deformacoes []\n" + np.array2string(deformacoes, formatter={'float_kind': lambda x: "%.8f" % x})
forcas_internas_str = "Forcas internas [N]\n" + np.array2string(forcas_internas, formatter={'float_kind': lambda x: "%.8f" % x})
tensoes_internas_str = "Tensoes internas [Pa]\n" + np.array2string(tensoes_internas, formatter={'float_kind': lambda x: "%.8f" % x})

# Salvar resultados em um arquivo
with open('resultados.txt', 'w') as f:
    f.write(reacoes_apoio_str + "\n\n")
    f.write(deslocamentos_str + "\n\n")
    f.write(deformacoes_str + "\n\n")
    f.write(forcas_internas_str + "\n\n")
    f.write(tensoes_internas_str + "\n\n")

