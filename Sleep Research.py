# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:04:01 2026

@author: DELL
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df_wushui = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\Wushui1.csv",header=0)
df_wushui = df_wushui[df_wushui['ID'] <= 2000]
df_wushui = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\Bugui.csv",header=0)
df_wushui = df_wushui[df_wushui['ID'] <= 2000]
df_TSG = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\TSG.csv",header=0)

r'''
date_all = df_wushui['Day'].unique()
print(date_all)
for i in df_wushui['ID'].unique():
    tsg_i= df_wushui[df_wushui['ID'] == i ]
    if not len(tsg_i) == 31:
        for j in date_all:
            if not j in tsg_i['Day'].unique():
                ID = tsg_i.loc[tsg_i.index[0] , 'ID']
                day = j
                performance = 0
                df_wushui = pd.concat([df_wushui, pd.DataFrame([[ID,day,performance]],columns = ['ID','Day','Performance'])])
                print(i,day)
df_wushui.to_csv(r"C:\Users\DELL\Desktop\新数据\Bugui.csv")

#上述代码为基础数据处理代码，仅会运行一次，这里我们注释掉
'''

df_w_f = df_wushui
df_w_f['Dayday'] = df_w_f['Day'].apply(lambda x: int(x[7:]))
df_w_f.sort_values(by=['ID','Dayday'],inplace=True)
print(df_w_f.head())
plt.rcParams['font.sans-serif']=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False 
fig = plt.figure(figsize=(24,9))
sns.set_theme(style='darkgrid')  

plt.title('Nap Goodness of 2000 Students',fontsize=20)
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)

data_numpy = []
label = []
for i in df_w_f['ID'].unique():
    da = list(df_w_f[df_w_f['ID'] == i]['Performance'])
    label.append(i)
    data_numpy.append(da)

print(len(data_numpy[0]))

sns.heatmap(np.array(data_numpy).transpose() , yticklabels=list(df_w_f['Day'].unique()))
plt.xticks(rotation = 45)

plt.ylabel('Date')
plt.xlabel('ID_Number')

plt.close()

fig = plt.figure(figsize=(30,9))
plt.title('Total Usage Time of Library',fontsize=20)
sns.set_theme(style='darkgrid')  
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)

df_TSG['Gender'] = df_TSG['Gender'].replace({'男':'Male','女':'Female'})
df_TSG['Dayday'] = df_TSG['Day'].apply(lambda x: int(x[8:]))
df_TSG.sort_values(by=['ID','Dayday'],inplace=True)
'''sns.lineplot(x='Day',y='Is',hue = 'Gender',data=df_TSG,style="Gender",markers=['x','x'],color=['orange','blue'])
sns.lineplot(x='Day',y='Is',data=df_TSG, markers="o",label='All')
#sns.boxplot(x='Day',y='First' , data=df_TSG)
#sns.boxplot(x='Day',y='Last' , data=df_TSG)
#sns.lineplot(x='Day',y='First' , data=df_TSG,linewidth = 2 ,color='white')
#sns.lineplot(x='Day',y='Last' , data=df_TSG,linewidth = 2 ,color='white')

grouped = df_TSG.groupby('Day')
plt.yticks([28800,31800,36000,39000,49800,51800,55800,58800,68400,71400,74700],['8:00','8:50','10:00','10:50','13:30','14:20','15:30','16:20','19:00','19:50','20:40'])
plt.xticks(rotation = 45)
plt.xlabel('Day')
plt.ylabel('Rate')'''
plt.close()

df_t_f = df_TSG[(df_TSG['During'] != 0)&(df_TSG['During'] < 12*3600)]
fig = plt.figure(figsize=(15,9))
plt.title('Total Usageof Library',fontsize=20)
sns.histplot(df_t_f, x='During', hue='Gender' , kde=True)
plt.xticks([3600,7200,10800,3600*4,3600*5,3600*6,3600*7,3600*8,3600*9,3600*10,3600*11,3600*12],[1,2,3,4,5,6,7,8,9,10,11,12])
plt.xlabel('Hour')