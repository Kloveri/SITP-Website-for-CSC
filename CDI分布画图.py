# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 15:50:47 2025

@author: DELL
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

column = ['TimeOD','OD','CDIave']
CDIdata = pd.DataFrame(columns = column)
breakfast_rail_df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\B.csv",header=0,encoding='utf-8')

bins=[27000,27300,27600,27900,28200,28500,28800,29100,29400,29700,30000]
names=['7:30-7:35','7:35-7:40','7:40-7:45','7:45-7:50','7:50-7:55','7:55-8:00','8:00-8:05','8:05-8:10','8:10-8:15','8:15-8:20']
breakfast_rail_df['When'] = pd.cut(breakfast_rail_df['Time'],bins,labels=names)
print(breakfast_rail_df.head())
timegrouped = breakfast_rail_df.groupby('When')
for time, group in timegrouped:
    timeODgrouped = group.groupby(['X','Y'])
    for name,OD in timeODgrouped:
        index = OD.index
        OD_new = OD[OD['CDI']!=1]
        ave_CDI = OD_new['CDI'].mean()
        CDIdata = pd.concat([CDIdata , pd.DataFrame([[time , name , ave_CDI]],columns = column)])
        

CDIdata = CDIdata.reset_index()
grouped = CDIdata.groupby('OD')
for name, group in grouped:
    index = group.index
    print(index)
    print(name,group[['TimeOD','CDIave']])

CDIdata = CDIdata.sort_values(by='OD')
CDIdata.to_csv(r"C:\Users\DELL\Desktop\新数据\C.csv")