# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:39:34 2025

@author: DELL
"""
import numpy as np
import pandas as pd
import math
import requests
df=pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月.csv",header=0)
place_all = df["Place"].unique()
r_pi = np.pi * 3000/180
pi = math.pi
ob = 0.00669342162296594323
la = 6378245.0
def judge_China(lon, lat):
    if lon < 70 or lon > 140:
        return True
    if lat < 0 or lat > 55:
        return True
    return False
def bd09_gcj02(lon_bd09, lat_bd09):
    m = lon_bd09 - 0.0065
    n = lat_bd09 - 0.006
    c = np.sqrt(m * m + n * n) - 0.00002 * np.sin(n * r_pi)
    o = math.atan2(n, m) - 0.000003 * math.cos(m * r_pi)
    lon_gcj02 = c * math.cos(o)
    lat_gcj02 = c * math.sin(o)
    return [lon_gcj02, lat_gcj02]
def transformlat(lon, lat):
    r = -100.0 + 2.0 * lon + 3.0 * lat + 0.2 * lat * lat + 0.1 * lon * lat + 0.2 * math.sqrt(math.fabs(lon))
    r += (20.0 * math.sin(6.0 * lon * pi) + 20.0 * math.sin(2.0 * lon * pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    r += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return r
def transformlng(lon, lat):
    r = 300.0 + lon + 2.0 * lat + 0.1 * lon * lon + 0.1 * lon * lat + 0.1 * math.sqrt(math.fabs(lon))
    r += (20.0 * math.sin(6.0 * lon * pi) + 20.0 * math.sin(2.0 * lon * pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(lon * pi) + 40.0 * math.sin(lon / 3.0 * pi)) * 2.0 / 3.0
    r += (150.0 * math.sin(lon / 12.0 * pi) + 300.0 * math.sin(lon / 30.0 * pi)) * 2.0 / 3.0
    return r

def gcj02_wgs84(lon_gcj02, lat_gcj02):
    if judge_China(lon_gcj02, lat_gcj02):
        return [lon_gcj02, lat_gcj02]
    tlat = transformlat(lon_gcj02 - 105.0, lat_gcj02 - 35.0)
    tlng = transformlng(lon_gcj02 - 105.0, lat_gcj02 - 35.0)
    rlat = lat_gcj02 / 180.0 * pi
    m = math.sin(rlat)
    m = 1 - ob * m * m
    sm = math.sqrt(m)
    tlat = (tlat * 180.0) / ((la * (1 - ob)) / (m * sm) * pi)
    tlng = (tlng * 180.0) / (la / sm * math.cos(rlat) * pi)
    lat_wgs84 = 2 * lat_gcj02 - (lat_gcj02 + tlat)
    lon_wgs84 = 2 * lon_gcj02 - (lon_gcj02 + tlng)
    return [lon_wgs84, lat_wgs84]
def bd09_wgs84(lon_bd09, lat_bd09):
    tmpList_gcj02 = bd09_gcj02(lon_bd09, lat_bd09)
    return gcj02_wgs84(tmpList_gcj02[0], tmpList_gcj02[1])

geolist = []
for i in place_all:
    params = {
    "address":    "上海市杨浦区同济大学" + str(i),
    "output":    "json",
    "ak":       "AP8AvIuokSzdDCRYCs48H7mvNElUqK8E"}
    r = requests.get(url='https://api.map.baidu.com/geocoding/v3',params = params)
    result = r.json()
    try:     
        lng,lat = result['result']['location']['lng'] , result['result']['location']['lat']
        lng_new , lat_new = bd09_wgs84(lng, lat)[0] , bd09_wgs84(lng, lat)[1]
        #MY API KEY
    except:
        lng_new , lat_new = np.nan , np.nan
    print(result['status'])
    geolist.append([i,lng_new,lat_new])
    
from geopy.geocoders import Nominatim
def get_location_info(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((latitude, longitude), language='en')
    return location

geoDataframe = pd.DataFrame(geolist,columns=["Place","Lng","Lat"])
geoDataframe.to_csv(r"C:\Users\DELL\Desktop\校园POI信息.csv")
print(geoDataframe)
