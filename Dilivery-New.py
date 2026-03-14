import pandas as pd
import numpy as np

df=pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月.csv",header=0)
dili=pd.read_excel(r"C:\Users\DELL\Desktop\外卖领取点信息.xlsx",header=0)
action=pd.read_excel(r"C:\Users\DELL\Desktop\行为性质.xlsx",header=0)
diliplace=dili[["Place","DeliveryPlace"]]
df=df[df["ID"]<=30]
def secondshift(x):
    return x.hour*3600+x.minute*60+x.second

def preprocessing(df):
    df['Time']=pd.to_datetime(df['Time'])
    df["Day"]=df["Time"].apply(lambda x: x.strftime("%Y/%m/%d"))
    df["Second"]=df["Time"].apply(secondshift)
    sametime=[]
    for i in range(df.shape[0]-1):
        if abs(df.loc[i+1,"Second"]-df.loc[i,"Second"])<=15  :
            sametime.append(i)
    df.drop(df.index[sametime],inplace=True)
    return df
df = preprocessing(df)

def Informationupdate(df, diliplace,action):
    # 按照 'Day'、'St_ID' 和 'Time' 对数据框 df 排序
    df = df.sort_values(by=['Day', 'ID', 'Time'])  
    # 按照 'Place' 进行左关联
    df = df.merge(diliplace, on='Place', how='left')
    df=df.merge(action, on="Type_l", how="left")
    return df
df = Informationupdate(df, diliplace,action)

def getdormitory(x):
    y=x.groupby("ID")    
    for name,grouped in y:
        try:
            z=grouped[grouped["Action"]==2]
            a=z.iloc[0]["Place"]
        except:
            a=None
        ID=grouped.iloc[0]["ID"]
        x.loc[x["ID"]==ID,"Dor"]=a
        
    return x
df=getdormitory(df)

def validlunch(second):
    # 判断时间是否在午餐的时间范围内（10:30 - 13:30）
    if 37800 < second < 48600:
        return True  
    else:
        return False 

# 验证是否为合法的晚餐时间
def validdinner(second):
    # 判断时间是否在晚餐的时间范围内（16:30 - 19:30）
    if 59400 < second < 70200:
        return True  
    else:
        return False

def validbreakfast(second):
    # 判断时间是否在晚餐的时间范围内（16:30 - 19:30）
    if 23400 < second < 32400:
        return True  
    else:
        return False
    
def mealisnot(x, y):
    try:
        if y == "早餐" or y == "午餐" or y == "晚餐":
            x = x.reset_index(drop=True)
            number = x.shape[0] 
            for i in range(number):
                if x.loc[i, "Type_s"] == y or x.loc[i, "Type_s"] == "其他":
                    return True 
                    break 
                else:
                    pass 
            return False 
    except:
        return "Error! Choose the right type of meal!"

df["Breakfast"] = df.apply(lambda row: 1 if validbreakfast(row['Second']) else 0, axis=1)
df['Lunch'] = df.apply(lambda row: 1 if validlunch(row['Second']) else 0, axis=1)
df['Dinner'] = df.apply(lambda row: 1 if validdinner(row['Second']) else 0, axis=1)
df['Lunchtype'] = 0
df['Dinnertype'] = 0
df['Breakfasttype'] = 0
grouped = df.groupby(['Day', 'ID'])
dili=dili.set_index(["Place"])
for name, group in grouped:
    # 初始化为0，如果有餐则更新为1
    lunch_sum = group['Lunch'].sum()
    dinner_sum = group['Dinner'].sum()
    breakfast_sum = group['Breakfast'].sum()
    if breakfast_sum == 0:
        df.loc[group.index, 'Breakfasttype'] = 0#无法识别
    elif mealisnot(group, "早餐"):
        df.loc[group.index, 'Breakfasttype'] = 2#在校就餐
    else:
        df.loc[group.index, 'Breakfasttype'] = 1#还未识别的
    if lunch_sum == 0:
        df.loc[group.index, 'Lunchtype'] = 0#无法识别
    elif mealisnot(group, "午餐"):
        df.loc[group.index, 'Lunchtype'] = 2#在校就餐
    else:
        df.loc[group.index, 'Lunchtype'] = 1#还未识别的
    
    # 标记晚餐类型
    if dinner_sum == 0:
        df.loc[group.index, 'Dinnertype'] = 0
    elif mealisnot(group, "晚餐"):
        df.loc[group.index, 'Dinnertype'] = 2
    else:
        df.loc[group.index, 'Dinnertype'] = 1
    
