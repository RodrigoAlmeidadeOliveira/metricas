import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

#File path

file_path = '/users/rodrigoalmeidadeoliveira/documents/dados/IATEC_ACMS_US.xlsx'

#Load the Excel file

data = pd.ExcelFile(file_path)

#Load the data from the first sheet

df = data.parse('Sheet1')

#Preprocess the data

df['Created Date'] = pd.to_datetime(df['Created Date'])
df['Activated Date'] = pd.to_datetime(df['Activated Date'])
df['Closed Date'] = pd.to_datetime(df['Closed Date'])

#Define a 3-month period (January to March 2023)

start_date = '2023-01-01'
end_date = '2023-03-31'
df_3months = df[(df['Created Date'] >= start_date) & (df['Created Date'] <= end_date)]

#Calculate lead time

df_3months['Lead Time'] = (df_3months['Closed Date'] - df_3months['Created Date']).dt.total_seconds() / (60 * 60 * 24)  # in days

#Group by month and calculate metrics

monthly_analysis = df_3months.groupby(df_3months['Created Date'].dt.to_period('M')).agg(
tasks=('ID', 'size'),
avg_lead_time=('Lead Time', 'mean')
)

#Add demand rate (tasks per day in each month)

monthly_analysis['demand_rate'] = monthly_analysis['tasks'] / monthly_analysis.index.map(
lambda x: x.end_time.day
)

#Function to calculate CONWIP cards

def calculate_optimal_conwip_cards(avg_lead_time, total_tasks):
bottleneck_rate = 1 / avg_lead_time if avg_lead_time > 0 else 0  # Bottleneck rate for the system
critical_wip = bottleneck_rate * avg_lead_time
optimal_conwip_cards = total_tasks  # Using total tasks as a proxy for throughput
return optimal_conwip_cards

#Apply the function to calculate optimal CONWIP cards

monthly_analysis['optimal_conwip_cards'] = monthly_analysis.apply(
lambda row: calculate_optimal_conwip_cards(row['avg_lead_time'], row['tasks']), axis=1
)

#Prepare data for forecasting with linear trend

monthly_analysis['Month_Num'] = range(len(monthly_analysis))  # Create a numerical representation of months
X = monthly_analysis['Month_Num'].values.reshape(-1, 1)
y = monthly_analysis['tasks'].values

#Fit a linear regression model

linear_model = LinearRegression()
linear_model.fit(X, y)

#Forecast for the next 3 months

future_months = np.array(range(len(monthly_analysis), len(monthly_analysis) + 3)).reshape(-1, 1)
forecast_linear = linear_model.predict(future_months)

#Prepare forecasted data

forecast_months_linear = ['2023-04', '2023-05', '2023-06']
forecast_data_linear = pd.DataFrame({'Month': forecast_months_linear, 'Forecasted WIP': forecast_linear})

#Combine actual data with forecasted data for comparison

visualization_data_linear = pd.concat([monthly_analysis[['tasks']].reset_index(), forecast_data_linear], ignore_index=True)
visualization_data_linear.set_index('Month', inplace=True)

#Plot actual WIP and forecasted WIP

plt.figure(figsize=(10, 6))
plt.plot(visualization_data_linear.index[:len(monthly_analysis)], visualization_data_linear['tasks'][:len(monthly_analysis)], marker='o', label='Actual WIP')
plt.plot(visualization_data_linear.index[-3:], visualization_data_linear['Forecasted WIP'][-3:], marker='o', linestyle='--', label='Forecasted WIP (Linear Trend)')
plt.title('Actual and Forecasted WIP (Next 3 Months)')
plt.xlabel('Month')
plt.ylabel('WIP (Tasks)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show()