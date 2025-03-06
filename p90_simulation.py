import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configurações
N = 30  # Tamanho da amostra
P = 90  # Percentil
iterations = 10000  # Número de amostras

# Função para simular o experimento
def simulate_experiment(N, P, iterations):
    results = []
    for i in range(1, iterations + 1):
        sample = np.random.rand(N) * 100  # Gerar amostras aleatórias (0 a 100)
        percentile_value = np.percentile(sample, P)  # Calcular o valor do percentil
        above_count = np.sum(sample > percentile_value)  # Valores acima do percentil
        below_count = N - above_count  # Valores abaixo do percentil
        
        # Criar registro da simulação
        record = {
            "Sample_Index": i,
            "Sample_Size": N,
            "Percentile": P,
            "Above_Percentile_Count": above_count,
            "Below_Percentile_Count": below_count,
            "Percentile_Value": percentile_value,
        }
        
        # Adicionar os valores da amostra
        for j in range(N):
            record[f"Sample_Point_{j + 1}"] = sample[j]
        
        results.append(record)
    return pd.DataFrame(results)

# Simular o experimento
df = simulate_experiment(N, P, iterations)

# Mostrar as primeiras linhas da tabela
print(df.head())

# Plotar o histograma para "Above_Percentile_Count"
# plt.hist(df["Above_Percentile_Count"], bins=np.arange(-0.5, N + 1.5, 1), edgecolor='black', density=True, alpha=0.7)
# plt.title(f'Histograma das Contagens Acima do Percentil {P}')
# plt.xlabel('Número de Valores Acima do Percentil')
# plt.ylabel('Frequência Relativa')
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()

# Plotar o histograma para "Percentile_Value"
plt.hist(df["Percentile_Value"], bins=10, edgecolor='black', density=True, alpha=0.7)
plt.title(f'Histograma dos Valores Percentis (P={P})')
plt.xlabel('Valor do Percentil')
plt.ylabel('Frequência Relativa')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
