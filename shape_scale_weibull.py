import pandas as pd
import numpy as np
from scipy.special import gamma
from scipy.stats import weibull_min

# Carregar os dados do CSV
df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
data = df.values

# Calcular a média e a variância dos dados
mean = np.mean(data)
variance = np.var(data)

# Estimar o parâmetro shape (k) usando a fórmula dos momentos
def estimate_shape(mean, variance):
    return (mean / (variance ** 0.5)) ** (-1.086)

# Estimar o parâmetro scale (λ) usando o valor estimado de shape (k)
def estimate_scale(mean, shape):
    return mean / gamma(1 + 1/shape)

# Calcular os parâmetros shape e scale
shape = estimate_shape(mean, variance)
scale = estimate_scale(mean, shape)

# Exibir os parâmetros shape e scale
print(f'Parâmetro Shape: {shape}')
print(f'Parâmetro Scale: {scale}')

# Ajustar a distribuição Weibull aos dados
shape, loc, scale = weibull_min.fit(data, floc=0)

# Exibir os parâmetros shape e scale
print(f'Parâmetro Shape weibull fit: {shape}')
print(f'Parâmetro Scale weibull fit: {scale}')
