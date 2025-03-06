import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Supondo que você já tenha carregado os dados em lead_time_data
lead_time_data = pd.read_excel('/users/rodrigoalmeidadeoliveira/documents/dados/LT_TH_SERVIÇO-05.xlsx', sheet_name='Lead Time')

lead_times = lead_time_data['LT']

# Cálculos estatísticos
mean_lt = lead_times.mean()
median_lt = lead_times.median()
std_lt = lead_times.std()
min_lt = lead_times.min()
max_lt = lead_times.max()
percentile_95 = np.percentile(lead_times, 95)
percentile_90 = np.percentile(lead_times, 90)
percentile_85 = np.percentile(lead_times, 85)

# Estatísticas descritivas
desc_stats = {
    "Média": mean_lt,
    "Mediana": median_lt,
    "Desvio Padrão": std_lt,
    "Mínimo": min_lt,
    "Máximo": max_lt,
    "Percentil 95%": percentile_95,
    "Percentil 90%": percentile_90,
    "Percentil 85%": percentile_85
}

# Exibição das estatísticas descritivas em uma tela separada
fig, ax = plt.subplots(figsize=(6, 4))
ax.axis('tight')
ax.axis('off')
table_data = [[key, f"{value:.2f}"] for key, value in desc_stats.items()]
table = ax.table(cellText=table_data, colLabels=["Estatística", "Valor"], cellLoc='center', loc='center')
table.scale(1, 2)
ax.set_title('Estatísticas Descritivas de Lead Time')
plt.show()

# Criando uma nova tela para os gráficos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Gráfico de dispersão
ax1.scatter(range(len(lead_times)), lead_times, color='blue', label='Lead Time')
ax1.axhline(y=mean_lt, color='green', linestyle='--', label=f'Média: {mean_lt:.2f}')
ax1.axhline(y=percentile_95, color='red', linestyle='--', label=f'Percentil 95%: {percentile_95:.2f}')
ax1.axhline(y=percentile_90, color='orange', linestyle='--', label=f'Percentil 90%: {percentile_90:.2f}')
ax1.axhline(y=percentile_85, color='purple', linestyle='--', label=f'Percentil 85%: {percentile_85:.2f}')
ax1.set_title('Gráfico de Dispersão de Lead Time')
ax1.set_xlabel('Índice')
ax1.set_ylabel('Lead Time')
ax1.legend()
ax1.grid(True)

# Histograma
ax2.hist(lead_times, bins=20, color='blue', alpha=0.7, label='Lead Time')
ax2.axvline(x=mean_lt, color='green', linestyle='--', label=f'Média: {mean_lt:.2f}')
ax2.axvline(x=percentile_95, color='red', linestyle='--', label=f'Percentil 95%: {percentile_95:.2f}')
ax2.axvline(x=percentile_90, color='orange', linestyle='--', label=f'Percentil 90%: {percentile_90:.2f}')
ax2.axvline(x=percentile_85, color='purple', linestyle='--', label=f'Percentil 85%: {percentile_85:.2f}')
ax2.set_title('Histograma de Lead Time')
ax2.set_xlabel('Lead Time')
ax2.set_ylabel('Frequência')
ax2.legend()
ax2.grid(True)

# Ajuste o layout para uma melhor visualização
plt.tight_layout()
plt.show()