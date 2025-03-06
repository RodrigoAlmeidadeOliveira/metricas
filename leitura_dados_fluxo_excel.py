import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as s


# Load the dataset
file_path = '/users/rodrigoalmeidadeoliveira/documents/dados/COMISSIONAMENTO_METRICAS_30092019.xlsx'
#data = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/vazao_teste_nao_ordenado.csv')
df = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
# Calculate the lead time (difference between 'New Backlog' and 'Concluido PRD')
from datetime import datetime

# Convert columns to datetime
df['New Backlog'] = pd.to_datetime(df['New Backlog'], errors='coerce')
df['Concluido PRD'] = pd.to_datetime(df['Concluido PRD'], errors='coerce')

# Calculate lead time in days
df['Lead Time'] = (df['Concluido PRD'] - df['New Backlog']).dt.days

# Calculate average lead time
average_lead_time = df['Lead Time'].mean()

print(f'Average Lead Time: {average_lead_time} days')
print(df.head())

# Calculate the distribution of lead times
distribution = df['Lead Time'].value_counts()

distribution


# Set the aesthetic style of the plots
sns.set_style('whitegrid')

# Plot the distribution of lead times
plt.figure(figsize=(10, 6))
sns.histplot(df['Lead Time'].dropna(), kde=True, bins=30)
plt.title('Distribution of Lead Times')
plt.xlabel('Lead Time (days)')
plt.ylabel('Frequency')
plt.show()



# Plot the scatter distribution of lead times
plt.figure(figsize=(10, 6))
sns.scatterplot(df['Lead Time'].sort_values())
plt.title('Distribution of Lead Times')
plt.xlabel('Lead Time (days)')
plt.ylabel('Frequency')
plt.show()

# Descriptive statistics
print("**Descriptive statistics**")
print(df['Lead Time'].describe())

percentile63 = np.percentile(df['Lead Time'].dropna(), 63)
    
shape, loc, scale = s.weibull_min.fit(df['Lead Time'].dropna(), floc=0)

print("Parâmetro de forma (shape):", shape)
print("Parâmetro de escala (scale):", scale)
print("Percentil 63:", percentile63)

# Identify outliers in the lead time distribution using the IQR method
Q1 = df['Lead Time'].quantile(0.25)
Q3 = df['Lead Time'].quantile(0.75)
IQR = Q3 - Q1

# Define outliers as those beyond 1.5 times the IQR from the Q1 and Q3
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter the dataframe for outliers
outliers = df[(df['Lead Time'] < lower_bound) | (df['Lead Time'] > upper_bound)]

print(f'Lower Bound: {lower_bound}, Upper Bound: {upper_bound}')
print(f'Number of Outliers: {len(outliers)}')
outliers[['Lead Time']].head()

print("\n**Additional statistics**")
print("Média móvel (3 valores):", df['Lead Time'].rolling(window=3).mean().iloc[-1])
print("Moda: "     , format(df['Lead Time'].mode()))
print("Mediana: "  , df['Lead Time'].median())
print("Quartil 1: ", df['Lead Time'].quantile(q=0.25))
print("Quartil 3: ", df['Lead Time'].quantile(q=0.75))
print("Quintil 1: ", df['Lead Time'].quantile(q=0.2))
print("Quintil 3: ", df['Lead Time'].quantile(q=0.8))
print("Decil 1: ", df['Lead Time'].quantile(q=0.1))
print("Decil 9: ", df['Lead Time'].quantile(q=0.9))
print("Percentil 15: ", df['Lead Time'].quantile(q=0.15))
print("Percentil 85: ", df['Lead Time'].quantile(q=0.85))
print("Percentil 95: ", df['Lead Time'].quantile(q=0.95))
print("Amplitude: ", df['Lead Time'].max() - df['Lead Time'].min())
#print("Desvio médio absoluto: ", df['Lead Time'].mean().abs().mean())
print("Variância: ", df['Lead Time'].var())
print("Desvio padrão: ", df['Lead Time'].std())
print("Coeficiente de variação: ", df['Lead Time'].std() / df['Lead Time'].mean())
print("Intervalo inter-quartil: ", df['Lead Time'].quantile(q=0.75) - df['Lead Time'].quantile(q=0.25))



# Filter the dataset for work items with outlier lead times
outlier_work_items = df[df['Lead Time'] > upper_bound]

# Plot the distribution of blocked days for outlier lead times
plt.figure(figsize=(12, 6))
plt.hist(outlier_work_items['Blocked Days'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Blocked Days')
plt.ylabel('Frequency')
plt.title('Distribution of Blocked Days for Outlier Lead Times')
plt.grid(axis='y', alpha=0.75)
plt.show()