df['Time']=pd.to_datetime(df['Time'])
df['Day'] = pd.to_datetime(df['Day'])

def Gatetimes(df):
    df=df.sort_values(by=["Time"])
    df['Gatetimes'] = 0
    for i in range(len(df)):
        if pd.isna(df.iloc[i]['DeliveryPlace']):
            df.iloc[i, df.columns.get_loc('Gatetimes')] = 0
        else:
            forward_count = 0
            for j in range(i - 1, -1, -1):
                #如果'DeliveryPlace'的值与i行的不同了，中断计数
                if pd.isna(df.iloc[j]['DeliveryPlace']) or df.iloc[j]['DeliveryPlace'] != df.iloc[i]['DeliveryPlace']:
                    break
                forward_count += 1
            backward_count = 0
            for k in range(i + 1, len(df)):
                #如果'DeliveryPlace'的值与i行的不同了，中断计数
                if pd.isna(df.iloc[k]['DeliveryPlace']) or df.iloc[k]['DeliveryPlace'] != df.iloc[i]['DeliveryPlace']:
                    break
                backward_count += 1
            df.iloc[i, df.columns.get_loc('Gatetimes')] = forward_count + backward_count + 1
    return df

def process_meal(df, meal_type_key, meal_key):
    meal_df = df[(df[meal_type_key] == 1) & (df[meal_key] == 1)]
    grouped = meal_df.groupby(['Day', 'ID'])

    for name, group in grouped:
        original_indices = group.index
        updated_group = Gatetimes(group.copy())
        df.loc[original_indices, ['Gatetimes']] = updated_group[['Gatetimes']]

    grouped2 = df[df[meal_type_key] == 1].groupby(['Day', 'ID'])
    for name, group in grouped2:
        if group[meal_key].eq(1).any():
            if (group['Gatetimes'] >= 2).any():
                df.loc[group.index, meal_type_key] = 5
            elif (group['Gatetimes'] == 1).any():
                df.loc[group.index, meal_type_key] = 6
            else:
                df.loc[group.index, meal_type_key] = 7

# 处理午餐
process_meal(df, 'Lunchtype', 'Lunch')
# 处理晚餐
process_meal(df, 'Dinnertype', 'Dinner')

def Timetype_1(df):
    # 排序数据框，按照 'Time' 列升序排列
    df = df.sort_values(by='Time')

    df['OutTimes'] = 0
    df['DiliTimes'] = 0

    # 筛选 'Lunchtype' 为 1 且 'Gatetimes' 大于等于 2 的行
    df_filtered = df[(df['Gatetimes'] >= 2)]

    # 遍历筛选后的行，计算相邻行中 'DeliveryPlace' 相同的组，并计算时间差
    for i in range(len(df_filtered) - 1):
        if df_filtered.iloc[i]['DeliveryPlace'] == df_filtered.iloc[i+1]['DeliveryPlace']:
            time_diff =df_filtered.iloc[i+1]['Second'] - df_filtered.iloc[i]['Second']

            if time_diff > 900:
                df.loc[df_filtered.index[i], 'OutTimes'] += 1
            elif time_diff <= 900:
                df.loc[df_filtered.index[i], 'DiliTimes'] += 1

    return df

