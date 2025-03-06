import pandas as pd
import numpy as np
from scipy.stats import linregress
from scipy.special import gammaln

# Carregar os dados do CSV
df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')  # Substitua pelo caminho correto do seu arquivo CSV
data = df['A'].dropna().values # Certifique-se de que não há valores NaN

# Passo 2: Ordenar os dados em ordem crescente
data_sorted = np.sort(data)
print(data_sorted)

# Passo 3: Calcular os centros dos intervalos
n = len(data_sorted)
interval_centers = [(2 * (i + 1) - 3) / (2 * n) for i in range(n)]  # Corrigido para i + 1

# Evitar valores exatamente 0 ou 1
interval_centers = np.clip(interval_centers, 1e-10, 1 - 1e-10)

# Passo 4: Calcular os logaritmos naturais dos dados
log_data = np.log(data_sorted)

# Passo 5: Linearizar a função de distribuição cumulativa
log_minus_log_prob = np.log(-np.log(1 - np.array(interval_centers)))

# Garantir que os arrays sejam unidimensionais
log_data = np.ravel(log_data)
log_minus_log_prob = np.ravel(log_minus_log_prob)

# Verificar o tamanho dos arrays
print(f'Tamanho de log_data: {len(log_data)}')
print(f'Tamanho de log_minus_log_prob: {len(log_minus_log_prob)}')

# Verificar se os arrays são unidimensionais
print(f'log_data é unidimensional: {log_data.ndim == 1}')
print(f'log_minus_log_prob é unidimensional: {log_minus_log_prob.ndim == 1}')

# Passo 6: Calcular o parâmetro shape usando regressão linear
if len(log_data) == len(log_minus_log_prob):
    slope, intercept, r_value, _, _ = linregress(log_data, log_minus_log_prob)
else:
    raise ValueError("Os tamanhos dos arrays log_data e log_minus_log_prob não coincidem.")

# Passo 8: Calcular o parâmetro scale
scale = np.exp(-intercept / slope)

# Passo 9: Calcular o R-quadrado para avaliar a qualidade do ajuste
r_squared = r_value**2

# Passo 10: Comparar a média prevista com a média real
predicted_mean = scale * np.exp(gammaln(1 + 1 / slope))
actual_mean = np.mean(data_sorted)

# Cálculo da mediana e percentil 98
median = np.median(data_sorted)
percentile_98 = np.percentile(data_sorted, 98)
percentile_98_to_median = percentile_98 / median

# Exibir os resultados
print(f'Quantidade de Pontos: {n}')
print(f'Parâmetro Shape: {slope}')
print(f'Parâmetro Scale: {scale}')
print(f'R-quadrado: {r_squared}')
print(f'Média Prevista: {predicted_mean}')
print(f'Média Real: {actual_mean}')
print(f'Mediana: {median}')
print(f'Percentil 98: {percentile_98}')
print(f'Percentil 98 / Mediana: {percentile_98_to_median}')
