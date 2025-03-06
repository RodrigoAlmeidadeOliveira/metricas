from signal import pause
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as s
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas import read_csv
import scipy.stats as s
import random
import numpy as np
from scipy.stats import weibull_min
from scipy.optimize import curve_fit
import seaborn as sns # common form of importing seaborn

# Tamanho do vetor
tamanho = 1000000
vetor = []
data = read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste.csv')
percentile63 = np.percentile(data, 63)
desvio_medio = s.median_abs_deviation(data)
media = np.mean(data)
coef_var = (desvio_medio / media ) * 100
print(desvio_medio)
print(coef_var)
shape, loc, scale = weibull_min.fit(data, floc=0)

print("Parâmetro de forma (shape):", shape)
print("Parâmetro de escala (scale):", scale)

print("P63: " , percentile63)


for i in range(tamanho):
    semanas = 0
    wip =10 
    while wip > 0:
        #Syntax : random.weibullvariate(alpha, beta)
        #Parameters :
        #alpha : scale parameter
        #beta : shape parameter
        
        numero = random.weibullvariate(scale, shape)  #* random.random()
        wip -= numero
        semanas += 1      
    vetor.append(semanas)

# Plotar o histograma
plt.hist(vetor, bins=range(1, max(vetor) + 2), color='blue', edgecolor='black')
#sns.distplot(vetor, kde=True, rug=True)
#plt.hist(vetor, bins=200, color='blue', edgecolor='black')
percentile = np.percentile(vetor, 85)
percentile2 = np.percentile(vetor, 15)
print("P85: " ,percentile )
print("P15: " ,percentile2)
## print median, average, max
print("median")
print(np.median(vetor))
print("average")
print(np.mean(vetor))
print("max")
print(np.max(vetor))
plt.axvline(percentile, color='r', linestyle='dashed', linewidth=2)
plt.axvline(percentile2, color='r', linestyle='dashed', linewidth=2)
plt.xlabel('Semanas')
plt.ylabel('Frequência')
plt.title('Histograma de Semanas para Reduzir WIP a Zero - Weibull')
plt.grid(True)
plt.show()

