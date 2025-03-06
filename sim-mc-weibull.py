import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as s
import statsmodels.api as sm
import random
from scipy.special import gammaln

# Configurar o estilo dos gráficos
sns.set_style('whitegrid')

# Tamanho do vetor
tamanho = 1000000
vetor = []

# Carregar os dados
df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
data = df['A'].dropna().values.astype(float)

# Ordenar os dados
data_sorted = np.sort(data)

# Calcular os parâmetros Weibull
shape, loc, scale = s.weibull_min.fit(data, floc=0)
percentile63 = np.percentile(data_sorted, 63)

#simulação de monte carlo
print("P63: " , percentile63)
wip_ini = 70
for _ in range(tamanho):
    semanas = 0
    wip = wip_ini
    while wip > 0:
        # Syntax: random.weibullvariate(alpha, beta)
        # Parameters:
        # alpha: scale parameter
        # beta: shape parameter

        numero = round(random.weibullvariate(scale, shape),0)
        wip -= numero
        semanas += 1
    vetor.append(semanas)

# Criar DataFrame para estatísticas descritivas
df_stats = pd.DataFrame(data, columns=["Vazão semanal (itens)"])

# Estatísticas descritivas básicas
desc_stats = df_stats.describe()

# Estatísticas adicionais
additional_stats = {
    "Média móvel (3 valores)": df_stats.rolling(window=3).mean().iloc[-1, 0],
    "Moda": df_stats.mode().iloc[0, 0],
    "Mediana": df_stats.median()[0],
    "Quartil 1": df_stats.quantile(q=0.25)[0],
    "Quartil 3": df_stats.quantile(q=0.75)[0],
    "Quintil 1": df_stats.quantile(q=0.2)[0],
    "Quintil 3": df_stats.quantile(q=0.8)[0],
    "Decil 1": df_stats.quantile(q=0.1)[0],
    "Decil 9": df_stats.quantile(q=0.9)[0],
    "Percentil 15": df_stats.quantile(q=0.15)[0],
    "Percentil 85": df_stats.quantile(q=0.85)[0],
    "Percentil 95": df_stats.quantile(q=0.95)[0],
    "Amplitude": df_stats.max()[0] - df_stats.min()[0],
    "Desvio médio absoluto": df_stats.mad()[0],
    "Variância": df_stats.var()[0],
    "Desvio padrão": df_stats.std()[0],
    "Coeficiente de variação": df_stats.std()[0] / df_stats.mean()[0],
    "Intervalo inter-quartil": df_stats.quantile(q=0.75)[0] - df_stats.quantile(q=0.25)[0],
    "Coeficiente de assimetria": df_stats.skew()[0],
    "Coeficiente de curtose": df_stats.kurt()[0],
}

# Exibir as estatísticas descritivas em uma tela
plt.figure(figsize=(12, 8))
plt.axis('off')
plt.title('Estatísticas Descritivas')
table = plt.table(cellText=desc_stats.values.round(2),
                  rowLabels=desc_stats.index,
                  colLabels=desc_stats.columns,
                  cellLoc='center',
                  loc='center')
table.scale(1.5, 1.5)
plt.show()

# Exibir as estatísticas adicionais
plt.figure(figsize=(12, 8))
plt.axis('off')
plt.title('Estatísticas Adicionais')
table_data = [[key, f"{value:.2f}"] for key, value in additional_stats.items()]
table = plt.table(cellText=table_data, colLabels=["Estatística", "Valor"], cellLoc='center', loc='center')
table.scale(1.5, 1.5)
plt.show()

# Passo 6: Calcular a regressão linear usando statsmodels
n = len(data_sorted)
interval_centers = [(2 * (i + 1) - 3) / (2 * n) for i in range(n)]
interval_centers = np.clip(interval_centers, 1e-10, 1 - 1e-10)
log_data = np.log(data_sorted)
log_minus_log_prob = np.log(-np.log(1 - np.array(interval_centers)))
log_data_with_const = sm.add_constant(log_data)
model = sm.OLS(log_minus_log_prob, log_data_with_const)
results = model.fit()
intercept, slope = results.params
r_squared = results.rsquared
scale_weibull = np.exp(-intercept / slope)
predicted_mean = scale_weibull * np.exp(gammaln(1 + 1 / slope))
actual_mean = np.mean(data_sorted)
median = np.median(data_sorted)
percentile_98 = np.percentile(data_sorted, 98)
percentile_98_to_median = percentile_98 / median

# Exibir os resultados da regressão
print(f'Quantidade de Pontos: {n}')
print(f'Parâmetro Shape: {slope}')
print(f'Parâmetro Scale: {scale_weibull}')
print(f'R-quadrado: {r_squared}')
print(f'Média Prevista: {predicted_mean}')
print(f'Média Real: {actual_mean}')
print(f'Mediana: {median}')
print(f'Percentil 98: {percentile_98}')
print(f'Percentil 98 / Mediana: {percentile_98_to_median}')

# Gerar os gráficos em uma única tela
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Gráfico de dispersão
ax1.scatter(df.index, data, label='Dados', color='blue')
ax1.set_title('Gráfico de Dispersão')
ax1.set_xlabel('Índice')
ax1.set_ylabel('Vazão semanal (itens)')
ax1.legend()

# Histograma
percentile = np.percentile(vetor, 85)
percentile2 = np.percentile(vetor, 15)
ax2.hist(vetor, bins=30, color='blue', edgecolor='black')
ax2.axvline(percentile, color='red', linestyle='dashed', linewidth=2)
ax2.axvline(percentile2, color='green', linestyle='dashed', linewidth=2)
ax2.axvline(np.mean(data_sorted), color='yellow', linestyle='dashed', linewidth=2)
ax2.set_title('Histograma de Vazão Semanal')
ax2.set_xlabel('Semanas')
ax2.set_ylabel('Frequência')
ax2.legend(["P85", "P15", "Média"])

# Ajustar layout e mostrar gráficos
plt.tight_layout()
plt.show()
