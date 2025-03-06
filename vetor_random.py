import random
import matplotlib.pyplot as plt

# Tamanho do vetor
tamanho = 100000

# Gerar números aleatórios entre 2 e 10
vetor = [random.lognormvariate(2, 3)for _ in range(tamanho)]
vetor2 = [random.weibullvariate(2, 30)for _ in range(tamanho)]
# Plotar o histograma
plt.hist(vetor, bins=10, color='blue', edgecolor='black')
plt.xlabel('Valores')
plt.ylabel('Frequência')
plt.title('Histograma de Números Aleatórios entre 2 e 10')
plt.grid(True)
plt.show()

plt.hist(vetor2, bins=10, color='blue', edgecolor='black')
plt.xlabel('Valores')
plt.ylabel('Frequência')
plt.title('Histograma de Números Aleatórios entre 2 e 10')
plt.grid(True)
plt.show()