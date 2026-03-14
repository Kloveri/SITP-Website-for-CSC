import pandas as pd
import numpy as np
from time import gmtime
from time import strftime
import datetime
from datetime import timedelta

df=pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月.csv",header=0)
print(len(df))
#df = pd.read_csv(r"C:\Users\DELL\Desktop\新数据\新示例数据.csv",header=0)
dili=pd.read_excel(r"C:\Users\DELL\Desktop\外卖领取点信息.xlsx",header=0)
action=pd.read_excel(r"C:\Users\DELL\Desktop\行为性质.xlsx",header=0)
diliplace=dili[["Place","DeliveryPlace"]]
df=df[df["ID"]<=2000]
def secondshift(x):
    return x.hour*3600+x.minute*60+x.second

'Dor'
def preprocessing(df):
    df['Time']=pd.to_datetime(df['Time'])
    df["Day"]=df["Time"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["Time"] = df["Time"].astype("datetime64[ns]")  
    df["Week"]=df["Time"].apply(lambda x: x.strftime("%A"))
    df["Second"]=df["Time"].apply(secondshift)
    df["HMS"] = df["Second"]
    df["HMS"]=df["HMS"].map(lambda x:strftime('%H:%M:%S',gmtime(x)))
    sametime=[]
    for i in range(df.shape[0]-1):
        if abs(df.loc[i+1,"Second"]-df.loc[i,"Second"])<=15  :
            sametime.append(i)
    df.drop(df.index[sametime],inplace=True)
    return df
df = preprocessing(df)

'''
def preprocessing(df):
    df['Time']=pd.to_datetime(df['Time'] , format = 'ISO8601')
    df["Day"]=df["Time"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["Time"] = df["Time"].astype("datetime64[ns]")  
    df["Week"]=df["Time"].apply(lambda x: x.strftime("%A"))
    df["Second"]=df["Time"].apply(secondshift)
    df["HMS"] = df["Second"]
    df["HMS"]=df["HMS"].map(lambda x:strftime('%H:%M:%S',gmtime(x)))
    sametime=[]
    for i in range(df.shape[0]-1):
        if abs(df.loc[i+1,"Second"]-df.loc[i,"Second"])<=15  :
            sametime.append(i)
    df.drop(df.index[sametime],inplace=True)
    return df
df = preprocessing(df)
'''
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
df['Breakfasttype'] = 0
df['Lunchtype'] = 0
df['Dinnertype'] = 0

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

process_meal(df, "Breakfasttype", "Breakfast")
# 处理午餐
process_meal(df, 'Lunchtype', 'Lunch')
# 处理晚餐
process_meal(df, 'Dinnertype', 'Dinner')

def is_Outtime(index, meal_type_key ,df):
    df.loc[index,"OutTimes"] = 1
    df.loc[index,meal_type_key] = 3
    return df

def is_Dilitime(index, meal_type_key ,df):
    df.loc[index,"OutTimes"] = 1
    df.loc[index,meal_type_key] = 4
    return df
    
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
                df.loc[df_filtered.index[i], 'DiliTimes'] += 1       #取出吃外卖的开始节点, 为新加的内容
                df.loc[df_filtered.index[i], 'DiliStart'] = 1        #取出吃外卖的中止节点, 为新加的内容
                df.loc[df_filtered.index[i+1], 'DiliEnd'] = 1
                df.loc[df_filtered.index[i], 'DiliMiddleHMS'] = (df.loc[df_filtered.index[i], 'Second']+df.loc[df_filtered.index[i+1], 'Second'])/2

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
                index_weneed = original_indices[0]
                for i in range(original_indices[0],original_indices[-1] - 1):
                    if df.loc[i,"Gatetimes"] ==2 and df.loc[i+1,"Gatetimes"] ==2:
                        index_weneed = i 
                    else:
                        pass
                df.loc[index_weneed, "DiliStart"] = 1
                df.loc[index_weneed + 1,"DiliEnd"] = 1
                df.loc[index_weneed, "DiliMiddleHMS"] = (df.loc[index_weneed, "Second"]+df.loc[index_weneed + 1,"Second"])/2
                    
            else:
                df.loc[group.index, meal_type_key] = 6      #特殊划归处理
                
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
                is_Outtime(original_indices, meal_type_key, df)
            elif dilinum >= outnum:
                is_Dilitime(original_indices, meal_type_key, df)
                index_weneed = original_indices[0]
                index_weneed1 = original_indices[-1]
                time = 10000
                for i in range(len(group_filtered) - 1):
                    if group_filtered.iloc[i+1]["Second"] - group_filtered.iloc[i]["Second"] < time:
                        time = group_filtered.iloc[i+1]["Second"] - group_filtered.iloc[i]["Second"]
                        index_weneed = group_filtered.iloc[i]["index"]
                        index_weneed1 = group_filtered.iloc[i+1]["index"]
                df.loc[index_weneed,"DiliStart"] = 1
                df.loc[index_weneed1,"DiliEnd"] = 1
                df.loc[index_weneed, "DiliMiddleHMS"] = (df.loc[index_weneed, "Second"]+df.loc[index_weneed1,"Second"])/2
                df.loc
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
                            is_Outtime(original_indices, meal_type_key, df)
                        elif 2400 < time_diff <= 4800 :
                            is_Dilitime(original_indices, meal_type_key, df)
                            df.loc[original_indices[0],'DiliStart'] = 1        #为新加的内容
                            df.loc[original_indices[-1],'DiliEnd'] = 1
                            df.loc[original_indices[0],'DiliMiddleHMS'] = (df.loc[original_indices[0],'Second']+df.loc[original_indices[-1],'Second'])/2
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
                        is_Outtime(original_indices, meal_type_key, df)
                    else:
                        if group.loc[index_need,"Action"] != 2 and group.loc[index_need+1,"Action"] != 2:
                            is_Outtime(original_indices, meal_type_key, df)
                        else:
                            if group.loc[index_need,"Action"] == 3 or group.loc[index_need+1,"Action"] == 3:
                                if time_sta < 1800:
                                    is_Outtime(original_indices, meal_type_key, df)
                                elif time_sta >= 1800:
                                    is_Dilitime(original_indices, meal_type_key, df)
                                    df.loc[original_indices[index_need],'DiliStart'] = 1
                                    df.loc[original_indices[index_need+1],'DiliEnd'] = 1 
                                    df.loc[index_need, "DiliMiddleHMS"] = (df.loc[index_need, "Second"]+df.loc[index_need + 1,"Second"])/2
                            elif group.loc[index_need,"Action"] != 3 or group.loc[index_need+1,"Action"] != 3:
                                if time_sta < 2700:
                                    is_Outtime(original_indices, meal_type_key, df)
                                elif time_sta >= 2700:
                                    is_Dilitime(original_indices, meal_type_key, df)
                                    df.loc[original_indices[i],'DiliStart'] = 1
                                    df.loc[original_indices[i+1],'DiliEnd'] = 1 
                                    df.loc[original_indices[i],'DiliMiddleHMS'] = (df.loc[original_indices[i],'Second']+df.loc[original_indices[i+1],'Second'])/2
                                    
            elif group_filtered.index[0] == group.index[len(group)-1]:
                time_early={"Lunch":41400,"Dinner":61200}    #作为辅助识别,取出提早就餐和推迟就餐两种避峰措施的常识时间节点
                time_late={"Lunch":44400,"Dinner":64200}     #分别为中午11:30,12:20 ; 晚上17:00,17:50
                if len(group) >= 2:
                    if group.loc[len(group)-1,"Second"] - group.loc[len(group)-2,"Second"] >= 2400:
                        is_Outtime(original_indices, meal_type_key, df)
                    else:
                       if df.loc[len(group)-1,"Second"] >= time_late[meal_key]:
                           index_last = original_indices[-1]
                           today=group["Day"].values[0]
                           ID = group["ID"].values[0]
                           if index_last != df[df[["Day","ID"]]==[today,ID]].index[-1]:
                               time_next = df[df[["Day","ID"]]==[today,ID]].loc[index_last + 1,"Second"]
                               if time_next - group.loc[len(group)-1,"Second"] <= 9000:
                                   if 900 <= time_next - group.loc[len(group)-1,"Second"] <= 2400:
                                       is_Dilitime(original_indices, meal_type_key, df)
                                       df.loc[index_last,'DiliStart'] = 1                #新加的内容
                                       df.loc[index_last + 1,'DiliEnd'] = 1              #新加的内容
                                       df.loc[index_last,'DiliMiddleHMS'] = (df.loc[index_last,'Second']+df.loc[index_last + 1,'Second'])/2
                                   elif time_next - group.loc[len(group)-1,"Second"] > 2400:
                                       is_Outtime(original_indices, meal_type_key, df) 
                           else:
                               if 900 <= group.loc[len(group)-1,"Second"] - group.loc[len(group)-2,"Second"] < 2400:
                                   is_Dilitime(original_indices, meal_type_key, df)
                                   df.loc[index_last - 1,'DiliStart'] = 1                #新加的内容
                                   df.loc[index_last ,'DiliEnd'] = 1              #新加的内容
                                   df.loc[index_last - 1,'DiliMiddleHMS'] = (df.loc[index_last - 1,'Second']+df.loc[index_last,'Second'])/2
                       elif df.loc[len(group)-1,"Second"] <= time_early[meal_key]:
                           index_first = original_indices[0]
                           today=group["Day"].values[0]
                           ID = group["ID"].values[0]
                           mask = (df.loc[index_first - 1,"Action"] == None)|(df.loc[index_first - 1,"Action"] == 2)
                           try:
                               time_early = df[df[["ID","Day"]]==[ID,today]].loc[index_first - 1,"Second"]
                               if group.loc[0,"Second"] - time_early <= 5400 and mask:
                                   if 900 <= group.loc[0,"Second"] - time_early <= 2400:
                                       is_Dilitime(original_indices, meal_type_key, df)
                                       df.loc[index_first - 1,'DiliStart'] = 1                #新加的内容
                                       df.loc[index_first ,'DiliEnd'] = 1              #新加的内容
                                       df.loc[index_first - 1,'DiliMiddleHMS'] = (df.loc[index_first - 1,'Second']+df.loc[index_first,'Second'])/2
                                   elif group.loc[0,"Second"] - time_early > 2400:
                                       is_Outtime(original_indices, meal_type_key, df)
                           except:
                               if 900 <= group.loc[len(group)-1,"Second"] - group.loc[len(group)-2,"Second"] < 2400:
                                   is_Dilitime(original_indices, meal_type_key, df)
                                   df.loc[original_indices[-2],'DiliStart'] = 1  #新加的内容
                                   df.loc[original_indices[-1],'DiliEnd'] = 1  #新加的内容
                                   df.loc[original_indices[-2],'DiliMiddleHMS'] = (df.loc[original_indices[-2],'Second']+df.loc[original_indices[-1],'Second'])/2
            else:
                index = group_filtered.index[0]
                action_early,action_later = group.loc[index - 1,"Action"] , group.loc[index + 1,"Action"]
                time_early,time_later = group.loc[index - 1,"Second"] , group.loc[index + 1,"Second"]
                time_diff_early = group.loc[index,"Second"] - time_early
                time_diff_later = time_later - group.loc[index,"Second"]
                if (action_early == 3)|(action_early == 1) and (action_later == 3)|(action_later == 1):                  
                    if time_diff_early <= 900:
                        if time_diff_later >= 1950:                       #这个参数十分关键，必须通过科学的方法进行确定,考虑问卷等       
                            is_Outtime(original_indices, meal_type_key, df) #目前采用比例平衡法，即找到sigema使得午晚餐外食与外卖比例相等
                        elif 900 < time_diff_later < 1950:
                            today=group["Day"].values[0]
                            ID = group["ID"].values[0]
                            index_last = original_indices[-1]
                            try :
                                action_late = df[df[["ID","Day"]]==[ID,today]].loc[index_last + 1,"Action"]
                                time_latest = df[df[["ID","Day"]]==[ID,today]].loc[index_last + 1,"Second"]
                                mask1 = df[df[["ID","Action"]]==[ID,2]].loc[0,"Campus"] == group.loc[len(group) - 1,"Campus"]
                                if action_late == 0 and time_latest - group.loc[len(group) - 1,"Second"] <= 900 and mask1:
                                    is_Dilitime(original_indices, meal_type_key, df)
                                    df.loc[index_last + 1,'DiliEnd'] = 1   #新加的内容
                                    df.loc[index_last,'DiliStart'] = 1    #新加的内容
                                    df.loc[index_last,'DiliMiddleHMS'] = (df.loc[index_last,'Second']+df.loc[index_last + 1,'Second'])/2
                                else: 
                                    is_Outtime(original_indices, meal_type_key, df)
                            except:
                                pass
                    elif time_diff_later <= 900:
                        if time_diff_early >= 1950:                      #目前采用30分钟(外卖界限顶用时与外食界限底用时的均值)
                            is_Outtime(original_indices, meal_type_key, df)
                        elif 900 < time_diff_early <1950:                #若可能应对这部分再考虑,找到更为合适的处理方法
                            is_Dilitime(original_indices, meal_type_key, df)
                            df.loc[original_indices[group.index[index]] - 1,'DiliStart'] = 1   #新加的内容
                            df.loc[original_indices[group.index[index]] ,'DiliEnd'] = 1   #新加的内容
                            time_weneed = (df.loc[original_indices[group.index[index]] - 1,'Second']+df.loc[original_indices[group.index[index]],'Second'])/2
                            df.loc[original_indices[group.index[index]]-1,"DiliMiddleHMS"] = time_weneed
                    else:
                        if time_later - time_early >=3000:
                            is_Outtime(original_indices, meal_type_key, df)
                elif (action_early == 3)|(action_early == 1) and action_later == 2:
                    if time_diff_early <= 1950 and time_diff_later <= 900:
                        is_Dilitime(original_indices, meal_type_key, df)
                        df.loc[original_indices[group.index[index]] - 1,'DiliStart'] = 1   #新加的内容
                        df.loc[original_indices[group.index[index]] ,'DiliEnd'] = 1   #新加的内容
                        time_weneed = (df.loc[original_indices[group.index[index]] - 1,'Second']+df.loc[original_indices[group.index[index]],'Second'])/2
                        df.loc[original_indices[group.index[index]]-1,"DiliMiddleHMS"] = time_weneed
                    elif time_diff_early > 1950 and time_diff_later <= 900:
                        is_Outtime(original_indices, meal_type_key, df)
                    else:
                        if time_later - time_early >=3000:
                            is_Outtime(original_indices, meal_type_key, df)
                        else:
                            is_Dilitime(original_indices, meal_type_key, df)
                            df.loc[original_indices[group.index[index]] - 1,'DiliStart'] = 1   #新加的内容
                            df.loc[original_indices[group.index[index]] ,'DiliEnd'] = 1   #新加的内容
                            time_weneed = (df.loc[original_indices[group.index[index]] - 1,'Second']+df.loc[original_indices[group.index[index]],'Second'])/2
                            df.loc[original_indices[group.index[index]]-1,"DiliMiddleHMS"] = time_weneed
                elif action_early == 2 and action_later == 2:
                    if time_diff_early <= 900 and time_diff_later > 1950:
                        is_Dilitime(original_indices, meal_type_key, df)
                        df.loc[original_indices[group.index[index]] ,'DiliStart'] = 1   #新加的内容
                        df.loc[original_indices[group.index[index]] + 1 ,'DiliEnd'] = 1   #新加的内容
                        time_weneed = (df.loc[original_indices[group.index[index]],'Second']+df.loc[original_indices[group.index[index]] + 1,'Second'])/2
                        df.loc[original_indices[group.index[index]],"DiliMiddleHMS"] = time_weneed
                    elif time_diff_early > 1950 and time_diff_later <= 900:
                        is_Outtime(original_indices, meal_type_key, df)
                                           
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

df["DiliMiddleHMS"] = np.nan                           #后来新加的

for i in range(len(df) - 1):
    if df.loc[i,"Gatetimes"] == 2 and df.loc[i+1,"Gatetimes"] == 2:
        df.loc[i,"DiliStart"] = 1
        df.loc[i+1,"DiliEnd"] = 1 
        df.loc[i,"DiliMiddleHMS"] = (df.loc[i,"Second"]+df.loc[i+1,"Second"])/2 
        if df.loc[i+1,"Second"] - df.loc[i,"Second"]<=1500:                  #目前采用的参数是1500，可以考虑其他的参数！
            df.loc[i,"StandardTimeDiff"] = df.loc[i+1,"Second"] - df.loc[i,"Second"]
print(df.head())      
df["DiliMiddleHMS"] = round(df["DiliMiddleHMS"])


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

df["Days"] = df["Day"]
break_index = df[df["Breakfast"] == 0].index
df.loc[break_index,"Consum_notbreakfast"] = df.loc[break_index,"Consum_amount"]      
grouped = df.groupby(['Day', 'ID'])
# 对每个分组保留唯一行，并只保留特定字段

def get_student_id(ID) -> str:
    st_id = '265'
    in_id = '%04d'%(ID)
    return str(st_id + in_id)
df['Student_ID'] = df['ID'].apply(get_student_id)

unique_rows = grouped.agg({
    'Days':'first',    #保留天
    'ID':'first',      #保留ID
    'Consum_amount':'mean',   #计算食堂花销总额
    'Consum_notbreakfast':'mean',  #计算无早餐的食堂花销
    'Gender':'first',  #保留Gender
    'Week':'first',  #保留'Week'
    'OutTimes': 'sum',  # 计算总'OutTimes'
    'DiliTimes': 'sum',  # 计算总'DiliTimes'
    'Lunch': 'first',  # 保留'Lunch'
    'Lunchtype': 'first',  # 保留'Lunchtype'
    'Dinner': 'first',  # 保留'Dinner'
    'Dinnertype': 'first', #保留'DinnerType'
    'Dor':'first', #保留'Dor'宿舍信息
    'Breakfasttype': 'first', #保留'Breakfast'
    'Student_ID': 'first' #'Student_ID'
})

# 分类计数和计算占比
def calculate_counts_and_proportions(df, column):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'Counts']
    counts['Proportion'] = (counts['Counts'] / counts['Counts'].sum()) * 100
    return counts

