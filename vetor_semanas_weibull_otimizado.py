import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as s
import random
import math

# Tamanho do vetor
tamanho = 1000000
vetor_semanas = [] 

# Carregar os dados do CSV uma vez
datacsv = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste.csv')
dados = datacsv  # Substitua 'coluna_desejada' pelo nome correto da coluna

# Calcular média e desvio padrão uma vez
media_dados = dados.mean()
desvio_dados = dados.std()

print("Dados de entrada")
print("median")
print(np.median(dados))
print("average")
print(media_dados)
print("max")
print(dados.max())
    
max_valor = int(dados.max())
min_valor = int(dados.min())
(shape, scale) = s.exponweib.fit_loc_scale(dados, 1, 1 )
print(shape, scale)

# Vetorização para calcular as semanas de uma vez
numeros = np.random.normal(media_dados, desvio_dados, tamanho)
vetor_semanas = np.ceil(np.cumsum(np.where(numeros < 0, 0, numeros) / 20))

# Plotar o histograma
plt.hist(vetor_semanas, bins=np.arange(1, max_valor + 2), color='blue', edgecolor='black')
percentile = np.percentile(vetor_semanas, 85)
percentile2 = np.percentile(vetor_semanas, 15)
print("P85: " ,percentile )
print("P15: " ,percentile2)
## print median, average, max
print("median")
print(np.median(vetor_semanas))
print("average")
print(np.mean(vetor_semanas))
print("max")
print(vetor_semanas.max())
plt.axvline(percentile, color='r', linestyle='dashed', linewidth=2)
plt.axvline(percentile2, color='r', linestyle='dashed', linewidth=2)
plt.xlabel('Semanas')
plt.ylabel('Frequência')
plt.title('Histograma de Semanas para Reduzir WIP a Zero - Normal')
plt.grid(True)
plt.show()