import time
import numpy as np
import matplotlib.pyplot as plt
from pandas._libs.tslibs.offsets import Hour

import datetime

# Obter a hora atual
hora_inicio = datetime.datetime.now()

# Imprimir a hora de início
print("O programa iniciou em:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))

# Definindo os parâmetros da distribuição Weibull
k = 1  # parâmetro de forma
l = 1  # parâmetro de escala

# Gerando a distribuição Weibull com um milhão de registros
num_registros = 1000000
tamanho = 10000
valores_k = []
for _ in range(tamanho):
    dados_weibull = np.random.weibull(k, num_registros) * l
    percentil_98 = np.percentile(dados_weibull, 98)
    mediana = np.median(dados_weibull)
    ratio_p98_mediana = percentil_98 / mediana
    valores_k.append(ratio_p98_mediana)
    

# Calculando o percentil 98 e a mediana
percentil_98 = np.percentile(dados_weibull, 98)
mediana = np.median(dados_weibull)

# Exibindo os resultados
print(f"Percentil 98: {percentil_98}")
print(f"Mediana: {mediana}")
ratio_p98_mediana = percentil_98 / mediana
print(f"Ratio: {ratio_p98_mediana}")

 

# Obter a hora atual
hora_fim= datetime.datetime.now()

# Imprimir a hora de início
print("O programa terminou em:", hora_fim.strftime("%Y-%m-%d %H:%M:%S"))


plt.hist(valores_k, edgecolor='black')
plt.xlabel('VALORES K')
plt.ylabel('Frequência')
plt.title('Histograma de Valores K')
plt.grid(True)
plt.tight_layout()
plt.show()