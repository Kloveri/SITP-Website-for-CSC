# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 00:08:37 2025

@author: DELL
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\新示例数据最新预处理.csv",header=0)
#df = df[(df['ID'] >= 1000) & (df['ID'] <= 1100)]
column = ['ID','Day','Performance']
wushui = pd.DataFrame()
wanshui = pd.DataFrame()

grouped = df.groupby(['ID','Day'])
for name, group in grouped:
    group_day = group[(group['Second'] >= 40500) & (group['Second'] <= 49200)]
    group_night = group[group['Second'] >= 64800]
    # print(name)
    if group_day['Type_s'].isin(['第四节课下课']).any() or group_day['Type_s'].isin(['第五节课上课']).any():
        group_day_dor = group_day[group_day['Type_l'] == '进出宿舍']
        if len(group_day_dor) == 0:
            if group_day['Type_s'].isin(['第五节课上课']).any():
                performance = -1
            else:
                performance = 0
        elif len(group_day_dor) == 1:
            index_dor = group_day_dor.index[0]
            if not index_dor == group_day.index[-1]:
                second_start = group_day.loc[index_dor , 'Second']
                second_end = group_day.loc[index_dor + 1, 'Second']
                second_rest = second_end - second_start
                performance = second_rest/(group_day.loc[group_day.index[-1],'Second'] -  \
                                           group_day.loc[group_day.index[0],'Second'])
            else: 
                performance = (group_day.loc[group_day.index[-1],'Second'] - group_day.loc[group_day.index[-2],'Second'])/\
                    (group_day.loc[group_day.index[-1],'Second'] - group_day.loc[group_day.index[0],'Second'])
        else:
            performance = (group_day_dor.loc[group_day_dor.index[-1],'Second'] - group_day_dor.loc[group_day_dor.index[0],'Second'])/\
                (group_day.loc[group_day.index[-1],'Second'] - group_day.loc[group_day.index[0],'Second'])
    else:
        if len(group_day) == 0:
            performance = 0
        elif len(group_day) == 1:
            performance == 0.1
        else:
            performance_p = (group_day.loc[group_day.index[-1],'Second'] - group_day.loc[group_day.index[0],'Second']) / 8700
            performance = performance_p if performance_p <= 1 else 1/performance_p
                
    wushui = pd.concat([wushui , pd.DataFrame([[group.loc[group.index[0],'ID'], \
                                               group.loc[group.index[0],'Day'],performance]],columns=column)])
        
    if len(group_night)==0 :
        bugui = -1
    else:
        group_night_dor = group_night[group_night['Type_l'] == '进出宿舍']
        if len(group_night) == 0:
            bugui = 0
        else:
            bugui = 1
    wanshui = pd.concat([wushui , pd.DataFrame([[group.loc[group.index[0],'ID'], \
                                               group.loc[group.index[0],'Day'],bugui]],columns=column)])
    
    
print(wushui)
wushui.to_csv(r"C:\Users\DELL\Desktop\新数据\Wushui.csv")
wanshui.to_csv(r"C:\Users\DELL\Desktop\新数据\Bugui.csv")
