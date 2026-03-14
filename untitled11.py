# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 16:50:47 2025

@author: DELL
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
import seaborn as sns
from scipy.stats import *
from time import strftime
warnings.filterwarnings('ignore')
pd.options.display.notebook_repr_html=True 
plt.rcParams['font.sans-serif']=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False 

unique_rows = pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月-2.csv",encoding = 'ansi')
unique_rows_man = unique_rows[unique_rows['Gender'] == '男']
unique_rows_woman = unique_rows[unique_rows['Gender'] == '女']
def calculate_counts_and_proportions(df1, df2, column):
    counts1 = df1[column].value_counts().reset_index()
    counts1.columns = [column, 'Counts']
    counts2 = df2[column].value_counts().reset_index()
    counts2.columns = [column, 'Counts']
    counts1['Proportion'] = (counts2['Counts'] / counts1['Counts'].sum()) * 100
    return counts1

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
breakfasttype_stats = calculate_counts_and_proportions(unique_rows,unique_rows, 'Breakfasttype')
lunchtype_stats = calculate_counts_and_proportions(unique_rows,unique_rows, 'Lunchtype')
dinnertype_stats = calculate_counts_and_proportions(unique_rows,unique_rows, 'Dinnertype')
outtimes_stats = calculate_counts_and_proportions(unique_rows,unique_rows, 'OutTimes')
dilitimes_stats = calculate_counts_and_proportions(unique_rows,unique_rows, 'DiliTimes')
unique_rows["Lunchtype_Situation"] =unique_rows["Lunchtype"].apply(InOut)
unique_rows["Dinnertype_Situation"] =unique_rows["Dinnertype"].apply(InOut)
unique_rows.sort_values(by=["Lunchtype_Situation","Dinnertype_Situation"],inplace =True)

# 输出结果


#print('man:\n')
print("Breakfasttype Statistics:\n", breakfasttype_stats)

print("Lunchtype Statistics:\n", lunchtype_stats)
print("Dinnertype Statistics:\n", dinnertype_stats)
print("OutTimes Statistics:\n", outtimes_stats)
print("DiliTimes Statistics:\n", dilitimes_stats)

print(len(unique_rows_man),len(unique_rows_woman))