def process_meal2(df, meal_type_key, meal_key):
    meal_df = df[(df[meal_type_key] == 5) & (df[meal_key] == 1)]
    grouped = meal_df.groupby(['Day', 'ID'])

    for name, group in grouped:
        original_indices = group.index
        updated_group = Timetype_1(group.copy())
        df.loc[original_indices, ['OutTimes']] = updated_group[['OutTimes']]
        df.loc[original_indices, ['DiliTimes']] = updated_group[['DiliTimes']]

    grouped2 = df[df[meal_type_key] == 5].groupby(['Day', 'ID'])
    for name, group in grouped2:
        if group[meal_key].eq(1).any():
            if (group['OutTimes'] == 1).any():
                df.loc[group.index, meal_type_key] = 3
            elif (group['DiliTimes'] == 1).any():
                df.loc[group.index, meal_type_key] = 4
            else:
                df.loc[group.index, meal_type_key] = 6
                
    return df

def process_meal3(df, meal_type_key, meal_key):
    meal_df = df[(df[meal_type_key] == 6) & (df[meal_key] == 1)]
    grouped=meal_df.groupby(["Day","ID"])
    
    for name,group in grouped:
        original_indices = group.index
        group = group.reset_index(drop=False)
        group_filtered=group[group["Gatetimes"] == 1]
        group_filtered=group_filtered.reset_index(drop=False)
        outnum,dilinum=0,0
        
        if len(group_filtered) >=2 :
            for i in range(len(group_filtered)-1):
                if group_filtered.loc[i+1,"Act_ID"] - group_filtered.loc[i,"Act_ID"] == 1:
                    place1,time1=group_filtered.loc[i,"Place"],group_filtered.loc[i,"Second"]
                    place2,time2=group_filtered.loc[i+1,"Place"],group_filtered.loc[i+1,"Second"]
                    time_diff=time2 - time1 - dili.loc[place1,place2]
                    if time_diff < 0 :
                        group_filtered.loc[i,"OutTimes"] = 0
                        group_filtered.loc[i,"DiliTimes"] = 0
                    elif 0 < time_diff < 1200:
                        group_filtered.loc[i,"DiliTimes"] = 1
                    else:
                        group_filtered.loc[i,"OutTimes"] = 1 
                        
                    if group_filtered["OutTimes"].eq(1).any():
                        outnum += 1
                    elif group_filtered["DiliTimes"].eq(1).any():
                        dilinum += 1
                        
                elif group_filtered.loc[i+1,"Act_ID"] - group_filtered.loc[i,"Act_ID"] > 1:
                    index1,index2=group_filtered.loc[i,"index"],group_filtered.loc[i+1,"index"]
                    group_new=group.iloc[index1:index2]
                    group_new = group_new.reset_index(drop=False)
                    group_new["TimeDiff"] = 0
                    for i in range(len(group_new)-1):
                        if group_new.loc[i,"Action"] != group_new.loc[i+1,"Action"]:
                            time = group_new.loc[i+1,"Second"] - group_new.loc[i,"Second"]
                            if time >= 480 :
                                group_new.loc[i,"TimeDiff"] = time
                    group_new["TimeDiff"]=group_new["TimeDiff"].agg("min")
                    group_new["OutTimes"]=group_new["TimeDiff"].apply(lambda x: 1 if x > 1500 else 0) 
                    group_new["DiliTimes"]=group_new["OutTimes"].apply(lambda x: 1 if x == 0 else 0)
                    
                    if group_filtered["OutTimes"].eq(1).any():
                        outnum += 1
                    elif group_filtered["DiliTimes"].eq(1).any():
                        dilinum += 1
            if outnum > dilinum:
                df.loc[original_indices,"OutTimes"] = 1
                df.loc[original_indices,meal_type_key] = 3
            elif dilinum >= outnum:
                df.loc[original_indices,"DiliTimes"] = 1
                df.loc[original_indices,meal_type_key] = 4
                    
    return df

