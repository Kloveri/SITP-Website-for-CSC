# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 23:27:55 2025

@author: DELL
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

result = pd.DataFrame()
df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\Z.csv",header=0,encoding='utf-8')
grouped = df.groupby("Place")
for name, group in grouped:
    al = group['Dor'].value_counts()
    al = al.rename(name)
    result = pd.concat([result,al],axis=1)

indexlist=['西北一楼','西北二楼','西北三楼','西北四楼','西北五楼','学四楼','学五楼',
           '留学生1号楼','留学生2号楼','西南二楼 ','西南三楼','西南七楼','西南八楼',
           '西南九楼','西南十楼','西南十一楼','西南十二楼','彰武闸机','彰武1号楼','彰武2号楼',
           '彰武3号楼','彰武4号楼','彰武5号楼','彰武6号楼','彰武7号楼','彰武8号楼','彰武9号楼','彰武10号楼']
result = result.reindex(indexlist)    
result = result.replace({np.nan:0})
for i in range(result.shape[0]):
    a = 0
    for j in range(result.shape[1]):
        a += result.iloc[i,j]
        
    for j in range(result.shape[1]):
        result.iloc[i,j] = round(result.iloc[i,j]/a,3)
print(result)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(14,9))
plt.grid()
ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
ax1=ax
ax=plt.bar(np.arange(len(result)),result['学苑食堂'],edgecolor='black',linewidth=2,color='white')
for i in range(5):
    ax.patches[i].set_hatch('/')
    ax.patches[i].set_linewidth(1)
for i in range(5,9):
    ax.patches[i].set_hatch('.')
    ax.patches[i].set_linewidth(1)
for i in range(9,15):
    ax.patches[i].set_hatch('-')
    ax.patches[i].set_linewidth(1)
for i in range(15,18):
    ax.patches[i].set_hatch('\\')
    ax.patches[i].set_linewidth(1)
for i in range(18,len(result)):
    ax.patches[i].set_hatch('|-')
    ax.patches[i].set_linewidth(1)
handles = [mpatches.Patch(facecolor=['white','white','white','white','white'][i], edgecolor='black', hatch=['/', '.','-','\\','|-'][i]) for i in range(5)]
ax1.legend(handles, ['西北片区','北部片区）','西南片区','南校区','彰武校区'], loc='upper center', bbox_to_anchor=(0.8, 1), ncol=2, frameon=False)
plt.text()
plt.xticks(np.arange(len(result)),result.index,rotation=45)
plt.xlabel('宿舍及宿舍片区')
plt.ylabel('数量统计')
plt.title('学苑食堂早餐就餐来源分布')