def InOut(Type):
    if Type == 0 or Type == 6 or Type == 7:
        return "Unknown"
    elif Type == 2:
        return "Dinning_Hall"
    elif Type == 3:
        return "Eating_Out"
    elif Type ==4:
        return "Dilivery_Demae"
# 计算'Lunchtype'、'Dinnertype'、'OutTimes'和'DiliTimes'的分类计数及占比
breakfasttype_stats = calculate_counts_and_proportions(unique_rows, 'Breakfasttype')
lunchtype_stats = calculate_counts_and_proportions(unique_rows, 'Lunchtype')
dinnertype_stats = calculate_counts_and_proportions(unique_rows, 'Dinnertype')
outtimes_stats = calculate_counts_and_proportions(unique_rows, 'OutTimes')
dilitimes_stats = calculate_counts_and_proportions(unique_rows, 'DiliTimes')
unique_rows["Lunchtype_Situation"] =unique_rows["Lunchtype"].apply(InOut)
unique_rows["Dinnertype_Situation"] =unique_rows["Dinnertype"].apply(InOut)
unique_rows.sort_values(by=["Lunchtype_Situation","Dinnertype_Situation"],inplace =True)
# 输出结果
print("Breakfasttype Statistics:\n", breakfasttype_stats)
print("Lunchtype Statistics:\n", lunchtype_stats)
print("Dinnertype Statistics:\n", dinnertype_stats)
print("OutTimes Statistics:\n", outtimes_stats)
print("DiliTimes Statistics:\n", dilitimes_stats)
unique_rows.to_csv(r"C:\Users\DELL\Desktop\校园活动信息5月-2.csv")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings
from scipy.stats import *
from time import strftime
warnings.filterwarnings('ignore')

