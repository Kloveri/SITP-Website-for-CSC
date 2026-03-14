# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 17:08:10 2025

@author: DELL
"""

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
import math
fig=plt.figure(figsize=(12,9))
plt.grid()
ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
from scipy.stats import norm
k=5
data_qu_21 = data_qu[(data_qu['Place'] == '赤峰路50号门')|(data_qu['Place'] == '赤峰路67号门')]
data_hui_21 = data_hui[(data_hui['Place'] == '赤峰路50号门')|(data_hui['Place'] == '赤峰路67号门')]
data_21 = []
for i in name:
    real = len(data_qu_21[data_qu_21['Qu'] == i]) - len(data_hui_21[data_hui_21['Hui'] == i])
    real = abs(real) if i < "12:15" else -abs(real)
    real = real*1.3 if i < "12:15" else real*2
    data_21.append(real)
    data_21_ = [sum(data_21[:i]) for i in range(len(data_21))]
    data_21_1 = [data_21_[i] -  96/(15*np.exp(1/np.sqrt(i)) - 30*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_2 = [data_21_[i] -  96/(20*np.exp(1/np.sqrt(i)) - 40*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_3 = [data_21_[i] -  96/(25*np.exp(1/np.sqrt(i)) - 50*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_4 = [data_21_[i] -  96/(30*np.exp(1/np.sqrt(i)) - 60*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_5 = [data_21_[i] -  96/(35*np.exp(1/np.sqrt(i)) - 70*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_6 = [data_21_[i] -  96/(40*np.exp(1/np.sqrt(i)) - 80*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_7 = [data_21_[i] -  96/(45*np.exp(1/np.sqrt(i)) - 90*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_8 = [data_21_[i] -  96/(60*np.exp(1/np.sqrt(i)) - 100*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_9 = [data_21_[i] -  96/(70*np.exp(1/np.sqrt(i)) - 110*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_10 = [data_21_[i] -  96/(60*np.exp(1/np.sqrt(i)) - 120*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_11 = [data_21_[i] -  96/(65*np.exp(1/np.sqrt(i)) - 130*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
    data_21_12 = [data_21_[i] -  96/(200*np.exp(1/np.sqrt(i)) - 200*np.exp(-abs(i-12)/10)) for i in range(len(data_21_))]
ax=plt.plot(np.arange(len(data_21_1)),data_21_1,color='maroon',label = 'a=30',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_2,color='brown',label = 'a=40',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_3,color='indianred',label = 'a=50',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_4,color='lightcoral',label = 'a=60',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_5,color='cornsilk',label = 'a=70',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_6,color='gold',label = 'a=80',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_7,color='goldenrod',label = 'a=90',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_8,color='darkgoldenrod',label = 'a=100',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_9,color='darkslategray',label = 'a=110',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_10,color='navy',label = 'a=120',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_11,color='mediumblue',label = 'a=130',linewidth=3)
plt.plot(np.arange(len(data_21_1)),data_21_12,color='blue',label = 'a=+oo',linewidth=3)

'''
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
'''
plt.title('理想分布下所需外卖柜数——南门外卖柜')
#plt.plot([0,36],[0,0],color='black',linewidth = 4)
plt.xlim(0,36)
plt.ylim(-100,100)
plt.xticks(np.arange(len(data_21)),name,rotation=45)
plt.legend(loc = 'upper right')

