import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as s
import random
import seaborn as sns
from scipy.stats import linregress
from scipy.special import gammaln
import statsmodels.api as sm


# Obter a hora atual
hora_inicio = datetime.datetime.now()

# Imprimir a hora de início
print("O programa iniciou em:", hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))

# Configurando o estilo estético dos gráficos
sns.set_style('whitegrid')

# Tamanho do vetor para simulação
tamanho = 1000000
vetor = []

# Lendo os dados do CSV
df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
data = df['A'].dropna().values  # Certifique-se de que não há valores NaN
data = data.astype(float)

# Criar o gráfico de dispersão
plt.scatter(df.index, data, label='Dados')

# Ordenando os dados para o cálculo de percentis
data_sorted = np.sort(data)
print(data_sorted)

# Cálculo do percentil 63
percentile63 = np.percentile(data_sorted, 63)

# Ajuste dos dados a uma distribuição Weibull
shape, loc, scale = s.weibull_min.fit(data, floc=0)
print("Parâmetro de forma (shape):", shape)
print("Parâmetro de escala (scale):", scale)

# Criar DataFrame com as estatísticas descritivas
df_stats = pd.DataFrame(data, columns=["Vazão semanal (itens)"])
print("**Estatísticas descritivas**")
print(df_stats.describe())

# Estatísticas adicionais
additional_stats = {
    "Média móvel (3 valores)": df_stats.rolling(window=3).mean().iloc[-1, 0],
    "Moda": df_stats.mode().iloc[0, 0],
    "Mediana": df_stats.median().iloc[0],
    "Quartil 1": df_stats.quantile(q=0.25).iloc[0],
    "Quartil 3": df_stats.quantile(q=0.75).iloc[0],
    "Quintil 1": df_stats.quantile(q=0.2).iloc[0],
    "Quintil 3": df_stats.quantile(q=0.8).iloc[0],
    "Decil 1": df_stats.quantile(q=0.1).iloc[0],
    "Decil 9": df_stats.quantile(q=0.9).iloc[0],
    "Percentil 15": df_stats.quantile(q=0.15).iloc[0],
    "Percentil 85": df_stats.quantile(q=0.85).iloc[0],
    "Amplitude": df_stats.max().iloc[0] - df_stats.min().iloc[0],
    "Desvio médio absoluto":  (df_stats - df_stats.mean()).abs().mean().iloc[0],
    "Variância": df_stats.var().iloc[0],
    "Desvio padrão": df_stats.std().iloc[0],
    "Coeficiente de variação": df_stats.std().iloc[0] / df_stats.mean().iloc[0],
    "Intervalo inter-quartil": df_stats.quantile(q=0.75).iloc[0] - df_stats.quantile(q=0.25).iloc[0],
    "Coeficiente de assimetria": df_stats.skew().iloc[0],
    "Coeficiente de curtose": df_stats.kurt().iloc[0],
}

# Exibindo as estatísticas descritivas em forma de tabela
plt.figure(figsize=(12, 8))
plt.axis('off')
plt.title('Estatísticas Descritivas')
table = plt.table(cellText=df_stats.describe().values.round(2),
                  rowLabels=df_stats.describe().index,
                  colLabels=df_stats.describe().columns,
                  cellLoc='center',
                  loc='center')
table.scale(2, 1.5)
plt.show()

# Simulação de Monte Carlo
print("P63: ", percentile63)
wip_ini = 70
for _ in range(tamanho):
    semanas = 0
    wip = wip_ini
    while wip > 0:
        numero = round(random.weibullvariate(scale, shape), 0)
        wip -= numero
        semanas += 1
    vetor.append(semanas)

# Cálculo dos percentis P85 e P15
percentile = np.percentile(vetor, 85)
percentile2 = np.percentile(vetor, 15)

# Estatísticas descritivas do vetor simulado
print("**Estatísticas descritivas** - Vetor")
print(s.describe(vetor))
print("**Estatísticas descritivas** - Dados lidos")
print(s.describe(data))

# Exibição de resultados
print("Mediana:", np.median(vetor))
print("Média:", np.mean(vetor))
print("Máximo:", np.max(vetor))

# Exibir percentis e previsões
print("P15:", np.percentile(vetor, 15))
print("P85:", np.percentile(vetor, 85))

# Passo 2: Ordenar os dados em ordem crescente
data_sorted = np.sort(data)

# Passo 3: Calcular os centros dos intervalos e logaritmos
n = len(data_sorted)
interval_centers = [(2 * (i + 1) - 3) / (2 * n) for i in range(n)]
interval_centers = np.clip(interval_centers, 1e-10, 1 - 1e-10)

# Logaritmos naturais dos dados
log_data = np.log(data_sorted)
log_minus_log_prob = np.log(-np.log(1 - np.array(interval_centers)))

# Adicionar constante para regressão
log_data_with_const = sm.add_constant(log_data)

# Regressão linear
model = sm.OLS(log_minus_log_prob, log_data_with_const)
results = model.fit()

# Parâmetros da regressão
intercept, slope = results.params
r_squared = results.rsquared
scale = np.exp(-intercept / slope)
predicted_mean = scale * np.exp(gammaln(1 + 1 / slope))
actual_mean = np.mean(data_sorted)

# Exibir os resultados
median = np.median(data_sorted)
percentile_98 = np.percentile(data_sorted, 98)
percentile_98_to_median = percentile_98 / median

print(f'Parâmetro Shape: {slope}')
print(f'Parâmetro Scale: {scale}')
print(f'R-quadrado: {r_squared}')
print(f'Média Prevista: {predicted_mean}')
print(f'Média Real: {actual_mean}')
print(f'Mediana: {median}')
print(f'Percentil 98: {percentile_98}')
print(f'Percentil 98 / Mediana: {percentile_98_to_median}')

# Obter a hora atual
hora_fim= datetime.datetime.now()

# Imprimir a hora de início
print("O programa terminou em:", hora_fim.strftime("%Y-%m-%d %H:%M:%S"))



# Histograma de semanas simuladas
#plt.hist(vetor, bins=range(1, max(vetor) + 2), color='blue', edgecolor='black')
plt.hist(vetor, color='blue', edgecolor='black')
plt.axvline(percentile, color='r', linestyle='dashed', linewidth=2)
plt.axvline(percentile2, color='g', linestyle='dashed', linewidth=2)
plt.axvline(np.mean(vetor), color='y', linestyle='dashed', linewidth=2)
plt.xlabel('Semanas')
plt.ylabel('Frequência')
plt.title('Histograma de Semanas para Reduzir WIP a Zero - Weibull\n WIP = ' + str(wip_ini) + "\n P85: " + str(percentile) + " P15: " + str(percentile2))
plt.legend(["P85 (vermelho) -- P15 (verde) -- Média (amarelo)"])
plt.grid(True)
plt.tight_layout()
plt.show()
