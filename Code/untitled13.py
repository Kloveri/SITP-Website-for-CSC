# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 10:14:50 2026

@author: DELL
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\新示例数据最新预处理.csv",header=0)
tsg = pd.DataFrame()
column = ['ID','Day','Age','Gender','Identity','Week','Dor','Is','During','First','Last']

grouped = df.groupby(['ID','Day'])
for name, group in grouped:
    group_library = group[group['Type_l'] == '进出图书馆']
    if len(group_library) == 0:
        is_l = 0
        time_l = 0
        first_l = np.nan
        last_l = np.nan
    else:
        group_library_in = group_library[group_library['Type_s'] == '进图书馆']
        group_library_out = group_library[group_library['Type_s'] == '出图书馆']
        is_l = 1
        for j in reversed(group_library.index):
            group_library_now = group_library.loc[group_library.index[0:j]]
            g_l_n_i = group_library_now[group_library_now['Type_s'] == '进图书馆']
            g_l_n_o = group_library_now[group_library_now['Type_s'] == '出图书馆']
            if len(g_l_n_i) == len(g_l_n_o):
                time_l = g_l_n_o['Second'].sum() - g_l_n_i['Second'].sum()
                time_l = abs(time_l)
                break
            else:
                pass
        first_l = group_library_in.loc[group_library_in.index[0],'Second'] if len(group_library_in) !=0 else np.nan
        last_l = group_library_out.loc[group_library_out.index[-1],'Second'] if len(group_library_out) !=0 else np.nan
    _id = list(group.loc[group.index[0] , ['ID','Day','Age','Gender','Identity','Week','Dor']])
    _id.extend([is_l,time_l,first_l,last_l])
    tsg = pd.concat([tsg , pd.DataFrame([_id] , columns = column)])

date_all = tsg['Day'].unique()
for i in tsg['ID'].unique():
    tsg_i= df[df['ID'] == i ]
    if not len(tsg_i) == 31:
        for j in date_all:
            if not j in tsg_i['Day'].unique():
                _id = list(tsg_i.loc[tsg_i.index[0],['ID','Day','Age','Gender','Identity','Week','Dor']])
                _id[1] = j
                _id.extend([0,0,np.nan,np.nan])
                tsg = pd.concat([tsg , pd.DataFrame([_id] , columns = column)])
tsg.to_csv(r"C:\Users\DELL\Desktop\新数据\TSG.csv")
