
import pandas as pd
import numpy as np

# Carregar os dados do CSV
df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
data = df.values

# Ordenar os dados
data = np.sort(data)

# Calcular a probabilidade acumulada
n = len(data)
rank = np.arange(1, n + 1)
prob = (rank - 0.5) / n

# Transformar os dados para ajuste linear
log_data = np.log(data).flatten()
log_minus_log_prob = np.log(-np.log(1 - prob)).flatten()

# Ajustar uma linha reta aos dados transformados
p = np.polyfit(log_data, log_minus_log_prob, 1)

# Calcular os parâmetros shape e scale
shape = p[0]
scale = np.exp(-p[1] / shape)

# Exibir os parâmetros shape e scale
print(f'Parâmetro Shape: {shape}')
print(f'Parâmetro Scale: {scale}')

