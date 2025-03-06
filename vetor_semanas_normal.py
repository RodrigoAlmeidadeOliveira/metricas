from signal import pause
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as s
import random
from pandas import read_csv
import math

# Tamanho do vetor
tamanho = 1000000
vetor_semanas = [] 
datacsv = read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste.csv')
media_dados = float(np.mean(datacsv))
desvio_dados = float(np.std(datacsv))

print("Dados de entrada")
print("median")
print(np.median(datacsv))
print("average")
print(np.mean(datacsv))
print("max")
print(np.max(datacsv))
    
max = int(datacsv.min())
min = int(datacsv.max())
(shape, scale) = s.exponweib.fit_loc_scale(datacsv, 1, 1 )
print(shape, scale)

for i in range(tamanho):
    semanas = 0
    wip = 20
    numero = 0
    while wip > 0:
        numero = random.normalvariate(media_dados,desvio_dados) 
        wip -= numero
        semanas += 1      
    vetor_semanas.append(semanas)

# Plotar o histograma
#plt.hist(vetor_semanas, bins=range(1, max(vetor_semanas) + 2), color='blue', edgecolor='black')
plt.hist(vetor_semanas, bins=10, color='blue', edgecolor='black')
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
print(np.max(vetor_semanas))
plt.axvline(percentile, color='r', linestyle='dashed', linewidth=2)
plt.axvline(percentile2, color='r', linestyle='dashed', linewidth=2)
plt.xlabel('Semanas')
plt.ylabel('Frequência')
plt.title('Histograma de Semanas para Reduzir WIP a Zero - Normal')
plt.grid(True)
plt.show()