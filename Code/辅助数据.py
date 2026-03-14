# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 21:34:43 2025

@author: DELL
"""
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import scipy.stats as stats

result = []
for i in range(36):
    a=40*np.exp(1/np.sqrt(i)) - 40*np.exp(-abs(i-12)/10)
    result.append(a)

fig=plt.figure(figsize=(12,9))
plt.grid()
ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
ax = plt.plot(np.arange(len(result)),result,color='black',linewidth = 3)
plt.title('理想取外卖响应时间分布')
print(result)
