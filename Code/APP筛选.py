# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 00:43:44 2025

@author: DELL
"""

import pandas as pd
import numpy as np
original = pd.read_excel(r"C:\Users\DELL\Desktop\APP清单_ident.xlsx")
li = pd.read_excel(r"C:\Users\DELL\Desktop\数据库中所有app名称（深圳）.xlsx")
original = original.apply(lambda x: x.astype(str).str.upper())
li=li.apply(lambda x: x.astype(str).str.upper())
infor = pd.DataFrame([],columns=['orignal','new'])
a=0
original['IsNot'] = 1
for i in range(len(original)):
    #if not li['app_name'].value_counts()[original.loc[i,'APP']] > 0:
    if not li['app_name'].isin([original.loc[i,'APP']]).any():
        original.loc[i,'IsNot'] = 0
        
        index = li[li['app_name'].str.contains(original.loc[i,'APP'])].index
        if not len(index) == 0: 
            value = li.loc[index]
            value['new'] = original.loc[i,'APP']
            a+=1
            print(value)
            infor = pd.concat([infor ,value] )
            
    
        
infor.to_csv(r'C:\Users\DELL\Desktop\检查信息.csv')
original['是否在联通系统内'] = original['是否在联通系统内'].replace({'是':1,"否":0})
original['Check'] = original['是否在联通系统内'] - original['IsNot']
original['Check'] = original['Check'].replace({0:np.nan,1:'待检查',-1:'待检查'})
original.to_excel(r"C:\Users\DELL\Desktop\APP清单_ident_New.xlsx")
print(original.head(100))
