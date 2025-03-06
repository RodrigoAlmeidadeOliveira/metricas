import matplotlib.pyplot as plt

# Dados de exemplo (percentual de custo e percentual de avanço)
projetos = ['Projeto A', 'Projeto B', 'Projeto C', 'Projeto D', 'Projeto E']
custo = [20, 30, 25, 35, 40]  # Percentual de custo
avanco = [10, 15, 20, 25, 30]  # Percentual de avanço

# Criando o gráfico
plt.figure(figsize=(10, 6))

# Plotando o percentual de custo
plt.scatter(custo, range(len(projetos)), color='red', label='% de custo')

# Plotando o percentual de avanço
plt.scatter(avanco, range(len(projetos)), color='green', label='% de avanço')

# Adicionando labels aos pontos
for i, txt in enumerate(projetos):
    plt.annotate(txt, (custo[i], i), textcoords="offset points", xytext=(10,0), ha='center')

# Configurando o gráfico
plt.xlabel('% de custo / % de avanço')
plt.ylabel('Projetos')
plt.title('Gráfico Fever - Custo vs Avanço de Projetos')
plt.grid(True)
plt.legend()

# Exibindo o gráfico
plt.show()