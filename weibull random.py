import random  
import matplotlib.pyplot as plt  
    
nums = []  
alpha = 1
beta = 1.5
    
for i in range(10000):  
    temp = random.weibullvariate(alpha, beta)  
    nums.append(temp)  
        
plt.hist(nums, bins = 200)  
plt.show() 