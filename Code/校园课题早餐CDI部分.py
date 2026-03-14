# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 18:41:13 2025

@author: DELL
"""

import pandas as pd
import numpy as np
from time import gmtime
from time import strftime
import datetime
from datetime import timedelta

r'''
df=pd.read_csv(r"C:\Users\DELL\Desktop\新数据\新示例数据最新预处理.csv",header=0,encoding='utf-8')
dili=pd.read_excel(r"C:\Users\DELL\Desktop\外卖领取点信息.xlsx",header=0)
action=pd.read_excel(r"C:\Users\DELL\Desktop\行为性质.xlsx",header=0)
diliplace=dili[["Place","DeliveryPlace"]]

r"""
df['First8'] = 0
grouped1 = df.groupby(['Day', 'ID'])
for name,group in grouped1:
    index = group.index
    group_8 = group[group['Second'] == 28800]
    group_8 = group_8[group_8['Type_s'] == '第一节课上课']
    if not len(group_8)==0 :
        df.loc[index , 'First8'] = 1
df.to_csv(r"C:\Users\DELL\Desktop\新数据\新示例数据最新预处理加早八.csv")
数据预处理时使用的临时语句
"""

def mealisnot(x, y):
    try:
        if y == "早餐" or y == "午餐" or y == "晚餐":
            x = x.reset_index(drop=True)
            number = x.shape[0] 
            for i in range(number):
                if x.loc[i, "Type_s"] == y or x.loc[i, "Type_s"] == "其他":
                    return True 
                    break 
                else:
                    pass 
            return False 
    except:
        return "Error! Choose the right type of meal!"

df_breakfast = df[df["Breakfast"] == 1]
column = ['Index','ID','Day','Age','X','Y','Time','TimeOD','First8','Which']
breakfast_rail_df = pd.DataFrame(columns = column)
grouped = df_breakfast.groupby(['Day', 'ID'])
for name, group in grouped:
    breakfast_sum = group['Breakfast'].sum()
    if breakfast_sum == 0:
        df.loc[group.index, 'Breakfasttype'] = 0#无法识别
    elif mealisnot(group, "早餐"):
        df.loc[group.index, 'Breakfasttype'] = 2#在校就餐
    else:
        df.loc[group.index, 'Breakfasttype'] = 1#还未识别的
    
    for index in group.index[:-1]:
        if group.loc[index , 'Type_s'] == '早餐' or group.loc[index + 1 , 'Type_s'] == '早餐':
            ID = group.loc[index , 'ID']
            age = group.loc[index, 'Age']
            day = group.loc[index, 'Day']
            time = (group.loc[index, 'Second'] + group.loc[index+1, 'Second'])/2
            timeod = group.loc[index+1, 'Second'] - group.loc[index, 'Second']
            first888 = group.loc[index, 'First8']
            which = 'Back' if  group.loc[index , 'Type_s'] == '早餐' else 'Go'
            breakfast_rail_df = pd.concat([breakfast_rail_df , pd.DataFrame([[index,ID,day,age,group.loc[index,'Place'],group.loc[index+1,'Place'],time,timeod,first888,which]],columns = column)])
                                                                    
breakfast_rail_df = breakfast_rail_df.sort_values(by=['ID' , 'Day'])                      
breakfast_rail_df.to_csv(r"C:\Users\DELL\Desktop\新数据\B.csv")

'''
breakfast_rail_df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\B.csv",header=0,encoding='utf-8')
POI = pd.read_csv(r"C:\Users\DELL\Desktop\校园POI信息.csv",header=0,encoding='ansi')
breakfast_rail_df = pd.merge(left = breakfast_rail_df , right = POI , left_on = 'X', right_on = 'Place')
breakfast_rail_df = breakfast_rail_df.rename(columns={'Lng':'X_Lng','Lat':'X_Lat'})
breakfast_rail_df = pd.merge(left = breakfast_rail_df , right = POI , left_on = 'Y', right_on = 'Place')
breakfast_rail_df = breakfast_rail_df.rename(columns={'Lng':'Y_Lng','Lat':'Y_Lat'})
breakfast_rail_df['Distance'] = 100000*abs(breakfast_rail_df['X_Lat'] - breakfast_rail_df['Y_Lat']) + 111320*abs(breakfast_rail_df['X_Lng'] - breakfast_rail_df['Y_Lng'])
breakfast_rail_df['Speed'] = (breakfast_rail_df['Distance']/1000)/(breakfast_rail_df['TimeOD']/3600)
breakfast_rail_df.to_csv(r"C:\Users\DELL\Desktop\新数据\B.csv")
