import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

# Tamanho do vetor
tamanho = 1000000
vetor = []

# Leitura de dados a partir do arquivo CSV (ajuste o caminho do arquivo conforme necessário)
data = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste.csv')

# Ajustar uma distribuição Weibull aos dados e obter os parâmetros shape e scale
shape, loc, scale = np.percentile(data, [85, 95])

print("Parâmetros da distribuição Weibull:")
print("Percentile 85:", shape)
print("Percentile 95:", scale)

# Preencher o vetor com números aleatórios seguindo a distribuição Weibull
for _ in range(tamanho):
    semanas = 0
    wip = 50
    while wip > 0:
        numero = (scale / shape) * (-np.log(1 - random.random()))**(1 / shape)
        wip -= numero
        semanas += 1
    vetor.append(semanas)

# Calcular os percentis
percentile_85 = np.percentile(vetor, 85)
percentile_95 = np.percentile(vetor, 95)

# Plotar o histograma
plt.hist(vetor, bins=range(1, max(vetor) + 2), color='blue', edgecolor='black')
plt.axvline(percentile_85, color='r', linestyle='dashed', linewidth=2, label='85th Percentile')
plt.axvline(percentile_95, color='g', linestyle='dashed', linewidth=2, label='95th Percentile')
plt.xlabel('Semanas')
plt.ylabel('Frequência')
plt.title('Histograma de Semanas para Reduzir WIP a Zero')
plt.legend()
plt.grid(True)
plt.show()