df=pd.read_csv(r"C:\Users\DELL\Desktop\校园活动信息5月-1.csv",header=0)
import scipy.stats as stats

    
import matplotlib.patches as mpatches
class analysis:
    
    #分析画图工具装入包中，方便对各类数据进行调用，对方法进行继承与装饰
    def __init__(self,df):
        self.df = df
    
    def Proportion(self,day,columns1,columns2,hue=None): 
        
        self.columns1 = columns1
        self.columns2 = columns2
        self.day = day
        self.hue = hue
        self.df[self.columns1] = self.df[self.columns1].replace({'Dilivery_Demae':'外卖就餐','Dinning_Hall':'食堂就餐','Eating_Out':'外出就餐','Unknown':'未识别'})
        if hue == None:
            title=self.day + self.columns1 +" & "+self.columns2
        else:
            title='晚餐就餐类型男女分布差异'
        plt.title(title)
        if hue == None:
            pass
         #   sns.histplot(data =self.df, x=self.columns1,color=' white ',label="{}".format(self.columns1),stat="density")
          ## plt.legend()
        else:
            ax=sns.histplot(data =self.df, x=self.columns1,kde = True,palette=['gray','black'],hue=self.hue,linewidth=2,multiple="dodge",stat="density",common_norm=False)
            
            hatches = ['/', '.', '', '.']
            for i in range(len(ax.patches)):
                ax.patches[i].set_hatch(hatches[i // len(self.df[self.columns1].unique())])
                ax.patches[i].set_linewidth(1)
            handles = [mpatches.Patch(facecolor=['gray','black'][i], edgecolor='black', hatch=['.', '/'][i]) for i in range(2)]
            legend_labels = ["女性","男性"]
            ax.legend(handles, legend_labels, loc='upper center', bbox_to_anchor=(0.8, 1), ncol=2, frameon=False)
            for bar in ax.patches:
                yval = bar.get_height()  # 获取柱子的高度
                ax.annotate(f'{yval:.3f}',  # 要标注的文本
                (bar.get_x() + bar.get_width() / 2-0.005, yval),  # 柱子的中心位置和高度
                ha='center', va='bottom',  # 水平和垂直对齐方式
                xytext=(0, 4),  # 文本偏移量
                textcoords='offset points',
                fontweight='bold'
                )  # 偏移单位
            plt.grid()
            ax.set_ylim(0,0.8)
        plt.xlabel("Situation")
    
    def ThirtyDay(self,meal,mealtype,kind,color,label,linewidth = 1):
        self.meal = meal
        self.kind = kind
        self.color = color
        self.label = label
        self.linewidth = linewidth
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
        title = '总体及各个宿舍每日晚餐吃外出频率'
        ax=plt.gca()
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['left'].set_linewidth(4)
        ax.spines['top'].set_linewidth(0)
        ax.spines['right'].set_linewidth(0)
        plt.title(title)
        plt.plot(df_weneed["Days"],df_weneed["Rate"],color = self.color ,label = self.label, linewidth = self.linewidth)
        plt.legend(loc = 'upper right')

        plt.scatter(df_filtered["Days"],df_filtered["Rate"],s=100,c="black",label="Tuesday",marker = 's')
        plt.scatter(df_filtered1["Days"],df_filtered1["Rate"],s=75,c="black",label="Weekend",marker = '^')
        plt.xticks(df_weneed["Days"],rotation = 45)
        plt.grid()
        
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
        title = "不同频度花销与外卖就餐频率"
        plt.title(title)
        ax1 = sns.histplot(data = result,x="Consum_notbreakfast",kde = True,palette =['gray','white'],hue = "BigSmall",linewidth=2)          #数据量为200时结果很理想，可以参考
        
        hatches = ['/', '.', '']
        i=0
        for i in range(len(ax1.patches)):
            ax1.patches[i].set_hatch(hatches[i //round(len(ax1.patches)/3)])
            ax1.patches[i].set_linewidth(1)
            i += 1
        handles = [mpatches.Patch(facecolor=['white','white','white'][i], edgecolor='black', hatch=['/', '.',''][i]) for i in range(3)]
        legend_labels = ["高频度外卖就餐","中频度外卖就餐",'低频度外卖就餐']
        ax1.legend(handles, legend_labels, loc='upper center', bbox_to_anchor=(0.8, 1), ncol=1, frameon=False)
        plt.xlabel('不计早餐的平均花销')
        plt.grid()
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
        title = '不同外出次数的平均花销'
        plt.title(title)
        real_result = real_result[real_result['Count'] < 15] 
        ax=plt.bar(real_result["Count"],real_result["Consum_amount"], alpha=0.6,label = "Real_Count",linewidth = 2,edgecolor='black',color='white')
        for i in range(15):
            ax.patches[i].set_hatch('/')
        plt.xlabel("次数")
        plt.ylabel("平均花销")

        for a, b in zip(real_result["Count"], real_result["Consum_amount"]):
            plt.text(a, b+0.5, str(round(b,1)), ha='center', va='bottom')
        plt.grid()
        '''
        poly_fit = np.polyfit(real_result["Count"], real_result["Consum_amount"], 1)
        slope = poly_fit[0]
        intercept = poly_fit[1]
        plt.plot(real_result["Count"], slope*real_result["Count"]+intercept, color='black',label="Simulator" , linestyle='--',linewidth = 2)'''
        plt.xlim(0,11.5)
        
    def DiliTimeHistplot(self,column):
        self.column = column
        statistic = df[df[self.column]==1]
        title = '晚餐取外卖进出校门时间分布'
        plt.title(title)
        statistic=statistic[statistic['Place'] == '国康路99号门（西北门）']
        statistic["hour"] = statistic["Second"] // 3600
        statistic["minute"] = (statistic["Second"] % 3600) // 60
        statistic["hour"] = statistic["hour"].astype("str")
        statistic["minute"] = statistic["minute"].astype("str")
        statistic["HourMinute"] = statistic["hour"] + ":" + statistic["minute"] +":00"
        statistic["HourMinute"] = pd.to_datetime(statistic["HourMinute"], format="%H:%M:%S").dt.time
        sns.histplot(data = statistic[statistic["DiliStart"] ==1],x="Second",bins=18,kde=True,label="取外卖出校门",stat="density")
        sns.histplot(data = statistic[statistic["DiliEnd"] ==1],x="Second",bins=18,kde=True,label="取完外卖回校门",stat="density")
        ax=sns.kdeplot(statistic["DiliMiddleHMS"],color="black",label="取外卖时间节点",linewidth = 3)
        #sns.distplot(statistic["DiliMiddleHMS"],hist=False,fit=norm,label="normal distribution")
        plt.xlim(58000,74000)
        ax.xaxis.set_ticks([x+21000 for x in [38400,39000,39600,40200,40800,41400,42000,42600,43200,43800,44400,45000,45600,46200,46800,47400,48000,48600,49200]],
                           ['16:30','16:40','16:50','17:00','17:10','17:20','17:30','17:40','17:50','18:00','18:10','18:20',
                            '18:30','18:40','18:50','19:00','19:10','19:20','19:30'],rotation = 45)
        plt.legend()
        plt.grid()
        print(statistic["HourMinute"])
        
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
        
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure(figsize=(36,27))
plt.rcParams.update({'font.size': 16})

analysis_plot_everydayeveryone = analysis(unique_rows)
fig.add_subplot(337)
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
analysis_plot_everydayeveryone.Proportion("All_day: ","Lunchtype_Situation",None,hue="Gender")
fig.add_subplot(338)
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
analysis_plot_everydayeveryone.Proportion("All_day: ","Dinnertype_Situation",None,hue="Gender")


analysis_plot_xinan2 = analysis(unique_rows[unique_rows['Dor'] == '西南二楼'])
analysis_plot_xibei2 = analysis(unique_rows[unique_rows['Dor'] == '西北二楼'])
analysis_plot_xinan12 = analysis(unique_rows[unique_rows['Dor'] == '西南十二楼'])
fig3=plt.figure(figsize=(16,48))
fig3.add_subplot(411)
analysis_plot_everydayeveryone.ThirtyDay("Lunch","Lunchtype","Dilivery",'black','总体',2.5)
analysis_plot_xinan2.ThirtyDay("Lunch","Lunchtype","Dilivery",'red','西南二楼')
analysis_plot_xibei2.ThirtyDay("Lunch","Lunchtype","Dilivery",'blue','西北二楼')
analysis_plot_xinan12.ThirtyDay("Lunch","Lunchtype","Dilivery",'orange','西南十二楼')
plt.grid()
fig3.add_subplot(412)
analysis_plot_everydayeveryone.ThirtyDay("Lunch","Lunchtype","OutEating",'black','总体',2.5)
analysis_plot_xinan2.ThirtyDay("Lunch","Lunchtype","OutEating",'red','西南二楼')
analysis_plot_xibei2.ThirtyDay("Lunch","Lunchtype","OutEating",'blue','西北二楼')
analysis_plot_xinan12.ThirtyDay("Lunch","Lunchtype","OutEating",'orange','西南十二楼')
plt.grid()
fig3.add_subplot(413)
analysis_plot_everydayeveryone.ThirtyDay("Dinner","Dinnertype","Dilivery",'black','总体',2.5)
analysis_plot_xinan2.ThirtyDay("Dinner","Dinnertype","Dilivery",'red','西南二楼')
analysis_plot_xibei2.ThirtyDay("Dinner","Dinnertype","Dilivery",'blue','西北二楼')
analysis_plot_xinan12.ThirtyDay("Dinner","Dinnertype","Dilivery",'orange','西南十二楼')
plt.grid()
fig3.add_subplot(414)
analysis_plot_everydayeveryone.ThirtyDay("Dinner","Dinnertype","OutEating",'black','总体',2.5)
analysis_plot_xinan2.ThirtyDay("Dinner","Dinnertype","OutEating",'red','西南二楼')
analysis_plot_xibei2.ThirtyDay("Dinner","Dinnertype","OutEating",'blue','西北二楼')
analysis_plot_xinan12.ThirtyDay("Dinner","Dinnertype","OutEating",'orange','西南十二楼')
plt.grid()
plt.close()

fig.add_subplot(331)
analysis_plot_everydayeveryone.Price("Lunchtype","Dinnertype","OutEating")
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
fig.add_subplot(332)
analysis_plot_everydayeveryone.Price("Lunchtype","Dinnertype","Dilivery")
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)
fig.add_subplot(333)
analysis_plot_everydayeveryone.Price2("Lunchtype","Dinnertype","OutEating")
ax=plt.gca()
ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)
ax.spines['top'].set_linewidth(0)
ax.spines['right'].set_linewidth(0)

fig.add_subplot(334)
analysis_plot_everydayeveryone.DiliTimeHistplot("Lunch")
fig.add_subplot(335)
analysis_plot_everydayeveryone.DiliTimeHistplot("Dinner")

fig.add_subplot(336)
analysis_plot_everydayeveryone.OnlyTimeHistplot("StandardTimeDiff")