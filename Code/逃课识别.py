# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 23:17:59 2025

@author: DELL
"""

import pandas as pd
import matplotlib.pyplot as plt

#读取数据
df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\新示例数据最新预处理.csv",header=0)
column = ['ID','Gender','Day','Week','Time','Lesson','Building','Classroom','Dor','What','TimeWhat']
taoke = pd.DataFrame()

#清洗与预处理
#只保留合法ID和时间列
# 按学生分组，提高效率
df['Taoke'] = 0
grouped = df.groupby(['ID','Day'])
for name, group in grouped:
    index = group[group['Type_l'] == '上课安排'].index
    if not len(index) == 0:
        for i in range(0,len(index) -1,2):
            if index[i+1] - index[i] != 1:
                df.loc[index[i],'Taoke'] = 1
                df.loc[index[i+1],'Taoke'] = 1
                
                ID = group.loc[index[i],'ID']
                gender = group.loc[index[i],'Gender']
                day = group.loc[index[i],'Day']
                week = group.loc[index[i],'Week']
                time = group.loc[index[i],'Second']
                lesson = group.loc[index[i],'Type_s'][:-2]
                building = group.loc[index[i],'Place']
                classroom =  group.loc[index[i],'Classroom']
                dor = group.loc[index[i],'Dor']
                what = group.loc[index[i] + 1,'Place']
                whattime = group.loc[index[i] + 1,'Second']
                
                taoke = pd.concat([taoke,pd.DataFrame([[ID,gender,day,week,time,lesson,building,
                                                        classroom,dor,what,whattime]],columns = column)])
                

taoke.to_csv(r"C:\Users\DELL\Desktop\新数据\T.csv")
df.to_csv(r"C:\Users\DELL\Desktop\新数据\S.csv")
                                                                 
