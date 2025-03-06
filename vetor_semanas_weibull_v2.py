from signal import pause
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as s
import random
import seaborn as sns
from scipy.stats import linregress
from scipy.special import gammaln
import statsmodels.api as sm

# Set the aesthetic style of the plots
sns.set_style('whitegrid')

# Tamanho do vetor
tamanho = 1000000
vetor = []

df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
data = df['A'].dropna().values # Certifique-se de que não há valores NaN
data = data.astype(float)
#df = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
# Criar o gráfico de pontos simples
plt.scatter(df.index, data, label='Dados')
data_sorted = np.sort(data)
print(data_sorted)


percentile63 = np.percentile(data_sorted, 63)
    
shape, loc, scale = s.weibull_min.fit(data, floc=0)

print("Parâmetro de forma (shape):", shape)
print("Parâmetro de escala (scale):", scale)


# Create DataFrame
df = pd.DataFrame(data, columns=["Vazão semanal (itens)"])

# Descriptive statistics
print("**Descriptive statistics**")
print(df.describe())

""" print("\n**Additional statistics**")
print(f"Média móvel (3 valores): {df[].rolling(window=3).mean().iloc[-1]}")
print(f"Moda: {df[].mode()[0]}")
print(f"Mediana: {df[].median()}")
print(f"Quartil 1: {df[].quantile(q=0.25)}")
print(f"Quartil 3: {df[].quantile(q=0.75)}")
print(f"Quintil 1: {df[].quantile(q=0.2)}")
print(f"Quintil 3: {df[].quantile(q=0.8)}")
print(f"Decil 1: {df[].quantile(q=0.1)}")
print(f"Decil 9: {df[].quantile(q=0.9)}")
print(f"Percentil 15: {df[].quantile(q=0.15)}")
print(f"Percentil 85: {df[].quantile(q=0.85)}")
print(f"Percentil 95: {df[].quantile(q=0.95)}")
print(f"Amplitude: {df[].max() - df[].min()}")
print(f"Desvio médio absoluto: {df[].mad()}")
print(f"Variância: {df[].var()}")
print(f"Desvio padrão: {df[].std()}")
print(f"Coeficiente de variação: {df[].std() / df[].mean()}")
print(f"Intervalo inter-quartil: {df[].quantile(q=0.75) - df[].quantile(q=0.25)}")
print(f"Coeficiente de assimetria: {df[].skew()}")
print(f"Coeficiente de curtose: {df[].kurt()}") """

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
    #"Desvio médio absoluto": df_stats.mad()[0],
    "Variância": df_stats.var()[0],
    "Desvio padrão": df_stats.std()[0],
    "Coeficiente de variação": df_stats.std()[0] / df_stats.mean()[0],
    "Intervalo inter-quartil": df_stats.quantile(q=0.75)[0] - df_stats.quantile(q=0.25)[0],
    "Coeficiente de assimetria": df_stats.skew()[0],
    "Coeficiente de curtose": df_stats.kurt()[0],

#Coeficiente de assimetria: Mede a assimetria dos dados. Um valor positivo indica assimetria positiva, ou seja, 
# a cauda direita dos dados é mais longa do que a cauda esquerda. Um valor negativo indica assimetria negativa, ou seja, 
# a cauda esquerda dos dados é mais longa do que a cauda direita.
    "Coeficiente de assimetria: ": df_stats.skew(),

#Coeficiente de curtose: Mede a achatamento dos dados. Um valor positivo indica dados mais achatados do que a distribuição normal.
# Um valor negativo indica dados mais pontiagudos do que a distribuição norma
    "Coeficiente de curtose: ": df_stats.kurt(),
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
    ##print(vetor[i])


#linhas = 100
#colunas = 100

# Inicializando uma matriz vazia
#matriz = np.empty((linhas, colunas), dtype=float)
#i=0; j=0;
# Preenchendo a matriz com valores float
#for i in range(linhas):
#     for j in range(colunas):
#         matriz[i, j] = np.percentile(vetor, 100-i)

#print("Dados da matriz")
#percentile = np.percentile(matriz, 85)
#plt.hist(matriz, bins=range(1, max(matriz) + 2), color='blue', edgecolor='black')
#sns.histplot(vetor.dropna(), kde=True, bins=30)


percentile = np.percentile(vetor, 85)
percentile2 = np.percentile(vetor, 15)

# Descriptive statistics
print("**Descriptive statistics** - Vetor")
print(s.describe(vetor))
print("**Descriptive statistics** - Dados lidos")
print(s.describe(data))

