import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from scipy.stats import skew

# Carregar o arquivo Excel
def process_and_plot(file_path):
    # Carregar os dados
    data = pd.ExcelFile(file_path)
    sheet_data = data.parse(sheet_name='Sheet1')

    # Converter as datas para datetime
    sheet_data["Activated Date"] = pd.to_datetime(sheet_data["Activated Date"])
    sheet_data["Closed Date"] = pd.to_datetime(sheet_data["Closed Date"])

    # Calcular o Lead Time em dias
    sheet_data["Lead Time"] = (sheet_data["Closed Date"] - sheet_data["Activated Date"]).dt.total_seconds() / 86400

    # Calcular o Throughput (tarefas fechadas por dia)
    throughput_data = sheet_data.groupby(sheet_data["Closed Date"].dt.date).size()
  
           
    # Preparar dados para gráficos Lead Time
    lead_time_data = sheet_data["Lead Time"].dropna()
    lead_time_mean = lead_time_data.mean()
    lead_time_moving_range = lead_time_data.diff().abs().dropna()
    lead_time_average_moving_range = lead_time_moving_range.mean()
    lead_time_ucl = lead_time_mean + 2.66 * lead_time_average_moving_range
    lead_time_lcl = max(lead_time_mean - 2.66 * lead_time_average_moving_range, 0)
    #print(lead_time_data)
    
    # Preparar dados para gráficos Throughput
    throughput_mean = throughput_data.mean()
    throughput_moving_range = throughput_data.diff().abs().dropna()
    throughput_average_moving_range = throughput_moving_range.mean()
    throughput_ucl = throughput_mean + 2.66 * throughput_average_moving_range
    throughput_lcl = max(throughput_mean - 2.66 * throughput_average_moving_range, 0)

   # Calcular o Lead Time em dias
    sheet_data["Lead Time"] = (sheet_data["Closed Date"] - sheet_data["Created Date"]).dt.total_seconds() / 86400

    # Calcular o Throughput (tarefas fechadas por dia)
    throughput_data = sheet_data.groupby(sheet_data["Closed Date"].dt.date).size()

    # Dados para WIP
    sheet_data['Inicio'] = sheet_data['Created Date']
    sheet_data['Fim'] = sheet_data['Closed Date']
    sheet_data['Inicio'] = sheet_data['Inicio'].dt.floor('D')
    sheet_data['Fim'] = sheet_data['Fim'].dt.floor('D')
    all_dates = pd.date_range(start=sheet_data['Inicio'].min(), end=sheet_data['Fim'].max(), freq='D')
    wip = pd.Series(index=all_dates, data=0)
    for _, row in sheet_data.iterrows():
        for single_date in pd.date_range(start=row['Inicio'], end=row['Fim'], freq='D'):
            if single_date in wip.index:
                wip[single_date] += 1
                
    #print(wip.values)
    # Preparar dados para gráficos WIP
    wip_mean = wip.mean()
    wip_moving_range = wip.diff().abs().dropna()
    wip_average_moving_range = wip_moving_range.mean()
    wip_ucl = wip_mean + 2.66 * wip_average_moving_range
    wip_lcl = max(wip_mean - 2.66 * wip_average_moving_range, 0)

    # Criar os gráficos em uma única tela
    fig, axs = plt.subplots(2, 1, figsize=(15, 10))

    # Gráfico Xbar - WIP
    axs[0].plot(wip.index, wip.values, marker='o', label='WIP')
    axs[0].axhline(wip_mean, color='blue', linestyle='--', label='Média (X̄)')
    axs[0].axhline(wip_ucl, color='red', linestyle='--', label='Limite Superior (UCL)')
    axs[0].axhline(wip_lcl, color='green', linestyle='--', label='Limite Inferior (LCL)')
    axs[0].set_title('Gráfico Xbar - WIP')
    axs[0].set_xlabel('Data')
    axs[0].set_ylabel('Trabalho em Progresso (WIP)')
    axs[0].legend()
    axs[0].grid(alpha=0.5)
    axs[0].xaxis.set_major_locator(mdates.DayLocator(interval=30))
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    axs[0].tick_params(axis='x', rotation=45)

    # Gráfico MRbar - WIP
    axs[1].plot(wip_moving_range.index, wip_moving_range.values, marker='o', label='Amplitude Móvel (MR)')
    axs[1].axhline(wip_average_moving_range, color='blue', linestyle='--', label='Média (MR̄)')
    axs[1].axhline(wip_average_moving_range + 3.27 * wip_average_moving_range, color='red', linestyle='--', label='Limite Superior (UCL-MR)')
    axs[1].set_title('Gráfico MRbar - WIP')
    axs[1].set_xlabel('Data')
    axs[1].set_ylabel('Amplitude Móvel (MR)')
    axs[1].legend()
    axs[1].grid(alpha=0.5)
    axs[1].xaxis.set_major_locator(mdates.DayLocator(interval=30))
    axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    axs[1].tick_params(axis='x', rotation=45)

    # Dados para histograma e estatísticas
    case_durations_days = sheet_data['Lead Time'].values
    #moda_series = pd.Series(case_durations_days).mode().iloc[0, 0]
    moda_series = sheet_data['Lead Time'].mode()
    average_lt= pd.Series(case_durations_days).mean()
    mediana_lt= pd.Series(case_durations_days).median()
    if not moda_series.empty:
        moda = moda_series[0]
        count = (case_durations_days == moda).sum()
    else:
        moda = None
        count = None
    skewness = skew(case_durations_days)
    percentiles = [15, 25, 50, 75, 85]
    percentile_values = np.percentile(case_durations_days, percentiles)
    p85 = percentile_values[-1]
    p15 = percentile_values[-4]

  # Gerar histograma
    plt.figure(figsize=(10, 6))
    plt.hist(case_durations_days, bins=30, color='blue', alpha=0.7, label='Lead Times')
    #if not moda_series.empty:
    #    plt.axvline(x=moda, color='red', linestyle='dashed', linewidth=2, label=f'Moda: {moda}')
    plt.axvline(x=p85, color='green', linestyle='dashed', linewidth=2, label=f'P85: {p85:.2f}')
    plt.axvline(x=p15, color='yellow', linestyle='dashed', linewidth=2, label=f'P15: {p15:.2f}')
    plt.axvline(x=average_lt, color='black', linestyle='dashed', linewidth=2, label=f'Média: {average_lt:.2f}')
    plt.axvline(x=mediana_lt, color='blue', linestyle='dashed', linewidth=2, label=f'Mediana: {mediana_lt:.2f}')
    plt.title('Histograma de Lead Times')
    plt.xlabel('Lead Time (dias)')
    plt.ylabel('Frequência')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    # Dados para CFD
    started = pd.Series(index=all_dates, data=0)
    finished = pd.Series(index=all_dates, data=0)
    for _, row in sheet_data.iterrows():
        if row['Inicio'] in started.index:
            started[row['Inicio']] += 1
        if row['Fim'] in finished.index:
            finished[row['Fim']] += 1
    cum_started = started.cumsum()
    cum_finished = finished.cumsum()

    # Criar os gráficos em uma única tela
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))

    # Gráfico Xbar - Lead Time
    axs[0, 0].plot(lead_time_data.index, lead_time_data, marker='o', label='Lead Time')
    axs[0, 0].axhline(lead_time_mean, color='blue', linestyle='--', label='Média (X̄)')
    axs[0, 0].axhline(lead_time_ucl, color='red', linestyle='--', label='Limite Superior (UCL)')
    axs[0, 0].axhline(lead_time_lcl, color='green', linestyle='--', label='Limite Inferior (LCL)')
    axs[0, 0].set_title('Gráfico Xbar - Lead Time')
    axs[0, 0].set_xlabel('Índice de Observação')
    axs[0, 0].set_ylabel('Lead Time (dias)')
    axs[0, 0].legend()
    axs[0, 0].grid(alpha=0.5)

    # Gráfico MRbar - Lead Time
    axs[0, 1].plot(lead_time_moving_range.index, lead_time_moving_range, marker='o', label='Amplitude Móvel (MR)')
    axs[0, 1].axhline(lead_time_average_moving_range, color='blue', linestyle='--', label='Média (MR̄)')
    axs[0, 1].axhline(lead_time_average_moving_range + 3.27 * lead_time_average_moving_range, color='red', linestyle='--', label='Limite Superior (UCL-MR)')
    axs[0, 1].set_title('Gráfico MRbar - Lead Time')
    axs[0, 1].set_xlabel('Índice de Observação')
    axs[0, 1].set_ylabel('Amplitude Móvel (MR)')
    axs[0, 1].legend()
    axs[0, 1].grid(alpha=0.5)

    # Gráfico Xbar - Throughput
    axs[1, 0].plot(throughput_data.index, throughput_data, marker='o', label='Throughput')
    axs[1, 0].axhline(throughput_mean, color='blue', linestyle='--', label='Média (X̄)')
    axs[1, 0].axhline(throughput_ucl, color='red', linestyle='--', label='Limite Superior (UCL)')
    axs[1, 0].axhline(throughput_lcl, color='green', linestyle='--', label='Limite Inferior (LCL)')
    axs[1, 0].set_title('Gráfico Xbar - Throughput')
    axs[1, 0].set_xlabel('Data de Fechamento')
    axs[1, 0].set_ylabel('Throughput (tarefas/dia)')
    axs[1, 0].legend()
    axs[1, 0].grid(alpha=0.5)

    # Gráfico MRbar - Throughput
    axs[1, 1].plot(throughput_moving_range.index, throughput_moving_range, marker='o', label='Amplitude Móvel (MR)')
    axs[1, 1].axhline(throughput_average_moving_range, color='blue', linestyle='--', label='Média (MR̄)')
    axs[1, 1].axhline(throughput_average_moving_range + 3.27 * throughput_average_moving_range, color='red', linestyle='--', label='Limite Superior (UCL-MR)')
    axs[1, 1].set_title('Gráfico MRbar - Throughput')
    axs[1, 1].set_xlabel('Data de Fechamento')
    axs[1, 1].set_ylabel('Amplitude Móvel (MR)')
    axs[1, 1].legend()
    axs[1, 1].grid(alpha=0.5)

    # Gráfico WIP
    axs[2, 0].plot(wip.index, wip.values, color='blue')
    axs[2, 0].set_title('Trabalho em Progresso ao Longo do Tempo (WIP)')
    axs[2, 0].set_xlabel('Data')
    axs[2, 0].set_ylabel('Trabalho em Progresso (WIP)')
    axs[2, 0].grid(True)
    axs[2, 0].xaxis.set_major_locator(mdates.DayLocator(interval=60))
    axs[2, 0].tick_params(axis='x', rotation=45)
    axs[2, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Gráfico CFD
    axs[2, 1].fill_between(cum_started.index, cum_started.values, color='blue', step='post', alpha=0.5, label='WIP')
    axs[2, 1].fill_between(cum_finished.index, cum_finished.values, color='green', step='post', alpha=0.5, label='Done')
    axs[2, 1].set_title('Diagrama de Fluxo Cumulativo (CFD)')
    axs[2, 1].set_xlabel('Data')
    axs[2, 1].set_ylabel('Quantidade Acumulada')
    axs[2, 1].legend()
    axs[2, 1].grid(True)
    axs[2, 1].xaxis.set_major_locator(mdates.DayLocator(interval=30))
    axs[2, 1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    axs[2, 1].tick_params(axis='x', rotation=45)
    
    

    plt.tight_layout()
    plt.show()

# Exemplo de uso
def main():
    file_path = '/users/rodrigoalmeidadeoliveira/documents/dados/dados_wip_Lead_time.xlsx'  # Substitua pelo caminho correto do arquivo
    process_and_plot(file_path)

if __name__ == "__main__":
    main()
