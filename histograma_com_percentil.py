import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#Create the data for the histogram. This can be done using numpy:
#data = np.random.randn(1000)
data = pd.read_csv('/users/rodrigoalmeidadeoliveira/documents/dados/lt_data_teste.csv')

#Create the histogram using matplotlib:
n, bins, patches = plt.hist(data, 50, density=True, facecolor='g', alpha=0.75)
#Add the percentile line to the histogram. This can be done by calculating the percentile and then plotting the line:
percentile = np.percentile(data, 95)
percentile2 = np.percentile(data, 85)
plt.axvline(percentile, color='r', linestyle='dashed', linewidth=2)
plt.axvline(percentile2, color='r', linestyle='dashed', linewidth=2)
#plt.scatter(data,data)
#Finally, show the plot:
plt.show()