pd.options.display.notebook_repr_html=True
sns.set_theme(style='darkgrid')  
plt.rcParams['font.sans-serif']=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False 
'''
数据识别及统计至此结束
'''
'''
place_all = df["Place"].unique()
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
        #MY API KEY
    except:
        lng,lat = np.nan , np.nan
    print(result['status'])
    geolist.append([i,lng,lat])
geoDataframe = pd.DataFrame(geolist,columns=["Place","Lng","Lat"])
'''
import geopandas as gpd 
#geo_location = pd.read_csv(r"C:\Users\DELL\Desktop\a.csv",header=0,encoding="ansi")    #后面改
#gdf_location = gpd.GeoDataFrame(geo_location, geometry=gpd.points_from_xy(geo_location.Lng, geo_location.Lat))
import networkx as nx 
import osmnx as ox
import folium
class analysis:
    
    #分析画图工具装入包中，方便对各类数据进行调用，对方法进行继承与装饰
    def __init__(self,df):
        self.df = df
    
    def Proportion(self,day,columns1,columns2,hue=None):       
        self.columns1 = columns1
        self.columns2 = columns2
        self.day = day
        self.hue = hue
        if hue == None:
            title=self.day + self.columns1 +" & "+self.columns2
        else:
            title=self.day + self.columns1 +" By "+self.hue
        plt.title(title)
        if hue == None:
            sns.histplot(data =self.df, x=self.columns1,kde = True,label="{}".format(self.columns1),stat="density")
            sns.histplot(data =self.df, x=self.columns2,kde = True,label="{}".format(self.columns2),stat="density")
            plt.legend()
        else:
            sns.histplot(data =self.df, x=self.columns1,hue=self.hue,kde = True,stat="density",common_norm=False)
        plt.xlabel("Situation")
        #对实际识别情况绘制直方图,包含核密度图,观察校园卡使用情况及可靠性
        #以及包含对单一就餐的多种人群识别呈现,采用hue参数导入分类原则
        
    def Proportion_Predict(self,day,columns1,columns2):
        self.columns1 = columns1
        self.columns2 = columns2
        self.day = day
        count1 = self.df[self.columns1].value_counts()
        count1 = count1.astype("float")
        new_eatout = count1["Eating_Out"] +count1["Unknown"]*count1["Eating_Out"]/(count1["Eating_Out"]+count1["Dilivery_Demae"])
        new_dili = count1["Dilivery_Demae"] +count1["Unknown"]*count1["Dilivery_Demae"]/(count1["Eating_Out"]+count1["Dilivery_Demae"])
        count1["Eating_Out"] = new_eatout
        count1["Dilivery_Demae"] = new_dili
        count1.drop("Unknown",inplace=True)           #将Unknown平均分配到Dilibery和Outeating上
        count1 = count1/count1.sum()
        count2 = self.df[self.columns2].value_counts()
        count2 = count2.astype("float")
        new_eatout = count2["Eating_Out"] +count2["Unknown"]*count2["Eating_Out"]/(count2["Eating_Out"]+count2["Dilivery_Demae"])
        new_dili = count2["Dilivery_Demae"] +count2["Unknown"]*count2["Dilivery_Demae"]/(count2["Eating_Out"]+count2["Dilivery_Demae"])
        count2["Eating_Out"] = new_eatout
        count2["Dilivery_Demae"] = new_dili
        count2.drop("Unknown",inplace=True)          #将Unknown平均分配到Dilibery和Outeating上
        count2 = count2/count2.sum()
        title="Predict "+self.day + self.columns1 +" & "+self.columns2
        plt.title(title)
        plt.bar(np.arange(len(count1)), count1, width =0.4, alpha=0.6,label=self.columns1)
        plt.bar(np.arange(len(count2))+0.4, count2,width =0.4,alpha=0.6,label=self.columns2)
        plt.xticks(np.arange(len(count1))+0.2,count1.index)
        plt.xlabel("Situation")
        plt.ylabel("Ratio")
        plt.legend()
        print(count1)   
        #对理想情况（所有全部被识别）
        
    def Scatter_Sort(self,columns1,columns2,hue,by):
        self.columns1 = columns1
        self.columns2 = columns2
        self.hue = hue
        self.by = by
        columns_dili1 = "Dili" + self.columns1
        columns_out1 = "Out" + self.columns1
        columns_dili2 = "Dili" + self.columns1
        columns_out2 = "Out" + self.columns1
        self.df["Extra"] = 1
        self.df[columns_dili1] = self.df["Lunchtype"].apply(lambda x: 1 if x==4 else 0)
        self.df[columns_out1] = self.df["Lunchtype"].apply(lambda x: 1 if x==3 else 0)
        self.df[columns_dili2] = self.df["Dinnertype"].apply(lambda x: 1 if x==4 else 0)
        self.df[columns_out2] = self.df["Dinnertype"].apply(lambda x: 1 if x==3 else 0)
        grouped = self.df.groupby(self.hue)
        result_all = grouped.agg({"Gender":"first",   #保留Gender用作区分
                                  "Extra":"sum",      #取len的特殊列，可删除
                                  columns_dili1:"sum",   #取计算列诸下:
                                  columns_out1:"sum",
                                  columns_dili2:"sum",
                                  columns_out2:"sum",
                                  "ID":"first"          #取ID,保留扩展功能的可能性
                                  })
        result_all["OutTime"] = result_all[columns_out1] + result_all[columns_out2]
        result_all["DiliTime"] = result_all[columns_dili1] + result_all[columns_dili2]
        result_all["OutRate"] = result_all["OutTime"]/(result_all["Extra"]*2)
        result_all["DiliRate"] = result_all["DiliTime"]/(result_all["Extra"]*2)
        title = "Meal_of: " + self.columns1 + " " + self.columns2 + " By " +self.hue
        plt.title(title)
        sns.scatterplot(data = result_all,x= "OutRate", y="DiliRate",hue=self.hue,size=self.by)
        plt.plot([0,min(max(result_all["OutRate"]),max(result_all["DiliRate"]))],
                 [0,min(max(result_all["OutRate"]),max(result_all["DiliRate"]))],color="black",linestyle='--')
        plt.legend(fontsize=7,loc="upper right")
        self.df.drop(["Extra"],axis = 1)
        #对各个宿舍进行外出就餐与校内就餐的分类，并按男女宿舍进行分类
        
    def DiliTimeHistplot(self,column):
        self.column = column
        statistic = df[df[self.column]==1]
        title = "Density of Dilivery take and back of " +self.column
        plt.title(title)
        
        statistic["hour"] = statistic["Second"] // 3600
        statistic["minute"] = (statistic["Second"] % 3600) // 60
        statistic["hour"] = statistic["hour"].astype("str")
        statistic["minute"] = statistic["minute"].astype("str")
        statistic["HourMinute"] = statistic["hour"] + ":" + statistic["minute"] +":00"
        statistic["HourMinute"] = pd.to_datetime(statistic["HourMinute"], format="%H:%M:%S").dt.time
        sns.histplot(data = statistic[statistic["DiliStart"] ==1],x="Second",bins=18,kde=True,label="Take",stat="density")
        sns.histplot(data = statistic[statistic["DiliEnd"] ==1],x="Second",bins=18,kde=True,label="Back",stat="density")
        sns.kdeplot(statistic["DiliMiddleHMS"],color="black",label="Standard",linewidth = 3)
        sns.distplot(statistic["DiliMiddleHMS"],hist=False,fit=norm,label="normal distribution")
        plt.legend()
        print(statistic["HourMinute"])
        #绘制三个直方图与核密度曲线，一条为开始取外卖时间点，一条为取完外卖后行为时间点（注意！指的是去玩外卖后第一条有记录的行为）
        #第三条为时间的中点，用于代表取外卖的密度，这是比较合适的
        
    def OnlyTimeKDEplot(self,column):
        df["WhichMeal"] = df["Lunch"] - df["Dinner"]
        target_value={-1:"Dinner",0:"Breakfast",1:"Lunch"}
        df["WhichMeal"] = df["WhichMeal"].map(target_value)
        self.column = column
        title = "Density of "+ self.column
        plt.title(title)
        sns.kdeplot(data=df, x="Second",y=self.column,hue="WhichMeal")
        #绘制随时间变化取外卖时间的变化值
        
    def OnlyTimeHistplot(self,column):
        self.column = column
        title = "Density of " + self.column
        plt.title(title)
        sns.histplot(data=df,x=self.column,kde = True,fill=True,label=self.column)

    def HowMuchTime(self,meal1,meal2,kind):
        di = {"Dilivery":4,"OutEating":3}
        self.meal1 = meal1
        self.meal2 = meal2
        self.kind = kind
        self.df["Count1"] = self.df[self.meal1].apply(lambda x: 1 if x==di[self.kind] else 0)
        self.df["Count2"] = self.df[self.meal2].apply(lambda x: 1 if x==di[self.kind] else 0)
        self.df["New_ID"] = self.df["ID"]
        grouped = self.df.groupby(["New_ID"])
        result = grouped.agg({"New_ID":"first",
                              "Consum_amount":"mean",
                              "Count1":"sum",
                              "Count2":"sum"})
        title = "Number of Students of " + self.kind
        plt.title(title)
        sns.histplot(data=result,x="Count1",kde = True,fill = False,label=self.meal1)
        sns.histplot(data=result,x="Count2",kde = True,fill = False,label=self.meal2)
        plt.xlabel(self.kind)
        plt.legend()
        #画出外卖与外食各个次数的学生个数，上次也有

    def Price(self,meal1,meal2,kind):
        di = {"Dilivery":4,"OutEating":3}
        self.meal1 = meal1
        self.meal2 = meal2
        self.kind = kind
        self.df["Count1"] = self.df[self.meal1].apply(lambda x: 1 if x==di[self.kind] else 0)
        self.df["Count2"] = self.df[self.meal2].apply(lambda x: 1 if x==di[self.kind] else 0)
        self.df["New_ID"] = self.df["ID"]
        grouped = self.df.groupby(["New_ID"])
        result = grouped.agg({"New_ID":"first",
                              "Consum_notbreakfast":"mean",
                              "Count1":"sum",
                              "Count2":"sum"})
        result["Count"] = result["Count1"] + result["Count2"]          #还没有学会装饰器，先复制过来了~(>_<)~
        bins ={"Dilivery":[0,2,5,100],"OutEating":[0,4,8,100]}
        result["BigSmall"] = pd.cut(result["Count"],bins[self.kind],labels=["Small","Normal","Big"])
        title = "Consume of Dinning Hall of Different frequency of " + self.kind
        plt.title(title)
        sns.histplot(data = result,x="Consum_notbreakfast",kde = True,hue = "BigSmall")          #数据量为200时结果很理想，可以参考
        #画出各个外卖外食消费频度的消费者在食堂的消费量，探究食堂对外食的影响
    
    def Price2(self,meal1,meal2,kind):
        di = {"Dilivery":4,"OutEating":3}
        self.meal1 = meal1
        self.meal2 = meal2
        self.kind = kind
        self.df["Count1"] = self.df[self.meal1].apply(lambda x: 1 if x==di[self.kind] else 0)
        self.df["Count2"] = self.df[self.meal2].apply(lambda x: 1 if x==di[self.kind] else 0)
        self.df["New_ID"] = self.df["ID"]
        grouped = self.df.groupby(["New_ID"])
        result = grouped.agg({"New_ID":"first",
                              "Consum_amount":"mean",
                              "Count1":"sum",
                              "Count2":"sum"})
        result["Count"] = result["Count1"] + result["Count2"]
        new_grouped = result.groupby(["Count"])
        real_result = new_grouped.agg({"Count":"first","Consum_amount":"mean"})
        title = "Consume of Dinning Hall of Different Times of " + self.kind 
        plt.title(title)
        plt.bar(real_result["Count"],real_result["Consum_amount"], alpha=0.6,label = "Real_Count")
        plt.xlabel("Times")
        plt.ylabel("Consum")
        poly_fit = np.polyfit(real_result["Count"], real_result["Consum_amount"], 1)
        slope = poly_fit[0]
        intercept = poly_fit[1]
        plt.plot(real_result["Count"], slope*real_result["Count"]+intercept, color='black',label="Simulator")
        #绘制不同食堂花销金额的人数，并做回归预测分析
    
    def From(self,meal,kind):
        self.meal = meal
        self.kind = kind
        df_filtered = df[["Place","Action","DiliStart",self.meal]]
        index = df_filtered[df_filtered[["DiliStart",self.meal]] == [1,1]].index        
        index_weneed = []
        for i in index:
            index_weneed.append(i-1)
        index_weneed = index_weneed[1:]
        df_we = df_filtered.loc[index_weneed]
        df_weneed = df_we.loc[df_we["Action"] == self.kind]
        df_weneed["Actiontext"] = df_weneed["Action"].map({np.nan:"DinningHall",0:"Door",1:"Library",2:"Dormitory",3:"Class"})
        title = "From Where of Who Eat Dilivery of " + self.meal + "of" + "Special Kind"
        plt.title(title)
        chart = sns.histplot(data = df_weneed, x="Place",hue="Actiontext",label="Where")
        chart. set_xticklabels ( chart.get_xticklabels (), rotation= 45)
        #绘制不同人从哪里来
    
    def FromAll(self,meal):
        self.meal = meal
        df_filtered = df[["Place","Action","DiliStart",self.meal]]
        index = df_filtered[df_filtered[["DiliStart",self.meal]] == [1,1]].index        
        index_weneed = []
        for i in index:
            index_weneed.append(i-1)
        index_weneed = index_weneed[1:]
        df_weneed = df.loc[index_weneed]
        df_weneed["Actiontext"] = df_weneed["Action"].map({np.nan:"DinningHall",0:"Door",1:"Library",2:"Dormitory",3:"Class"})
        title = "From Where of Who Eat Dilivery of " + self.meal
        plt.title(title)
        sns.histplot(data = df_weneed, x="Actiontext",hue="Actiontext",label="Where")
        #绘制不同类型来人数量
      
    def To(self,meal,kind):
        self.meal = meal
        self.kind = kind
        df_filtered = df[["Place","Action","DiliEnd",self.meal]]
        index = df_filtered[df_filtered[["DiliEnd",self.meal]] == [1,1]].index        
        index_weneed = []
        for i in index:
            index_weneed.append(i+1)
        index_weneed = index_weneed[:-1]
        df_we = df_filtered.loc[index_weneed]
        df_weneed = df_we.loc[df_we["Action"] == self.kind]
        df_weneed["Actiontext"] = df_weneed["Action"].map({np.nan:"DinningHall",0:"Door",1:"Library",2:"Dormitory",3:"Class"})
        title = "To Where of Who Eat Dilivery of " + self.meal + "of" + "Special Kind"
        plt.title(title)
        chart = sns.histplot(data = df_weneed, x="Place",hue="Actiontext",label="Where")
        chart. set_xticklabels ( chart.get_xticklabels (), rotation= 45)
        #绘制不同类型人去哪里
      
    def ToAll(self,meal):
        self.meal = meal
        df_filtered = df[["Place","Action","DiliEnd",self.meal]]
        index = df_filtered[df_filtered[["DiliEnd",self.meal]] == [1,1]].index        
        index_weneed = []
        for i in index:
            index_weneed.append(i+1)
        index_weneed = index_weneed[:-1]
        df_weneed = df.loc[index_weneed]
        df_weneed["Actiontext"] = df_weneed["Action"].map({np.nan:"DinningHall",0:"Door",1:"Library",2:"Dormitory",3:"Class"})
        title = "To Where of Who Eat Dilivery of " + self.meal
        plt.title(title)
        sns.histplot(data = df_weneed, x="Actiontext",hue="Actiontext",label="Where")
        #绘制不同类型去人数量   
        
    def ThirtyDay(self,meal,mealtype,kind):
        self.meal = meal
        self.kind = kind
        self.mealtype = mealtype
        di = {"Dilivery":4,"OutEating":3}
        df_meal = self.df
        df_meal["Count_Dili"] = df_meal[self.mealtype].apply(lambda x:1 if x == di[self.kind] else 0)
        df_meal["All"] = 1
        df_grouped = df_meal.groupby(["Day"])
        df_weneed = df_grouped.agg({"Days":"first","Count_Dili":"sum","All":"sum","Week":"first"})
        df_weneed["Rate"] = df_weneed["Count_Dili"]/df_weneed["All"]
        df_weneed=df_weneed.sort_values("Days")
        df_weneed["Week"]
        df_filtered = df_weneed.loc[df_weneed["Week"] == "Tuesday"]
        df_filtered1 = df_weneed.loc[df_weneed["Week"].isin(["Saturday","Sunday"]) == True]
        title = "Rate of " +self.meal +"of" + self.kind + "of 30Days"
        plt.title(title)
        plt.plot(df_weneed["Days"],df_weneed["Rate"])
        plt.scatter(df_filtered["Days"],df_filtered["Rate"],s=100,c="black",label="Tuesday")
        plt.scatter(df_filtered1["Days"],df_filtered1["Rate"],s=75,c="red",label="Weekend")
        plt.xticks(df_weneed["Days"],rotation = 45)
        plt.legend()
        #绘制月变化