## print median, average, max
print("median")
print(np.median(vetor))
print("average")
print(np.mean(vetor))
print("max")
print(np.max(vetor))

## print median, average, max

print("Considerando que tenho um período de tempo, quantos itens de trabalho provavelmente serão concluídos neste período?")
print("P15%")
print(np.percentile(vetor, 15))
print("P85%")
print(np.percentile(vetor, 85))




# Passo 2: Ordenar os dados em ordem crescente
print('# Passo 2: Ordenar os dados em ordem crescente')
df = data.astype(float)
df = np.sort(df)
print(df)
data_sorted = np.sort(data)
print(data_sorted)

# Converter os dados para o tipo numérico
data = data.astype(float)

# Passo 2: Ordenar os dados em ordem crescente
data_sorted = np.sort(data)

# Exibir o conteúdo de data_sorted
print("Conteúdo de data_sorted:")
print(data_sorted)

# Passo 3: Calcular os centros dos intervalos
n = len(data_sorted)
interval_centers = [(2 * (i + 1) - 3) / (2 * n) for i in range(n)]  # Corrigido para i + 1

# Evitar valores exatamente 0 ou 1
interval_centers = np.clip(interval_centers, 1e-10, 1 - 1e-10)

# Passo 4: Calcular os logaritmos naturais dos dados
log_data = np.log(data_sorted)

# Passo 5: Linearizar a função de distribuição cumulativa
log_minus_log_prob = np.log(-np.log(1 - np.array(interval_centers)))

# Garantir que os arrays sejam unidimensionais
log_data = np.ravel(log_data)
log_minus_log_prob = np.ravel(log_minus_log_prob)

# Verificar o tamanho dos arrays
print(f'Tamanho de log_data: {len(log_data)}')
print(f'Tamanho de log_minus_log_prob: {len(log_minus_log_prob)}')

# Verificar se os arrays são unidimensionais
print(f'log_data é unidimensional: {log_data.ndim == 1}')
print(f'log_minus_log_prob é unidimensional: {log_minus_log_prob.ndim == 1}')

# Adicionar uma constante (intercepto) para a regressão
log_data_with_const = sm.add_constant(log_data)

# Passo 6: Calcular a regressão linear usando statsmodels
model = sm.OLS(log_minus_log_prob, log_data_with_const)
results = model.fit()

# Extrair os parâmetros da regressão
intercept, slope = results.params

# Calcular o R-quadrado
r_squared = results.rsquared

# Passo 8: Calcular o parâmetro scale
scale = np.exp(-intercept / slope)

# Passo 9: Comparar a média prevista com a média real
predicted_mean = scale * np.exp(gammaln(1 + 1 / slope))
actual_mean = np.mean(data_sorted)

# Cálculo da mediana e percentil 98
median = np.median(data_sorted)
percentile_98 = np.percentile(data_sorted, 98)
percentile_98_to_median = percentile_98 / median

# Exibir os resultados
print(f'Quantidade de Pontos: {n}')
print(f'Parâmetro Shape: {slope}')
print(f'Parâmetro Scale: {scale}')
print(f'R-quadrado: {r_squared}')
print(f'Média Prevista: {predicted_mean}')
print(f'Média Real: {actual_mean}')
print(f'Mediana: {median}')
print(f'Percentil 98: {percentile_98}')
print(f'Percentil 98 / Mediana: {percentile_98_to_median}')

# Adicionar rótulos aos eixos
#plt.xlabel('Índice')
#plt.ylabel('Valores')

# Adicionar uma legenda
#plt.legend()

# Adicionar um título ao gráfico
#plt.title('Gráfico de Pontos Simples')

# Mostrar o gráfico
#plt.tight_layout()
#plt.show()
 
plt.hist(vetor, bins=range(1, max(vetor) + 2), color='blue', edgecolor='black')

# plt.hist(vetor, bins=200, color='blue', edgecolor='black')
print("Dados da simulação")

print("P85: ", percentile)
print("P15: ", percentile2)
plt.axvline(percentile, color='r', linestyle='dashed', linewidth=2)
plt.axvline(percentile2, color='g', linestyle='dashed', linewidth=2)
plt.axvline(np.mean(vetor), color='y', linestyle='dashed', linewidth=2)
plt.xlabel('Semanas')
plt.ylabel('Frequência')
plt.title('Histograma de Semanas para Reduzir WIP a Zero - Weibull \n WIP = '+ str(wip_ini)+ "\n P85: " +str(percentile)+ " P15: " +str(percentile2) )
plt.legend(["P85 red -- P15 green -- Média yellow"])

plt.grid(True)
plt.tight_layout()
plt.show()