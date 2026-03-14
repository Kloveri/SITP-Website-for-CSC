# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 21:16:52 2025

@author: DELL
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

breakfast_rail_df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\C.csv",header=0,encoding='ansi')
POI = pd.read_csv(r"C:\Users\DELL\Desktop\校园POI信息.csv",header=0,encoding='ansi')
breakfast_rail_df = pd.merge(left = breakfast_rail_df , right = POI , left_on = 'X', right_on = 'Place')
breakfast_rail_df = breakfast_rail_df.rename(columns={'Lng':'X_Lng','Lat':'X_Lat'})
breakfast_rail_df = pd.merge(left = breakfast_rail_df , right = POI , left_on = 'Y', right_on = 'Place')
breakfast_rail_df = breakfast_rail_df.rename(columns={'Lng':'Y_Lng','Lat':'Y_Lat'})
breakfast_rail_df.to_csv(r"C:\Users\DELL\Desktop\新数据\C.csv")