'''    
    def Route(self):

        G = ox.graph_from_bbox((121.49001, 31.278084, 121.508942, 31.292312),
                               network_type='all', truncate_by_edge=False )
        ox.plot_graph(G, bgcolor="white", node_color="blue", edge_color="gray", 
              node_size=10, edge_linewidth=0.5) 
        ox.plot.plot_footprints(gdf_location['geometry'])     #后面改
        return True
'''

#创建绘图区,方便比较绘图
fig=plt.figure(figsize=(24,18))

#创建对象,全部目标 
fig.add_subplot(331)
analysis_plot_everydayeveryone = analysis(unique_rows)
analysis_plot_everydayeveryone.Proportion("All_day: ","Lunchtype_Situation","Dinnertype_Situation", )
fig.add_subplot(334)
analysis_plot_everydayeveryone.Proportion_Predict("All_day_Predict: ","Lunchtype_Situation","Dinnertype_Situation")
#对宿舍进行结果分析
fig.add_subplot(339)
analysis_plot_everydayeveryone.Scatter_Sort("OutTime","DiliTime",hue="Dor",by="Gender")

#创建对象,平常日（1-5）
fig.add_subplot(332)
analysis_plot_workdayeveryone = analysis(unique_rows[(unique_rows["Week"] != "Saturday")&(unique_rows["Week"] != "Sunday")])
analysis_plot_workdayeveryone.Proportion("Work_day: ","Lunchtype_Situation","Dinnertype_Situation", )
fig.add_subplot(335)
analysis_plot_workdayeveryone.Proportion_Predict("Work_day_Predict: ","Lunchtype_Situation","Dinnertype_Situation")

