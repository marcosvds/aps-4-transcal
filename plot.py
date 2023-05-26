from funcoesTermosol import plota, importa, geraSaida

dados_estrutura = importa('entrada_original.xls')  # Importa todas as informações da estrutura do arquivo Excel

# Atribuindo os valores retornados a variáveis individuais
nn, N, nm, Inc, nc, F, nr, R = dados_estrutura

# Agora você pode usar as variáveis conforme necessário
plota(N, Inc)  # Exemplo de uso da função 'plota'
geraSaida("saida", Ft, Ut, Epsi, Fi, Ti)  # Exemplo de uso da função 'geraSaida'

