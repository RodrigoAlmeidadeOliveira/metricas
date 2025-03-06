import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Função para gerar uma planilha de exemplo com dados de lead time usando distribuição Weibull
def generate_example_data_weibull(filename='lead_time_data.csv', num_samples=100, shape=1.5, scale=10):
    # Gerar dados de exemplo com distribuição Weibull parametrizável
    weibull_samples = np.random.weibull(a=shape, size=num_samples) * scale
    weibull_samples = np.clip(weibull_samples, 1, None)  # Garantir que o lead time não seja menor que 1
    df = pd.DataFrame(weibull_samples, columns=['lead_time'])
    df.to_csv(filename, index=False)
    print(f"Arquivo de exemplo '{filename}' gerado com sucesso.")

# Função para simulação de Monte Carlo com ajuste de esforço paralelo
def monte_carlo_forecast(filename, num_simulations=1000000, num_work_items=10, target_forecast_days=50, tolerance=0.5):
    # Carregar os dados de lead time do arquivo CSV
    lead_time_data = pd.read_csv(filename)['lead_time']
    
    # Inicialização do esforço paralelo
    parallel_effort = 1
    diff = float('inf')  # Inicializa a diferença entre o percentil 85 e o alvo
    adjustment_factor = 0.1  # Fator de ajuste para o parallel_effort
    
    while abs(diff) > tolerance:
        # Listas para armazenar resultados das simulações
        total_days = []
        
        # Realizar simulações
        for _ in range(num_simulations):
            # Amostra aleatória de tempos de ciclo para cada item de trabalho
            sample = np.random.choice(lead_time_data, num_work_items, replace=True)
            # Soma dos tempos de ciclo e divisão pelo esforço paralelo
            days_to_complete = np.sum(sample) / parallel_effort
            total_days.append(days_to_complete)
        
        # Calcular o percentil 85 das simulações
        percentile_85 = np.percentile(total_days, 85)
        diff = percentile_85 - target_forecast_days
        
        # Ajuste do esforço paralelo
        if diff > 0:
            parallel_effort += adjustment_factor
        else:
            parallel_effort -= adjustment_factor
        
        print(f"Ajustando parallel_effort para {parallel_effort:.2f}, percentil 85: {percentile_85:.2f}, diferença: {diff:.2f}")

    # Percentis adicionais para o gráfico final
    percentile_15 = np.percentile(total_days, 15)
    percentile_50 = np.percentile(total_days, 50)
    percentile_95 = np.percentile(total_days, 95)
    
    print(f"\nEsforço paralelo final ajustado: {parallel_effort:.2f}")
    print(f"Média de dias para completar: {np.mean(total_days):.2f}")
    print(f"Percentil 15: {percentile_15:.2f}")
    print(f"Percentil 50 (mediana): {percentile_50:.2f}")
    print(f"Percentil 85 (target): {percentile_85:.2f}")
    print(f"Percentil 95: {percentile_95:.2f}")
    
    # Visualização dos resultados com histograma e linhas para percentis
    plt.hist(total_days, bins=30, color='skyblue', edgecolor='black')
    plt.axvline(percentile_15, color='orange', linestyle='dashed', linewidth=1.5, label='15th Percentile')
    plt.axvline(percentile_50, color='green', linestyle='dashed', linewidth=1.5, label='50th Percentile (Median)')
    plt.axvline(percentile_85, color='purple', linestyle='dashed', linewidth=1.5, label='85th Percentile (Target)')
    plt.axvline(percentile_95, color='red', linestyle='dashed', linewidth=1.5, label='95th Percentile')
    
    plt.title('Distribuição de Dias para Completar (Simulação Monte Carlo)')
    plt.xlabel('Dias para Completar')
    plt.ylabel('Frequência')
    plt.legend()
    plt.show()

# Gerar arquivo de exemplo com distribuição Weibull
generate_example_data_weibull(shape=1.5, scale=10)

# Executar simulação com ajuste para target de 50 dias no percentil 85
monte_carlo_forecast('lead_time_data.csv', target_forecast_days=50)