#创建对象，周末（67）
fig.add_subplot(333)
analysis_plot_weekdayeveryone = analysis(unique_rows[(unique_rows["Week"] == "Saturday")|(unique_rows["Week"] == "Sunday")])
analysis_plot_weekdayeveryone.Proportion("Week_day: ","Lunchtype_Situation","Dinnertype_Situation", )
fig.add_subplot(336)
analysis_plot_weekdayeveryone.Proportion_Predict("Week_day_Predict: ","Lunchtype_Situation","Dinnertype_Situation")

#创建对象,男女分别
fig.add_subplot(337)
analysis_plot_everydayeveryone.Proportion("All_day: ","Lunchtype_Situation",None,hue="Gender")
fig.add_subplot(338)
analysis_plot_everydayeveryone.Proportion("All_day: ","Dinnertype_Situation",None,hue="Gender")

fig1=plt.figure(figsize=(24,18))
fig1.add_subplot(331)
analysis_plot_everydayeveryone.DiliTimeHistplot("Lunch")
fig1.add_subplot(332)
analysis_plot_everydayeveryone.DiliTimeHistplot("Dinner")
fig1.add_subplot(333)
analysis_plot_everydayeveryone.OnlyTimeKDEplot("StandardTimeDiff")
fig1.add_subplot(334)
analysis_plot_everydayeveryone.OnlyTimeHistplot("StandardTimeDiff")
fig1.add_subplot(335)
analysis_plot_everydayeveryone.HowMuchTime("Lunchtype","Dinnertype","Dilivery")
fig1.add_subplot(336)
analysis_plot_everydayeveryone.HowMuchTime("Lunchtype","Dinnertype","OutEating")
fig1.add_subplot(337)
analysis_plot_everydayeveryone.Price("Lunchtype","Dinnertype","OutEating")
fig1.add_subplot(338)
analysis_plot_everydayeveryone.Price("Lunchtype","Dinnertype","Dilivery")
fig1.add_subplot(339)
analysis_plot_everydayeveryone.Price2("Lunchtype","Dinnertype","Dilivery")


