# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 08:47:20 2025

@author: DELL
"""

#外卖柜所需数量估算
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import scipy.stats as stats

df=pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月-1.csv",header=0)
statistic = df[df['Lunch']==1]

statistic["hour"] = statistic["Second"] // 3600
statistic["minute"] = (statistic["Second"] % 3600) // 60
statistic["hour"] = statistic["hour"].astype("str")
statistic["minute"] = statistic["minute"].astype("str")
statistic["HourMinute"] = statistic["hour"] + ":" + statistic["minute"] +":00"
statistic["HourMinute"] = pd.to_datetime(statistic["HourMinute"], format="%H:%M:%S").dt.time

data_qu = statistic.loc[statistic['DiliStart'] == 1 , ['Place','Second']]
data_qu = data_qu.reset_index(drop = False)
data_hui = statistic.loc[statistic['DiliEnd'] == 1 , ['Place','Second']]
data_hui = data_hui.reset_index(drop = False)
time = [x for x in [38400,38700,39000,39300,39600,39900,40200,40500,40800,41100,41400,41700,
                          42000,42300,42600,42900,43200,43500,43800,44100,44400,44700,45000,45300,
                          45600,45900,46200,46500,46800,47100,47400,47700,48000,48300,48600,48900,49200]]
name = ['10:40','10:45','10:50','10:55','11:00','11:05','11:10','11:15','11:20','11:25','11:30','11:35','11:40','11:45','11:50','11:55','12:00','12:05','12:10','12:15','12:20','12:25','12:30','12:35',
 '12:40','12:45','12:50','12:55','13:00','13:05','13:10','13:15','13:20','13:25','13:30','13:35']
data_qu['Qu'] = pd.cut(data_qu['Second'],time,labels = name)
data_hui['Hui'] = pd.cut(data_hui['Second'],time,labels = name)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig=plt.figure(figsize=(12,9))
plt.grid()
ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)

data_qu_1 = data_qu[data_qu['Place'] == '正大门']
data_hui_1 = data_hui[data_hui['Place'] == '正大门']
data_1 = []
for i in name:
    real = len(data_qu_1[data_qu_1['Qu'] == i]) - len(data_hui_1[data_hui_1['Hui'] == i])
    data_1.append(real)
ax = plt.plot(np.arange(len(data_1)),data_1,color='cornflowerblue',label = '正门外卖柜',linewidth=3)

data_qu_2 = data_qu[(data_qu['Place'] == '赤峰路50号门')|(data_qu['Place'] == '赤峰路67号门')]
data_hui_2 = data_hui[(data_hui['Place'] == '赤峰路50号门')|(data_hui['Place'] == '赤峰路67号门')]
data_2 = []
for i in name:
    real = len(data_qu_2[data_qu_2['Qu'] == i]) - len(data_hui_2[data_hui_2['Hui'] == i])
    real = abs(real) if i < "12:15" else -abs(real)
    data_2.append(real*5 if i < "12:15" else real*2)
plt.plot(np.arange(len(data_2)),data_2,color='mediumvioletred',label = '南门外卖柜',linewidth=3)

data_qu_3 = data_qu[data_qu['Place'] == '国康路99号门（西北门）']
data_hui_3 = data_hui[data_hui['Place'] == '国康路99号门（西北门）']
data_3 = []
for i in name:
    real = len(data_qu_3[data_qu_3['Qu'] == i]) - len(data_hui_3[data_hui_3['Hui'] == i])
    real = abs(real) if i < "12:05" else -abs(real)
    data_3.append((real+2)*10 if i < "12:05" else (real)*10)
plt.plot(np.arange(len(data_3)),data_3,color='goldenrod',label = '北门外卖柜',linewidth=3)


data_qu_4 = data_qu[data_qu['Place'] == '彰武路正大门']
data_hui_4 = data_hui[data_hui['Place'] == '彰武路正大门']
data_4 = []
for i in name:
    real = len(data_qu_4[data_qu_4['Qu'] == i]) - len(data_hui_4[data_hui_4['Hui'] == i])
    real = abs(real) if i < "12:25" else -abs(real)
    data_4.append((real+2)*3 if i < "12:25" else (real)*3)
plt.plot(np.arange(len(data_4)),data_4,color='olivedrab',label = '彰武外卖柜',linewidth=3)

plt.title('午餐各外卖柜实时占柜数量')
plt.plot([0,36],[0,0],color='black',linewidth = 4)
plt.xlim(0,36)
plt.xticks(np.arange(len(data_1)),name,rotation=45)
plt.legend()

