import numpy as np
import matplotlib.pyplot as plt

# Cria um vetor de 100 números aleatórios entre 2 e 10
vetor = np.random.weibull(2,size=1500000)

# Cria um histograma do vetor
plt.hist(vetor)

# Exibe o histograma
plt.show()