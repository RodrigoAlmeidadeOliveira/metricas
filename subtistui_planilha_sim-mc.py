import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import random
import scipy.stats as s

# Carregando os dados
# Substitua 'data' com os dados reais a serem usados
data = np.random.rand(100) * 100  # Exemplo temporário, substitua com seus dados reais
# Tamanho do vetor para simulação
tamanho = 1000000
vetor = []

# Lendo os dados do CSV
df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
data = df['A'].dropna().values  # Certifique-se de que não há valores NaN
data = data.astype(float)

# Ajuste dos dados à distribuição Weibull
shape, loc, scale = s.weibull_min.fit(data, floc=0)
print("Parâmetro de forma (shape):", shape)
print("Parâmetro de escala (scale):", scale)

# Configurações iniciais para a simulação
num_trials = 1000000  # Número de simulações (Monte Carlo)
initial_backlog = 50  # Backlog inicial

# Função de simulação Monte Carlo personalizada
def monte_carlo_backlog_custom(tamanho, wip_ini, scale, shape):
    resultados = []
    for _ in range(tamanho):
        semanas = 0
        wip = wip_ini
        while wip > 0:
            # Gera a taxa de conclusão semanal com distribuição Weibull e arredonda
            numero = round(random.weibullvariate(scale, shape), 0)
            wip -= numero
            semanas += 1
        resultados.append(semanas)
    return resultados

# Executa a simulação Monte Carlo para obter o número de semanas de cada simulação
vetor_semanas = monte_carlo_backlog_custom(tamanho=num_trials, wip_ini=initial_backlog, scale=scale, shape=shape)

# Converte os resultados para DataFrame para visualização e análise
df_mc_simulation = pd.DataFrame(vetor_semanas, columns=["Semanas"])

# Cálculo dos percentis de semanas (Percentis - SIM-MC)
percentiles = [50, 85, 95]
df_percentiles = df_mc_simulation.quantile(q=[p/100 for p in percentiles])
df_percentiles.index = [f"P{p}" for p in percentiles]

# Gráfico dos percentis de semanas
plt.figure(figsize=(10, 6))
plt.plot(df_percentiles, marker='o', linestyle='-')
plt.title("Percentis de Conclusão do Backlog")
plt.xlabel("Percentil")
plt.ylabel("Semanas para Concluir o Backlog")
plt.grid(True)
plt.show()

# Resumo: Projeção de prazos de entrega (deadline)
summary = {
    'Backlog Inicial': initial_backlog,
    'Projeção P50 (semanas)': df_percentiles.loc['P50'].values[0],
    'Projeção P85 (semanas)': df_percentiles.loc['P85'].values[0],
    'Projeção P95 (semanas)': df_percentiles.loc['P95'].values[0],
    'Deadline Estimada (P50)': pd.Timestamp.now() + pd.to_timedelta(df_percentiles.loc['P50'].values[0], unit='W'),
    'Deadline Estimada (P85)': pd.Timestamp.now() + pd.to_timedelta(df_percentiles.loc['P85'].values[0], unit='W'),
    'Deadline Estimada (P95)': pd.Timestamp.now() + pd.to_timedelta(df_percentiles.loc['P95'].values[0], unit='W'),
}

# Exibir resumo no console com formatação
print("\nResumo da Simulação de Backlog e Deadlines:")
for key, value in summary.items():
    print(f"{key}: {value}")

# Histograma do número de semanas para completar o backlog em cada simulação
plt.figure(figsize=(12, 6))
sns.histplot(vetor_semanas, bins=15, kde=True)
plt.title("Distribuição do Número de Semanas para Completar o Backlog")
plt.xlabel("Semanas para Completar")
plt.ylabel("Frequência")
plt.grid(True)
plt.show()

# Estatísticas adicionais sobre o número de semanas para completar o backlog
resumo_estatisticas = {
    "Média Semanas para Conclusão": df_mc_simulation["Semanas"].mean(),
    "Mediana Semanas para Conclusão": df_mc_simulation["Semanas"].median(),
    "Desvio Padrão": df_mc_simulation["Semanas"].std(),
    "Mínimo Semanas": df_mc_simulation["Semanas"].min(),
    "Máximo Semanas": df_mc_simulation["Semanas"].max()
}

# Exibir estatísticas agregadas no console com formatação
print("\nEstatísticas do Tempo de Conclusão do Backlog:")
for key, value in resumo_estatisticas.items():
    print(f"{key}: {value}")
