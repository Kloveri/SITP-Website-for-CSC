# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 00:05:13 2025

@author: DELL
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

r'''
breakfast_rail_df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\B.csv",header=0,encoding='utf-8')
index = breakfast_rail_df[breakfast_rail_df['Speed'] == 0].index
breakfast_rail_df = breakfast_rail_df.drop(breakfast_rail_df.index[index])
breakfast_rail_df['RealSpeed'] = (breakfast_rail_df['Distance'] - 100)/(breakfast_rail_df['TimeOD']-60)*3.6
index = breakfast_rail_df[breakfast_rail_df['RealSpeed']<0.5].index
index1 =  breakfast_rail_df[breakfast_rail_df['RealSpeed']==np.inf].index
breakfast_rail_df.loc[index , 'RealSpeed'] = breakfast_rail_df.loc[index,'Speed']
breakfast_rail_df.loc[index1 , 'RealSpeed'] = breakfast_rail_df.loc[index1,'Speed']
breakfast_rail_df.to_csv(r"C:\Users\DELL\Desktop\新数据\B.csv")
'''
breakfast_rail_df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\B.csv",header=0,encoding='utf-8')
breakfast_rail_df = breakfast_rail_df[breakfast_rail_df['Which'] == 'Go']
data = breakfast_rail_df['RealSpeed']

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(12,9))
plt.grid()
ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
ax = sns.histplot(data = breakfast_rail_df , x='RealSpeed',bins=250, stat = 'density',color='white')
sns.kdeplot(data = breakfast_rail_df , x='RealSpeed',bw=0.11,color = 'black' ,linewidth = 3,linestyle='--')
plt.plot([5,5],[0,0.25],linestyle='-.',color='gray',linewidth=3)
plt.plot([8.5,8.5],[0,0.25],linestyle='-.',color='gray',linewidth=3)
plt.plot([12.5,12.5],[0,0.25],linestyle='-.',color='gray',linewidth=3)


for i in range(12):
    ax.patches[i].set_hatch('/')
    ax.patches[i].set_linewidth(1)
for i in range(12,20):
    ax.patches[i].set_hatch('.')
    ax.patches[i].set_linewidth(1)
for i in range(20,30):
    ax.patches[i].set_hatch('-')
    ax.patches[i].set_linewidth(1)
for i in range(30,len(ax.patches)):
    ax.patches[i].set_hatch('')
    ax.patches[i].set_linewidth(1)
handles = [mpatches.Patch(facecolor=['white','white','white','white'][i], edgecolor='black', hatch=['/', '.','-',''][i]) for i in range(4)]
ax.legend(handles, ['步行','自行车（慢速）','自行车（快速）','电动车'], loc='upper center', bbox_to_anchor=(0.8, 1), ncol=2, frameon=False)
plt.xlabel('路途速度')
plt.ylabel('分布密度')
plt.xlim(0,20)

print(len(breakfast_rail_df[breakfast_rail_df['RealSpeed']<=5])/len(breakfast_rail_df))
print((len(breakfast_rail_df[breakfast_rail_df['RealSpeed']<=8.5])-len(breakfast_rail_df[breakfast_rail_df['RealSpeed']<=5]))/len(breakfast_rail_df))
print((len(breakfast_rail_df[breakfast_rail_df['RealSpeed']<=15])-len(breakfast_rail_df[breakfast_rail_df['RealSpeed']<=8.5]))/len(breakfast_rail_df))
print((len(breakfast_rail_df)-len(breakfast_rail_df[breakfast_rail_df['RealSpeed']<=15]))/len(breakfast_rail_df))
print(len(breakfast_rail_df))