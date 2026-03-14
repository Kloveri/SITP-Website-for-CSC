# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 14:41:33 2025

@author: DELL
"""

import pandas as pd
import numpy as np
from time import gmtime
from time import strftime
import datetime
from datetime import timedelta
import colorsys
df=pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月-1.csv",header=0)
dili=pd.read_excel(r"C:\Users\DELL\Desktop\外卖领取点信息.xlsx",header=0)
action=pd.read_excel(r"C:\Users\DELL\Desktop\行为性质.xlsx",header=0)
diliplace=dili[["Place","DeliveryPlace"]]
df=df[df["ID"]==114]
geo_location = pd.read_csv(r"C:\Users\DELL\Desktop\校园POI信息.csv",header=0,encoding="ansi")
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings
from scipy.stats import *
from time import strftime
warnings.filterwarnings('ignore')
import osmnx as ox
G = ox.graph_from_bbox((121.49001, 31.278084, 121.504942, 31.290312),
                       network_type='all', truncate_by_edge=False )
for i in list(G.edges()):
    try:
        G.get_edge_data(i[0],i[1])[1]
        G.remove_edge(i[0], i[1])
    except:
        pass
    G.get_edge_data(i[0],i[1])[0]['len'] = 0
    print(G.get_edge_data(i[0],i[1]))
    #print(G.get_edge_data(i[0],i[1]))
color = ox.plot.get_edge_colors_by_attr(G , attr ='len',start = 0 , stop = 1 , cmap='RdYlGn', na_color='none')
ox.plot.plot_graph(G , edge_color = color)
print(G.edges())

df_lunch = df[df['Dinner'] == 1]
grouped = df_lunch.groupby('Day')
for day, action in grouped:
    if not len(action) == 1:
        for lenth in range(len(action) - 1):
            action_first = action.iloc[lenth]['Place']
            action_last = action.iloc[lenth + 1]['Place']
            action_first_geo_lng , action_first_geo_lat = geo_location[geo_location['Place'] == action_first]['Lng'] ,geo_location[geo_location['Place'] == action_first]['Lat']
            action_last_geo_lng , action_last_geo_lat = geo_location[geo_location['Place'] == action_last]['Lng'] ,geo_location[geo_location['Place'] == action_last]['Lat']
            start_node, dist_start_node = ox.nearest_nodes(G, action_first_geo_lng, action_first_geo_lat, return_dist=True)
            end_node, dist_end_node = ox.nearest_nodes(G, action_last_geo_lng, action_last_geo_lat, return_dist=True)
            route = ox.shortest_path(G, start_node, end_node, weight="length")
            try:
                fig, ax = ox.plot_graph_route(G, route[0], route_color="y", route_linewidth=6, node_size=0) 
            except: pass
            
            print(action_first , action_last)
            
