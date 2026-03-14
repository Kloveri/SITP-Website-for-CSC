# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 14:29:01 2025

@author: DELL
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(12,9))
plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
index = ['校内就餐','校外就餐','外卖就餐']
plt.xticks(fontproperties = 'SimHei')
plt.yticks(fontproperties = 'Times New Roman')

def add_lists(list1, list2):
    result = [list1[i] + list2[i] for i in range(len(list1))]
    return result

br = [20.800 , 1.020 , 1.010]
lu = [47.318 , round(4.090+(10.456+7.330+6.423)*4.090/(4.090+1.496) , 3) , round(1.496+(10.456+7.330+6.423)*1.496/(4.090+1.496) , 3)]
di = [40.420 , round(6.393+(11.471+9.760+6.164)*6.393/(6.393+2.636) , 3) , round(2.636+(11.471+9.760+6.164)*2.636/(6.393+2.636) , 3)]

br1 = [5.666 , 0.821 , 0.720]
lu1 = [13.024 ,7.788 , round(0.445 + (3.513 + 2.551  +1.681)*0.445/(1.672 +  0.445),3)]
di1 = [10.537 , round(2.418+(4.003+3.395+1.735)*2.418/(2.418+0.798),3) , round(0.798+(4.003+3.395+1.735)*0.798/(2.418+0.798),3)]

bar_width = 0.2 
index_br = np.arange(3) - bar_width
index_lu = np.arange(3)
index_di = np.arange(3) + bar_width
i=0
for a, b in zip(index_br, br):
    plt.text(a, b+2, str(b), ha='center', va='bottom')
    
for a, b in zip(index_lu, lu):
    plt.text(a, b+2, str(b), ha='center', va='bottom')
for a, b in zip(index_di, di):
    plt.text(a, b+2, str(b), ha='center', va='bottom')
for a, b in zip(index_br, add_lists(br, br1)):
    plt.text(a, b+3, str(b), ha='center', va='bottom')
for a, b in zip(index_lu, add_lists(lu, lu1)):
    plt.text(a, b+3, str(b), ha='center', va='bottom') 
for a, b in zip(index_di, add_lists(di, di1)):
    plt.text(a, b+3, str(b), ha='center', va='bottom') 

plt.bar(index_br , height = br , width = bar_width , edgecolor='black' , label='早餐男', hatch='/', color='white')
plt.bar(index_lu , height = lu , width = bar_width , edgecolor='black' , label='午餐男', color='white')
plt.bar(index_di , height = di , width = bar_width , edgecolor='black' , label='晚餐男', hatch='.', color='white')

plt.bar(index_br , height = br1 , bottom = br,width = bar_width , edgecolor='black' , label='早餐女', hatch='/', color='gray')
plt.bar(index_lu , height = lu1 , bottom = lu,width = bar_width , edgecolor='black' , label='午餐女',  color='gray')
plt.bar(index_di , height = di1 ,bottom = di, width = bar_width , edgecolor='black' , label='晚餐女', hatch='.', color='gray')

plt.xticks(index_lu,index)
plt.grid()
plt.legend()
plt.title('估算全体学生就餐类型')
plt.close()


import seaborn as sns
import matplotlib.patches as mpatches
import pandas as pd
unique_rows = pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月-2.csv")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(8,9))
plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
bi=[0,1,2,3,4,5,6,7,8,9,10]
ax=sns.histplot(data =unique_rows, x='DiliTimes',bins=bi,palette='gray',color='white',linewidth=2,stat="density",common_norm=False)
sns.kdeplot(data =unique_rows, x='DiliTimes',bw=3,color='black',linestyle='--')
hatches = ['/']
for i in range(len(ax.patches)):
    ax.patches[i].set_hatch(hatches[i // len(unique_rows['OutTimes'].unique())])
    ax.patches[i].set_linewidth(1)
handles = [mpatches.Patch(facecolor=['white','white'][i], edgecolor='black', hatch=['/', '|'][i]) for i in range(2)]
legend_labels = ["外出就餐次数统计",'核密度拟合']
ax.legend(handles, legend_labels, loc='upper center', bbox_to_anchor=(0.8, 1), ncol=1, frameon=False)
for bar in ax.patches:
    yval = bar.get_height()  # 获取柱子的高度
    ax.annotate(f'{yval:.3f}',  # 要标注的文本
    (bar.get_x() + bar.get_width() / 2-0.005, yval),  # 柱子的中心位置和高度
    ha='center', va='bottom',  # 水平和垂直对齐方式
    xytext=(0, 4),  # 文本偏移量
    textcoords='offset points',
    fontweight='bold'
    )  # 偏移单位
    plt.title('月度外卖就餐次数分布')
plt.grid()
ax.set_ylim(0,0.02)
ax.set_xlim(0,10)
plt.xlabel("Situation")
