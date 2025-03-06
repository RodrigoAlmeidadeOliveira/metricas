import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Carregar os dados do CSV
df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
data = df.values

# Função de verossimilhança negativa
def negative_log_likelihood(params, data):
    shape, scale = params
    n = len(data)
    likelihoods = (shape - 1) * np.sum(np.log(data)) - np.sum((data / scale) ** shape) + n * np.log(shape / scale) - n * np.log(scale)
    return -likelihoods

# Estimar os parâmetros shape e scale usando a função de verossimilhança negativa
initial_guess = [1.0, 1.0]  # Chute inicial para os parâmetros
result = minimize(negative_log_likelihood, initial_guess, args=(data,), bounds=((0.0001, None), (0.0001, None)))
shape, scale = result.x

# Exibir os parâmetros shape e scale
print(f'Parâmetro Shape: {shape}')
print(f'Parâmetro Scale: {scale}')