'''
Parameters
----------
df : TYPE
    DESCRIPTION.
meal_type_key : TYPE
    DESCRIPTION.
meal_key : TYPE
    DESCRIPTION.

Returns
-------
df : TYPE
    DESCRIPTION.
    
Fiction process_meal4包含三部分处理，分别为对于门为饭点记录首次/中间/末次
处理只包含数据量 >= 2的部分数据,处理完后 mealtype = 6 表示有门记录但无法处理者
'''
def process_meal4(df, meal_type_key, meal_key):
    
    meal_df = df[(df[meal_type_key] == 6) & (df[meal_key] == 1)]
    grouped=meal_df.groupby(["Day","ID"])
    
    for name,group in grouped:

        original_indices = group.index
        group = group.reset_index(drop=False)
        group_filtered=group[group["Gatetimes"] == 1]
        if len(group_filtered) == 1:
            if group_filtered.index[0] == group.index[0]:
                if len(group) == 2:
                    if group.loc[1,"Action"] == 1 or group.loc[1,"Action"] ==3 :
                        time_diff = group.loc[1,"Second"] - group.loc[0,"Second"]
                        if time_diff <= 2400 :
                            df.loc[original_indices,"OutTimes"] = 1
                            df.loc[original_indices,meal_type_key] = 3
                        elif 2400 < time_diff <= 4800 :
                            df.loc[original_indices,"DiliTimes"] = 1
                            df.loc[original_indices,meal_type_key] = 4
                        else: pass
                elif len(group) >= 3:
                    count = 0   
                    time_sta = 0
                    for i in range(len(group)-1):
                        time_diff = group.loc[i+1,"Second"] - group.loc[i,"Second"]
                        if time_diff >= 1200:
                            if time_diff > time_sta:
                                time_sta = time_diff
                                index_need = i
                        else: count += 1
                    if count == len(group) - 1:
                        df.loc[original_indices,"OutTimes"] = 1
                        df.loc[original_indices,meal_type_key] = 3
                    else:
                        if group.loc[index_need,"Action"] != 2 and group.loc[index_need+1,"Action"] != 2:
                            df.loc[original_indices,"OutTimes"] = 1
                            df.loc[original_indices,meal_type_key] = 3
                        else:
                            if group.loc[index_need,"Action"] == 3 or group.loc[index_need+1,"Action"] == 3:
                                if time_sta < 1800:
                                    df.loc[original_indices,"OutTimes"] = 1
                                    df.loc[original_indices,meal_type_key] = 3
                                elif time_sta >= 1800:
                                    df.loc[original_indices,"DiliTimes"] = 1
                                    df.loc[original_indices,meal_type_key] = 4
                            elif group.loc[index_need,"Action"] != 3 or group.loc[index_need+1,"Action"] != 3:
                                if time_sta < 2700:
                                    df.loc[original_indices,"OutTimes"] = 1
                                    df.loc[original_indices,meal_type_key] = 3
                                elif time_sta >= 2700:
                                    df.loc[original_indices,"DiliTimes"] = 1
                                    df.loc[original_indices,meal_type_key] = 4
            elif group_filtered.index[0] == group.index[len(group)-1]:
                time_early={"Lunch":41400,"Dinner":61200}    #作为辅助识别,取出提早就餐和推迟就餐两种避峰措施的常识时间节点
                time_late={"Lunch":44400,"Dinner":64200}     #分别为中午11:30,12:20 ; 晚上17:00,17:50
                if len(group) >= 2:
                    if group.loc[len(group)-1,"Second"] - group.loc[len(group)-2,"Second"] >= 2400:
                        df.loc[original_indices,"OutTimes"] = 1
                        df.loc[original_indices,meal_type_key] = 3
                    else:
                       if df.loc[len(group)-1,"Second"] >= time_late[meal_key]:
                           index_last = original_indices[-1]
                           today=group["Day"].values[0]
                           ID = group["ID"].values[0]
                           if index_last != df[df[["Day","ID"]]==[today,ID]].index[-1]:
                               time_next = df[df[["Day","ID"]]==[today,ID]].loc[index_last + 1,"Second"]
                               if time_next - group.loc[len(group)-1,"Second"] <= 9000:
                                   if 900 <= time_next - group.loc[len(group)-1,"Second"] <= 2400:
                                       df.loc[original_indices,"DiliTimes"] = 1
                                       df.loc[original_indices,meal_type_key] = 4
                                   elif time_next - group.loc[len(group)-1,"Second"] > 2400:
                                       df.loc[original_indices,"OutTimes"] = 1
                                       df.loc[original_indices,meal_type_key] = 3 
                           else:
                               if 900 <= group.loc[len(group)-1,"Second"] - group.loc[len(group)-2,"Second"] < 2400:
                                   df.loc[original_indices,"DiliTimes"] = 1
                                   df.loc[original_indices,meal_type_key] = 4
                       elif df.loc[len(group)-1,"Second"] <= time_early[meal_key]:
                           index_first = original_indices[0]
                           today=group["Day"].values[0]
                           ID = group["ID"].values[0]
                           mask = (df.loc[index_first - 1,"Action"] == None)|(df.loc[index_first - 1,"Action"] == 2)
                           try:
                               time_early = df[df[["ID","Day"]]==[ID,today]].loc[index_first - 1,"Second"]
                               if group.loc[0,"Second"] - time_early <= 5400 and mask:
                                   if 900 <= group.loc[0,"Second"] - time_early <= 2400:
                                       df.loc[original_indices,"DiliTimes"] = 1
                                       df.loc[original_indices,meal_type_key] = 4
                                   elif group.loc[0,"Second"] - time_early > 2400:
                                       df.loc[original_indices,"OutTimes"] = 1
                                       df.loc[original_indices,meal_type_key] = 3
                           except:
                               if 900 <= group.loc[len(group)-1,"Second"] - group.loc[len(group)-2,"Second"] < 2400:
                                   df.loc[original_indices,"DiliTimes"] = 1
                                   df.loc[original_indices,meal_type_key] = 4
            else:
                index = group_filtered.index[0]
                action_early,action_later = group.loc[index - 1,"Action"] , group.loc[index + 1,"Action"]
                time_early,time_later = group.loc[index - 1,"Second"] , group.loc[index + 1,"Second"]
                time_diff_early = group.loc[index,"Second"] - time_early
                time_diff_later = time_later - group.loc[index,"Second"]
                if (action_early == 3)|(action_early == 1) and (action_later == 3)|(action_later == 1):                  
                    if time_diff_early <= 900:
                        if time_diff_later >= 1950:                       #这个参数十分关键，必须通过科学的方法进行确定,考虑问卷等
                            df.loc[original_indices,"OutTimes"] = 1       #目前采用比例平衡法，即找到sigema使得午晚餐外食与外卖比例相等
                            df.loc[original_indices,meal_type_key] = 3
                        elif 900 < time_diff_later < 1950:
                            today=group["Day"].values[0]
                            ID = group["ID"].values[0]
                            index_last = original_indices[-1]
                            try :
                                action_late = df[df[["ID","Day"]]==[ID,today]].loc[index_last + 1,"Action"]
                                time_latest = df[df[["ID","Day"]]==[ID,today]].loc[index_last + 1,"Second"]
                                mask1 = df[df[["ID","Action"]]==[ID,2]].loc[0,"Campus"] == group.loc[len(group) - 1,"Campus"]
                                if action_late == 0 and time_latest - group.loc[len(group) - 1,"Second"] <= 900 and mask1:
                                    df.loc[original_indices,"DiliTimes"] = 1
                                    df.loc[original_indices,meal_type_key] = 4
                                else: 
                                    df.loc[original_indices,"OutTimes"] = 1
                                    df.loc[original_indices,meal_type_key] = 3
                            except:
                                pass
                    elif time_diff_later <= 900:
                        if time_diff_early >= 1950:                      #目前采用30分钟(外卖界限顶用时与外食界限底用时的均值)
                            df.loc[original_indices,"OutTimes"] = 1
                            df.loc[original_indices,meal_type_key] = 3
                        elif 900 < time_diff_early <1950:                #若可能应对这部分再考虑,找到更为合适的处理方法！
                            df.loc[original_indices,"DiliTimes"] = 1
                            df.loc[original_indices,meal_type_key] = 4
                    else:
                        if time_later - time_early >=3000:
                            df.loc[original_indices,"OutTimes"] = 1
                            df.loc[original_indices,meal_type_key] = 3
                elif (action_early == 3)|(action_early == 1) and action_later == 2:
                    if time_diff_early <= 1950 and time_diff_later <= 900:
                        df.loc[original_indices,"DiliTimes"] = 1
                        df.loc[original_indices,meal_type_key] = 4
                    elif time_diff_early > 1950 and time_diff_later <= 900:
                        df.loc[original_indices,"OutTimes"] = 1
                        df.loc[original_indices,meal_type_key] = 3
                    else:
                        if time_later - time_early >=3000:
                            df.loc[original_indices,"OutTimes"] = 1
                            df.loc[original_indices,meal_type_key] = 3
                        else:
                            df.loc[original_indices,"OutTimes"] = 1
                            df.loc[original_indices,meal_type_key] = 4                                           
    return df

    '''
    之前的处理仅将饭点记录进行更改,而后面grouped.agg处理均取first值,故须对当天全部值进行覆盖
    '''
