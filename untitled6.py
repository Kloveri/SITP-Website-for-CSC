# -*- coding: utf-8 -*-
"""
Created on Fri May 30 11:38:05 2025

@author: DELL
"""

import networkx as nx 
import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd 

G = ox.graph_from_bbox((121.48401, 31.274084, 121.513942, 31.295312), network_type='all', truncate_by_edge=False )
ox.save_graph_geopackage(G, filepath="shp\同济大学周边道路网络.gpkg") 
#ox.save_graphml(G, filepath=r"C:\Users\DELL\Desktop\同济大学周边道路网络.graphml") 
ox.plot_graph(G, bgcolor="white", node_color="blue", edge_color="gray", 
              node_size=10, edge_linewidth=0.5) 