import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file into a pandas DataFrame
data_df = pd.read_excel('/users/rodrigoalmeidadeoliveira/documents/dados/lt_data_teste_v2.xls')

# Create scatter plot
plt.scatter(data_df['numid'], data_df['lt'])

# Calculate percentile lines
percentiles = [10, 50, 85, 95]

# Plot percentile lines
for p in percentiles:
    x_p = data_df['numid'].quantile(p/100)
    y_p = data_df['lt'].quantile(p/100)
    plt.axvline(x=x_p, color='red', linestyle='--', alpha=0.5)
    plt.axhline(y=y_p, color='red', linestyle='--', alpha=0.5)
    plt.text(x_p, y_p, f'{p}%', color='red')

# Add plot labels and title
plt.xlabel('X label')
plt.ylabel('Y label')
plt.title('Scatter plot with percentile lines')

# Show plot
plt.show()

