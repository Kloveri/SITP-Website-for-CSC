import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as st
import pandas as pd
import scipy.cluster as cl
plt.rcParams['font.sans-serif']=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False 
dfCities=pd.read_csv(r"C:\Users\DELL\Desktop\cities.csv")
x=dfCities["常住人口"].dropna()

plt.close("all")
fig=plt.hist(x)

plt.close("all")
sm.qqplot(x,loc=np.mean(x),scale=np.std(x),line="45")


x1= dfCities.loc[dfCities["南北"]=="北方","常住人口"]
x2= dfCities.loc[dfCities["南北"]=="南方","常住人口"]


x1=dfCities.loc[dfCities["东中西"]=="东部","常住人口"]
x2=dfCities.loc[dfCities["东中西"]=="中部","常住人口"]
x3=dfCities.loc[dfCities["东中西"]=="西部","常住人口"]


dfCarbon=pd.read_csv(r"C:\Users\DELL\Desktop\carbon.csv")
xs=dfCarbon[["二氧化碳排放量","生产总值","人口数","森林覆盖率"]]
xz=st.zscore(xs)

lk=cl.hierarchy.linkage(xz,metric="euclidean",method="complete")
plt.close("all")
fig=cl.hierarchy.dendrogram(lk)

dfCarbon["complete"]=cl.hierarchy.cut_tree(lk,3)
lk=cl.hierarchy.linkage(xz,metric="euclidean",method="complete")
plt.close("all")
fig=cl.hierarchy.dendrogram(lk)
plt.show()

k=3
km=cl.vq.kmeans(xz,k)
cenz=km[0]
#求中心的原值
ms=np.mean(xs,0)
ms=np.tile(ms,[k,1])
sds=np.tile(np.std(xs,0),[k,1])
cen=cenz*sds+ms

dfCarbon["kmeans"]=cl.vq.vq(xz,cenz)[0]
sses=[]
ks=range(1,11)
for k in ks:
    km=cl.vq.kmeans(xz, k)
    sses.append(km[1])
plt.plot(ks,sses)
plt.show()

from sklearn.decomposition import PCA
xs=dfCarbon[["二氧化碳排放量","生产总值","人口数","森林覆盖率"]].dropna()
xz=st.zscore(xs)
pca=PCA()
pca.fit(xz)
pca.components_

import seaborn as sns
dfAges=pd.read_csv(r"C:\Users\DELL\Desktop\ages.csv")
x=dfCities["常住人口"]
plt.close("all")
plt.hist(x,bins=30,histtype="step")
plt.title("Population histgram")
plt.xlabel("Population")
plt.ylabel("Count")

plt.close("all")
sns.histplot(dfCities,x="常住人口",hue="南北",element="step")
plt.show()

fig=sns.FacetGrid(dfCities, row="南北", col="细颗粒物浓度分类")
fig.map(sns.histplot,"常住人口",binwidth=100)

xm=-dfAges.iloc[0,1:]
xf=dfAges.iloc[1,1:]
y=dfAges.columns[1:]
plt.close("all")
plt.barh(y,xm,color="blue",label="男性")
plt.barh(y,xf,color="pink",label="女性")
plt.legend()

plt.close("all")
sns.boxplot(data=dfCities,x="南北", y="常住人口")
sns.pointplot(data=dfCities,x="南北",y="常住人口",estimator=np.mean,linestyles="None",errorbar=None,color="red")

df19=dfCities[["南北","细颗粒物19"]].assign(x=np.full(len(dfCities),"2019"))
df19.columns=["南北","浓度","年份"]
df20=dfCities[["南北","细颗粒物20"]].assign(x=np.full(len(dfCities),"2020"))
df20.columns=["南北","浓度","年份"]
dfall=pd.concat([df19,df20])
dfall.index=np.arange(0,len(dfall))
plt.close("all")
sns.barplot(data=dfall,x="南北",y="浓度",hue="年份")

df19=dfCities[["南北","细颗粒物19"]].assign(x=np.full(len(dfCities),"2019"))
df19.columns=["南北","浓度","年份"]
df20=dfCities[["南北","细颗粒物20"]].assign(x=np.full(len(dfCities),"2020"))
df20.columns=["南北","浓度","年份"]
dfall=pd.concat([df19,df20])
dfall.index=np.arange(0,len(dfall))
plt.close("all")
sns.lineplot(data=dfall,x="南北",y="浓度",hue="年份")

plt.close("all")
ax1=sns.barplot(data=dfall.loc[dfall["年份"]=="2019"],x="南北",y="浓度",hue="年份")
ax2=ax1.twinx()
sns.lineplot(data=dfall.loc[dfall["年份"]=="2020"],x="南北",y="浓度",ax=ax2,color="red")

df19=dfCities.groupby("东中西")["细颗粒物19"].mean()
df20=dfCities.groupby("东中西")["细颗粒物20"].mean()
dfall=pd.concat([df19,df20],axis=1)
plt.close("all")
dfall.plot(kind="area",stacked=True)

dfCarbon= pd.read_csv(r"C:\Users\DELL\Desktop\carbon.csv")
x=dfCarbon["生产总值"]
y=dfCarbon["二氧化碳排放量"]
x= sm.add_constant(x)
mdl=sm.OLS(y, x)
res=mdl.fit()
res.summary()


x=dfCarbon[["生产总值","人口数","森林覆盖率","是否受雪灾影响"]]
x=sm.add_constant(x)
mdl=sm.OLS(y,x)
res=mdl.fit()
print(res.summary())

dfJobBin=pd.read_csv(r"C:\Users\DELL\Desktop\cities.csv")

