# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 00:05:04 2025

@author: DELL
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\T.csv")
df['weight'] = df['Gender'].replace({'男':1,'女':2.5})
df_p = df.groupby('ID').agg({'ID':'first','What':'count','Gender':'first','weight':'first'})
dor = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\Z.csv")
dormitory = dor.groupby('ID').agg({'Dor':'first'})['Dor'].value_counts()
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
sns.kdeplot(data = df_p , x='What' , hue ='Gender',weights = df_p['weight'],palette = ['black','black'])
ax= sns.histplot(data = df_p , x='What' , hue ='Gender',weights = df_p['weight'],bins =25 ,palette=['white','gray'],linewidth=2,stat = 'density')
for bar in ax.patches:
    yval = bar.get_height()  # 获取柱子的高度
    ax.annotate(f'{yval:.2f}',  # 要标注的文本
    (bar.get_x() + bar.get_width() / 2-0.005, yval),  # 柱子的中心位置和高度
    ha='center', va='bottom',  # 水平和垂直对齐方式
    xytext=(0, 4),  # 文本偏移量
    textcoords='offset points',
    fontweight='bold',fontsize=12
    )  # 偏移单位

plt.xlim(0,30)
plt.title('学生月度逃课次数分布图')
"""
plt.close()

df_d = df.groupby('Dor').agg({'Dor':'first','What':'count','Gender':'first'})
df_d = pd.concat([df_d,dormitory] , axis =1)
df_d['Rate'] = df_d['What']/df_d['count']
indexlist=['西北一楼','西北二楼','西北三楼','西北四楼','西北五楼','学四楼','学五楼',
           '留学生1号楼','留学生2号楼','西南二楼 ','西南三楼','西南七楼','西南八楼',
           '西南九楼','西南十楼','西南十一楼','西南十二楼','彰武闸机','彰武1号楼','彰武2号楼',
           '彰武3号楼','彰武4号楼','彰武5号楼','彰武6号楼','彰武7号楼','彰武8号楼','彰武9号楼','彰武10号楼']
df_d = df_d.reindex(indexlist)    
df_d = df_d.replace({np.nan:0})

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(16,9))
plt.grid()
ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
ax1 = ax
ax = plt.bar(np.arange(len(df_d)) , df_d['Rate'],edgecolor='black',linewidth=2,color='white')
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
for i in range(18,len(df_d)):
    ax.patches[i].set_hatch('|-')
    ax.patches[i].set_linewidth(1)
handles = [mpatches.Patch(facecolor=['white','white','white','white','white'][i], edgecolor='black', hatch=['/', '.','-','\\','|-'][i]) for i in range(5)]
ax1.legend(handles, ['西北片区','北部片区','西南片区','南校区','彰武校区'], loc='upper center', bbox_to_anchor=(0.8, 1), ncol=2, frameon=False)
for i in range(len(df_d)):
    plt.text(i-0.5,df_d.iloc[i]['Rate']+0.25,str(round(df_d.iloc[i]['Rate'],1)))
plt.xticks(np.arange(len(df_d)),df_d.index,rotation = 45)
plt.title('宿舍月度平均逃课次数')
plt.close()

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(30,9))

ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
ax1 = ax

ax= sns.histplot(data = df , x='TimeWhat' , hue ='Week',linewidth=2,stat = 'density',bins=200,kde=True)
plt.xticks([28800,31800,36000,39000,49800,51800,55800,58800,68400,71400,74700],['第一节课','第二节课','第三节课','第四节课','第五节课','第六节课','第七节课','第八节课','第九节课','第十节课','第十一节课'])
plt.grid()
plt.xlabel('时间')
plt.ylabel('密度')
plt.title('学生逃课的时间分布')
plt.close()

def a(x):
    if x[-1]=='楼':
        return '宿舍'
    elif x[-2:]=='食堂':
        return '食堂'
    elif x[-1]=='门':
        return '出校'
    elif x[-1]==[')']:
        return '出校'
    elif x[-2:] == '闸机':
        return '出校'
    else:
        return '其余活动'
df_w = df['What'].value_counts()

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(20,9))

ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
ax1 = ax
df_w = df_w.reset_index(drop = False)
df_w['Type'] = df_w['What'].apply(a)
df_w = df_w.sort_values(by = 'Type')

ax=sns.barplot(data = df_w , x= 'What' , y='count',hue='Type',palette='dark:white',edgecolor='black')
plt.xticks(rotation = 45)
plt.grid()
plt.xlabel('逃课目的地去向')
plt.ylabel('数量')
plt.title('逃课目的地统计')
plt.close()

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(20,9))
ax=plt.rcParams.update({'font.size': 16})
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
ax1 = ax
df_nan = df[df['Building'] == '南楼']
df_nan_1 = df_nan.groupby('Day').agg({'Day':'first','Lesson':'count','Week':'first'})
df_nan_1['Mask'] = df_nan_1['Week'].replace({'Monday':1,'Tuesday':11/4,'Wednesday':1,'Thursday':1,'Friday':11/6,'Saturday':1})
df_nan_1['Count'] = df_nan_1['Mask']*df_nan_1['Lesson']
ax = plt.plot(np.arange(len(df_nan_1)),df_nan_1['Count'],label = '南楼',color = 'darkcyan',linewidth = 3)
df_nan_1 = df_nan_1.reset_index(drop = True)
index1 = df_nan_1[df_nan_1['Week'] == 'Tuesday'].index
plt.scatter(index1 , df_nan_1.loc[index1 , 'Count'],s=100,c="black",label="Tuesday",marker = 's')
index2 = df_nan_1[df_nan_1['Week'] == 'Friday'].index
plt.scatter(index2 , df_nan_1.loc[index2 , 'Count'],s=100,c="black",label="Friday",marker = '^')

df_nan = df[df['Building'] == '北楼']
df_nan_1 = df_nan.groupby('Day').agg({'Day':'first','Lesson':'count','Week':'first'})
df_nan_1['Mask'] = df_nan_1['Week'].replace({'Monday':1,'Tuesday':11/4,'Wednesday':1,'Thursday':1,'Friday':11/6,'Saturday':1})
df_nan_1['Count'] = df_nan_1['Mask']*df_nan_1['Lesson']
ax = plt.plot(np.arange(len(df_nan_1)),df_nan_1['Count'],label = '北楼',color = 'goldenrod',linewidth = 3)
df_nan_1 = df_nan_1.reset_index(drop = True)
index1 = df_nan_1[df_nan_1['Week'] == 'Tuesday'].index
plt.scatter(index1 , df_nan_1.loc[index1 , 'Count'],s=100,c="black",marker = 's')
index2 = df_nan_1[df_nan_1['Week'] == 'Friday'].index
plt.scatter(index2 , df_nan_1.loc[index2 , 'Count'],s=100,c="black",marker = '^')

df_nan = df[df['Building'] == '城规B楼']
df_nan_1 = df_nan.groupby('Day').agg({'Day':'first','Lesson':'count','Week':'first'})
df_nan_1['Mask'] = df_nan_1['Week'].replace({'Monday':1,'Tuesday':11/4,'Wednesday':1,'Thursday':1,'Friday':11/6,'Saturday':1})
df_nan_1['Count'] = df_nan_1['Mask']*df_nan_1['Lesson']
ax = plt.plot(np.arange(len(df_nan_1)),df_nan_1['Count'],label = '城规B楼',color = 'brown',linewidth = 3)
df_nan_1 = df_nan_1.reset_index(drop = True)
index1 = df_nan_1[df_nan_1['Week'] == 'Tuesday'].index
plt.scatter(index1 , df_nan_1.loc[index1 , 'Count'],s=100,c="black",marker = 's')
index2 = df_nan_1[df_nan_1['Week'] == 'Friday'].index
plt.scatter(index2 , df_nan_1.loc[index2 , 'Count'],s=100,c="black",marker = '^')

df_nan = df[df['Building'] == '瑞安楼']
df_nan_1 = df_nan.groupby('Day').agg({'Day':'first','Lesson':'count','Week':'first'})
df_nan_1['Mask'] = df_nan_1['Week'].replace({'Monday':1,'Tuesday':11/4,'Wednesday':1,'Thursday':1,'Friday':11/6,'Saturday':1})
df_nan_1['Count'] = df_nan_1['Mask']*df_nan_1['Lesson']
ax = plt.plot(np.arange(len(df_nan_1)),df_nan_1['Count'],label = '瑞安楼',color = 'slateblue',linewidth = 3)
df_nan_1 = df_nan_1.reset_index(drop = True)
index1 = df_nan_1[df_nan_1['Week'] == 'Tuesday'].index
plt.scatter(index1 , df_nan_1.loc[index1 , 'Count'],s=100,c="black",marker = 's')
index2 = df_nan_1[df_nan_1['Week'] == 'Friday'].index
plt.scatter(index2 , df_nan_1.loc[index2 , 'Count'],s=100,c="black",marker = '^')

df_nan = df[df['Building'] == '体育馆']
df_nan_1 = df_nan.groupby('Day').agg({'Day':'first','Lesson':'count','Week':'first'})
df_nan_1['Mask'] = df_nan_1['Week'].replace({'Monday':1,'Tuesday':11/4,'Wednesday':1,'Thursday':1,'Friday':11/6,'Saturday':1})
df_nan_1['Count'] = df_nan_1['Mask']*df_nan_1['Lesson']
ax = plt.plot(np.arange(len(df_nan_1)),df_nan_1['Count'],label = '体育馆',color = 'deeppink',linewidth = 3)
df_nan_1 = df_nan_1.reset_index(drop = True)
index1 = df_nan_1[df_nan_1['Week'] == 'Tuesday'].index
plt.scatter(index1 , df_nan_1.loc[index1 , 'Count'],s=100,c="black",marker = 's')
index2 = df_nan_1[df_nan_1['Week'] == 'Friday'].index
plt.scatter(index2 , df_nan_1.loc[index2 , 'Count'],s=100,c="black",marker = '^')

df_nan_1 = df.groupby('Day').agg({'Day':'first','Lesson':'count','Week':'first'})
df_nan_1['Mask'] = df_nan_1['Week'].replace({'Monday':1,'Tuesday':11/4,'Wednesday':1,'Thursday':1,'Friday':11/6,'Saturday':1})
df_nan_1['Count'] = df_nan_1['Mask']*df_nan_1['Lesson']

plt.bar(np.arange(len(df_nan_1)),df_nan_1['Count']/2,color = 'gray',alpha = 0.5)
print(df_nan_1)

plt.xticks(np.arange(len(df_nan_1)),df_nan_1.index,rotation = 45)
plt.grid()
plt.legend()
plt.title('各教学楼月度逃课标准化数量')

"""