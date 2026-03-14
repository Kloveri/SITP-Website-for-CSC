# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 10:11:48 2025

@author: lenovo
"""

import pandas as pd
import matplotlib.pyplot as plt

#读取数据
file_path = "E:\上课不良行为检测\校园活动信息5月.csv"
df_raw = pd.read_csv(file_path)


#清洗与预处理
#只保留合法ID和时间列
df = df_raw[['ID', 'Type_l', 'Type_s', 'Time']].copy()
df = df[df['ID'].apply(lambda x: isinstance(x, (int, str)) and str(x).isdigit())]
df['ID'] = df['ID'].astype(int)
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
df = df.dropna(subset=['Time'])

# 按学生分组，提高效率
groups = df.sort_values('Time').groupby('ID')

#检测迟到/旷课行为
#为每个学生：提取所有“上课安排”记录，按节次配对上课开始和结束时间段；查找其余活动是否落在这些时间段内，若有则计为一次迟到/旷课行为

results = []

for student_id, g in groups:
    records = g[['Type_s', 'Time']].values.tolist()
    
    class_periods = []
    stack = []
    
    for act, t in records:
        if '上课' in act and '下课' not in act:
            stack.append(t)
        elif '下课' in act and stack:
            start = stack.pop(0)
            end = t
            class_periods.append((start, end))
    
    violations = 0
    for act, t in records:
        if '上课' in act or '下课' in act:
            continue
        for start, end in class_periods:
            if start <= t <= end:
                violations += 1
                break
    
    results.append((student_id, violations))

#统计与可视化
res_df = pd.DataFrame(results, columns=['ID', 'violations'])
res_df.to_csv("E:\上课不良行为检测\学生违纪行为统计.csv", index=False, encoding='utf-8-sig')
plt.figure(figsize=(10, 6))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.hist(res_df['violations'], bins=20, edgecolor='black', color='steelblue')
plt.xlabel('迟到/旷课行为次数')
plt.ylabel('学生人数')
plt.title('学生在上课时间进行其他活动行为次数分布')
plt.grid(axis='y')
plt.tight_layout()
plt.show()
