# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 17:36:19 2025

@author: DELL
"""

import pandas as pd
import numpy as np
original_file = pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月.csv",header=0)
new_schedule = pd.read_csv(r"C:\Users\DELL\Desktop\新上课数据5月_250416.csv",header=0)

print(new_schedule.head())
original_file['Classroom'] = np.nan
original_file['Type_l'].replace({'上课安排' : np.nan} , inplace = True)
original_file.dropna(subset = ['Type_l'] , inplace = True)

print(original_file.head())
print(original_file['Type_l'].unique())

id_num = original_file['ID'].max()
id_num_new = new_schedule['ID'].max()
if id_num_new > id_num:
    new_schedule = new_schedule[new_schedule['ID'] <= id_num_new]

original_file_main = original_file[['ID','Age','Gender','Identity','Type_l','Type_s','Time','Campus','Place','Classroom']]
new_schedule_main = new_schedule[['ID','Age','Gender','Identity','Type_l','Type_s','Time','Campus','Place','Classroom']]
new_data = pd.concat([original_file_main , new_schedule_main])
new_data.sort_values(by = ['ID' , 'Time'] , inplace = True)
new_data = new_data.reset_index(drop = True)

while new_data['Age'].isnull().any():
    new_data['Age'].fillna(method = 'ffill' , inplace = True)
    new_data['Gender'].fillna(method = 'ffill' , inplace = True)
    new_data['Identity'].fillna(method = 'ffill' , inplace = True)
    
'''
ori_num = 1
id_ori = 1
for i in range(len(new_data) - 1):
    if i == 0:
        new_data.loc[i , 'Act_ID'] = 1
    else:
        if new_data.iloc[i+1]['ID'] == new_data.iloc[i]['ID']:
            ori_num += 1
            new_data.loc[i , 'Act_ID'] = ori_num           
        else:
            ori_num += 1
            new_data.loc[i , 'Act_ID'] = ori_num 
            ori_num = 0
            
Complexity of this code turns to be too high, unsupported to run
'''

new_data['Index'] = new_data.index
new_data['Act_ID'] = np.nan
ori_data = new_data.copy()
num = len(new_data[new_data['ID'] <= 2100])
new_data = new_data[(new_data['ID'] > 2100) & (new_data['ID'] <= 2200)]

for i in range(len(new_data)):
    new_data.loc[i + num,'Act_ID'] = new_data.loc[i + num,'Index'] - len(ori_data[ori_data['ID'] < ori_data.loc[i + num,'ID']]) + 1
print(new_data.head())

new_data_new = new_data[['Index','ID','Act_ID','Age','Gender','Identity','Type_l','Type_s','Time','Campus','Place','Classroom']]
new_data_new.to_csv(r"C:\Users\DELL\Desktop\新示例数据2100-2200.csv",header=True,index=False)