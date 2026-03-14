# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 14:54:29 2025

@author: DELL
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

breakfast_rail_df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\B.csv",header=0,encoding='ansi')
breakfast_rail_df['FreeSpeed'] = 0

b_walk=breakfast_rail_df[breakfast_rail_df['RealSpeed'] <= 5]
grouped = b_walk.groupby('ID')
for name, group in grouped:
    grouped_place = group.groupby(['X','Y'])
    for name_place , group_place in grouped_place:
        index = group_place.index
        breakfast_rail_df.loc[index , 'FreeSpeed'] = np.percentile(group_place['RealSpeed'],99)
 
b_bike=breakfast_rail_df[(breakfast_rail_df['RealSpeed'] > 5)&(breakfast_rail_df['RealSpeed'] <= 8.5)]
grouped = b_bike.groupby('ID')
for name, group in grouped:
    grouped_place = group.groupby(['X','Y'])
    for name_place , group_place in grouped_place:
        index = group_place.index
        breakfast_rail_df.loc[index , 'FreeSpeed'] = np.percentile(group_place['RealSpeed'],99)

b_bike1=breakfast_rail_df[(breakfast_rail_df['RealSpeed'] > 8.5)&(breakfast_rail_df['RealSpeed'] <= 13.5)]
grouped = b_bike1.groupby('ID')
for name, group in grouped:
    grouped_place = group.groupby(['X','Y'])
    for name_place , group_place in grouped_place:
        index = group_place.index
        breakfast_rail_df.loc[index , 'FreeSpeed'] = np.percentile(group_place['RealSpeed'],99)

b_e=breakfast_rail_df[breakfast_rail_df['RealSpeed'] > 13.5]
grouped = b_e.groupby('ID')
for name, group in grouped:
    grouped_place = group.groupby(['X','Y'])
    for name_place , group_place in grouped_place:
        index = group_place.index
        breakfast_rail_df.loc[index , 'FreeSpeed'] = np.percentile(group_place['RealSpeed'],99)  
        
breakfast_rail_df['CDI'] = breakfast_rail_df['FreeSpeed']/breakfast_rail_df['RealSpeed']
breakfast_rail_df.to_csv(r"C:\Users\DELL\Desktop\新数据\B.csv")