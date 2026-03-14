# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:34:07 2025

@author: DELL
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import scipy.stats as st

plt.rcParams['font.sans-serif']=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False 

data=pd.read_csv(r'C:\Users\DELL\Desktop\私铁营业里程与旅客数量.csv')
df=pd.DataFrame(data)
x1=df['会社営業キロ']
x=sm.add_constant(x1)
y=df['旅客数量']
a=np.linalg.inv(x.T@x)@x.T@y
print(a)

plt.scatter(x1,y)
plt.plot((0,500),(a[0]+a[1]*0,a[0]+a[1]*500),color='r')
plt.ylabel('旅客数量')
plt.xlabel('会社営業キロ')
plt.title('私铁营业里程与旅客数量关系回归分析图')
plt.show()

cancha=[y[i]-(a[0]+a[1]*x1[i]) for i in range(len(y))]
print(st.shapiro(cancha))
print(st.spearmanr(df['旅客数量'], cancha))
print(pd.DataFrame(cancha))
# 绘制Q-Q图
sm.qqplot(pd.Series(cancha),loc=np.mean(cancha), scale=np.std(cancha),line="45")
plt.title('残差Q-Q图')
plt.show()

# 绘制残差与因变量的散点图
fig=plt.figure()
plt.scatter(y, cancha)
plt.xlabel('因变量')
plt.ylabel('残差')
plt.title('残差与因变量散点图')
plt.axhline(y=0, color='r', linestyle='--')  # 添加y=0的参考线
plt.show()
