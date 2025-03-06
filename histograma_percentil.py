import pandas as pd
import matplotlib.pyplot as plt

# Read in the csv file
#data = pd.read_csv('file.csv')
data = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/lt_data_teste.csv')

# Create the histogram
percentile = 85
data.hist(bins=20)

percentile = plt.percentile(data, 95)
percentile2 = plt.percentile(data, 85)
plt.axvline(percentile, color='r', linestyle='dashed', linewidth=2)
plt.axvline(percentile2, color='r', linestyle='dashed', linewidth=2)

#plt.hist(data)
plt.scatter()
#plt.axvline(x=data.quantile(q=percentile/100), color='r', linestyle='dashed', linewidth=2)

# Create the scatter plot
#plt.scatter(data['col1'], data['col2'])
#plt.scatter(data['col1'])