def process_type6(df,meal_type_key):
    grouped = df.groupby(["Day","ID"])
    for name, group in grouped:
        original_indices = group.index
        if group[meal_type_key].eq(6).any() :
            all_meal = list(group[meal_type_key].values)
            real_meal = 6
            for j in all_meal:
                if j != 6:
                    real_meal = j
            df.loc[original_indices,meal_type_key] = real_meal                   
    return df

# 处理午餐
df=process_meal2(df, 'Lunchtype', 'Lunch')
# 处理晚餐
df=process_meal2(df, 'Dinnertype', 'Dinner')
df=process_meal3(df, 'Lunchtype', 'Lunch')
df=process_meal3(df, 'Dinnertype', 'Dinner')
df=process_meal4(df, 'Lunchtype', 'Lunch')
df=process_meal4(df, 'Dinnertype', 'Dinner')
df=process_type6(df, 'Lunchtype')
df=process_type6(df, 'Dinnertype')
df=df.sort_values(by=["ID","Act_ID"])
df.to_csv(r"C:\Users\DELL\Desktop\校园活动信息5月-1.csv",header=True,index=False)
print(df.head())

grouped = df.groupby(['Day', 'ID'])
# 对每个分组保留唯一行，并只保留特定字段
unique_rows = grouped.agg({
    'Day': 'first',  # 保留'Day'
    'ID': 'first',  # 保留'St_ID'
    'OutTimes': 'sum',  # 计算总'OutTimes'
    'DiliTimes': 'sum',  # 计算总'DiliTimes'
    'Lunch': 'first',  # 保留'Lunch'
    'Lunchtype': 'first',  # 保留'Lunchtype'
    'Dinner': 'first',  # 保留'Dinner'
    'Dinnertype': 'first', #保留'DinnerType'
    'Dor':'first', #保留'Dor'宿舍信息
    'Breakfasttype': 'first' #保留'Breakfast'
})

# 分类计数和计算占比
def calculate_counts_and_proportions(df, column):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'Counts']
    counts['Proportion'] = (counts['Counts'] / counts['Counts'].sum()) * 100
    return counts

# 计算'Lunchtype'、'Dinnertype'、'OutTimes'和'DiliTimes'的分类计数及占比
breakfasttype_stats = calculate_counts_and_proportions(unique_rows, 'Breakfasttype')
lunchtype_stats = calculate_counts_and_proportions(unique_rows, 'Lunchtype')
dinnertype_stats = calculate_counts_and_proportions(unique_rows, 'Dinnertype')
outtimes_stats = calculate_counts_and_proportions(unique_rows, 'OutTimes')
dilitimes_stats = calculate_counts_and_proportions(unique_rows, 'DiliTimes')

# 输出结果
print("Breakfasttype Statistics:\n", breakfasttype_stats)
print("Lunchtype Statistics:\n", lunchtype_stats)
print("Dinnertype Statistics:\n", dinnertype_stats)
print("OutTimes Statistics:\n", outtimes_stats)
print("DiliTimes Statistics:\n", dilitimes_stats)
unique_rows.to_csv(r"C:\Users\DELL\Desktop\校园活动信息5月-2.csv")