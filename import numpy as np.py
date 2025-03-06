import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Carregar dados do arquivo .xls
df = pd.read_excel('/users/rodrigoalmeidadeoliveira/documents/dados/metricas_adiq.xls')

# Calculando Lead Time
df['DONE'] = pd.to_datetime(df['DONE'])
df['Data de Criação-WI'] = pd.to_datetime(df['Data de Criação-WI'])
df['Lead Time'] = (df['DONE'] - df['Data de Criação-WI']).dt.days

# Estatísticas Descritivas
desc_stats = df.describe()

# Gráfico de Cumulative Flow
plt.figure(figsize=(10, 6))
sns.histplot(df['DONE'], bins=5, cumulative=True, stat='density', kde=True)
plt.title('Cumulative Flow')
plt.xlabel('Data de Conclusão (DONE)')
plt.ylabel('Densidade Cumulativa')
plt.show()

# Lead Time Control Chart
plt.figure(figsize=(10, 6))
plt.plot(df['DONE'], df['Lead Time'], marker='o', linestyle='-')
plt.axhline(y=df['Lead Time'].mean(), color='r', linestyle='--', label='Média')
plt.axhline(y=df['Lead Time'].mean() + 3*df['Lead Time'].std(), color='g', linestyle='--', label='3 Desvios Padrão')
plt.axhline(y=np.percentile(df['Lead Time'], 85), color='b', linestyle='--', label='Percentil 85%')
plt.legend()
plt.title('Lead Time Control Chart')
plt.xlabel('Data de Conclusão (DONE)')
plt.ylabel('Lead Time (dias)')
plt.show()

# Throughput Run Chart
plt.figure(figsize=(10, 6))
plt.plot(df['DONE'], range(1, len(df) + 1), marker='o', linestyle='-')
plt.title('Throughput Run Chart')
plt.xlabel('Data de Conclusão (DONE)')
plt.ylabel('Throughput')
plt.show()

# Histograma de Lead Time
plt.figure(figsize=(10, 6))
sns.histplot(df['Lead Time'], bins=5, kde=True)
plt.title('Histograma de Lead Time')
plt.xlabel('Lead Time (dias)')
plt.ylabel('Frequência')
plt.show()

# Análise de Assimetria
skewness = stats.skew(df['Lead Time'])
print(f'Assimetria do Lead Time: {skewness}')

# Desvio Padrão e Médio
std_deviation = df['Lead Time'].std()
mean_deviation = df['Lead Time'].mad()
print(f'Desvio Padrão do Lead Time: {std_deviation}')
print(f'Desvio Médio Absoluto do Lead Time: {mean_deviation}')