fig2=plt.figure(figsize=(24,18))
analysis_plot_everydayeveryonenew = analysis(unique_rows)
fig2.add_subplot(321)
analysis_plot_everydayeveryonenew.From("Lunch",2)
fig2.add_subplot(322)
analysis_plot_everydayeveryonenew.From("Lunch",3)
fig2.add_subplot(323)
analysis_plot_everydayeveryonenew.FromAll("Lunch")
fig2.add_subplot(324)
analysis_plot_everydayeveryonenew.ToAll("Lunch")
fig2.add_subplot(325)
analysis_plot_everydayeveryonenew.To("Lunch",2)
fig2.add_subplot(326)
analysis_plot_everydayeveryonenew.To("Lunch",3)

fig3=plt.figure(figsize=(24,28))
fig3.add_subplot(411)
analysis_plot_everydayeveryone.ThirtyDay("Lunch","Lunchtype","Dilivery")
fig3.add_subplot(412)
analysis_plot_everydayeveryone.ThirtyDay("Lunch","Lunchtype","OutEating")
fig3.add_subplot(413)
analysis_plot_everydayeveryone.ThirtyDay("Dinner","Dinnertype","Dilivery")
fig3.add_subplot(414)
analysis_plot_everydayeveryone.ThirtyDay("Dinner","Dinnertype","OutEating")
fig3.show()

