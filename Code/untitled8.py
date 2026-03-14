# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 16:39:56 2025

@author: DELL
"""
import requests
import json
import time
import random
from bs4 import BeautifulSoup
import re
from pyquery import PyQuery as pq
import warnings
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import random
warnings.filterwarnings('ignore')

def Eraser(text, word):
    try:
        text_new = re.findall(r'(.*){}(.*)'.format(str(word)),text)[0]
        text_new = text_new[0] + text_new[1]
    except:
        return text
    while text != text_new:
        text = text_new
        try:
           text_new = re.findall(r'(.*){}(.*)'.format(str(word)),text)[0]
           text_new = text_new[0] + text_new[1]
        except:
            break
    return text_new

def Isin(text , word):
    text_new = Eraser(text, word)
    if text_new == text:
        return False
    else: return True
 
def SinaCode(num):
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def base62_decode(string, alphabet=ALPHABET):
        """Decode a Base X encoded string into the number     
        Arguments:
        - `string`: The encoded string
        - `alphabet`: The alphabet to use for encoding
        """
        base = len(alphabet)
        strlen = len(string)
        num = 0
     
        idx = 0
        for char in string:
            power = (strlen - (idx + 1))
            num += alphabet.index(char) * (base ** power)
            idx += 1
     
        return num
    def base62_encode(num, alphabet=ALPHABET):
        """Encode a number in Base X
        `num`: The number to encode
        `alphabet`: The alphabet to use for encoding
        """
        if (num == 0):
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while num:
            rem = num % base
            num = num // base
            arr.append(alphabet[rem])
        arr.reverse()
        return ''.join(arr)

    def mid_to_url(midint):
        
        midint = str(midint)[::-1]
        size = len(midint) / 7 if len(midint) % 7 == 0 else len(midint) / 7 + 1
        result = []

        for i in range(int(size)):
            s = midint[i * 7: (i + 1) * 7][::-1]
            s = base62_encode(int(s))
            s_len = len(s)
            if i < size - 1 and len(s) < 4:
                s = '0' * (4 - s_len) + s
            result.append(s)
        result.reverse()
        return ''.join(result)[2:]
    
    return mid_to_url(num)

'''
Thanks to https://blog.luzy.top/posts/794074733/ offer a support.
'''
    
headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
'Cookie': 'SINAGLOBAL=7234031223700.781.1742178669676; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5IVOwOvmirgypi0VHc6Q.U5JpX5KMhUgL.FoMXehqX1hqcS0-2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSh5cShncSoMf; SCF=Asqm4FygdBsBTF7dZmQERrFZJbwE4aS6oaRKSisi5LHj2dmhXo6yw-ozS5szR6HrGmcRdBWX-9e_0UtLLSf6N7I.; SUB=_2A25FDyeVDeRhGeFK61QV-CjKzDmIHXVmZSVdrDV8PUNbmtANLRShkW9NQ4p_QAJbV0D7NzGIGMyqESQ1mRYVNMnH; ALF=1748165829; _s_tentry=-; Apache=8896123449324.492.1745653540096; ULV=1745653540177:7:1:1:8896123449324.492.1745653540096:1743314087187; WBPSESS=ZvT79JBQbnTB6N_-1iJAi0RaP9LjgkrtlaN5sdvJXLCp4sXo7wfcx7w3tfvmhkrlOS6h2fIA_nODfTleHqvYmZIoBLgqYc4AuuuqW6xLUkBpy1UOpKu4AkTllQzxgZbAH4dgm7-42NFeMUOEenN_8g=='
}
page = 2
people_comment = []
result_list_all = []
varNames = ['Content' , 'Offical or not' , 'Iine' , 'Trans'] 



for j in range(1,7):
    url = 'https://s.weibo.com/weibo?q=九亭外来&nodup=1&page={}'.format(j)
    get = requests.get(url = url , headers = headers)
    get.encoding=get.apparent_encoding
    if get.status_code == 200:
        soup=BeautifulSoup(get.content,"html.parser")
        content_all=soup.find("div",class_="main-full")
        contents=content_all.find_all("div",class_="card-wrap")
        for content in contents: 
            offical_text = content .find('div', class_ = 'avator')
            if Isin(str(offical_text) , '微博官方认证'):
                offical_or_not = 'Offical'
            else: offical_or_not = 'Not Offical'
            
            text_all = content.find('div', class_='content')
            texts  = content.find_all('p',class_ = 'txt')
            if len(re.findall(r'<a href=(.*?) target', str(texts[0]))) == 0:
               print(len(texts))
               text_real = re.findall(r'content\">\n *(.*?) *<[a/]', str(texts[0]))[0]
               print(text_real)
            else:
                print(len(texts))
                text_real = re.findall(r'</a>(.*?) *<', str(texts[0]))
                print(text_real)
                
            iine = content.find('a',title = '赞')
            iine_mid = re.findall(r'mid=(.*?)\"', str(iine))[0]
            url_iine = "https://m.weibo.cn/api/attitudes/show?id={}&page=1".format(iine_mid)
            requests_iine = requests.get(url = url_iine , headers = headers)
            requests_iine.encoding = requests_iine.apparent_encoding
            result_iine = BeautifulSoup(requests_iine.content , 'html.parser')
            iine_counts = re.findall(r"total_number\":(.*?),\"data\"", str(result_iine))
            if not len(iine_counts) == 0:
                iine_count = int(iine_counts[0])   #Int 
            else:
                iine_count = 0
            
            #url_body = re.findall(r'href=\"(.*?) suda',str(offical_text))[0]
            #url_head = 'https:' + url_body.split('?')[0] +"/"
            #url_feet = url_body.split('?')[1][:-1]
            #url_whole = url_head + str(SinaCode(content['mid'])) + "?" + url_feet
            #print(url_whole)    Another Choice
            url_whole = "https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={}&is_show_bulletin=2&is_mix=0&count=20&fetch_level=0&locale=zh-CN&flow=1".format(content['mid'])
            comment_request = requests.get(url = url_whole , headers = headers)
            comment_request.encoding = comment_request.apparent_encoding
            comment_request1 = BeautifulSoup(comment_request.content , 'html.parser')
            result = str(comment_request1).split('location')[:-1]
            comment_list = []
            for comment in result:       
                comment_every = re.findall(r"\"text\":\"(.*?)\",\"disable_reply", comment)[0]
                if not Isin(comment_every, 'img'):
                    comment_list.append(comment_every)
            for i in comment_list:
                people_comment.append(i)
                
            trans = len(comment_list)
            result_list_all.append([text_real , offical_or_not , iine_count , trans])    #need to transfer dtype
            '''
            comment_web = content.find('div' , class_ = 'card-act')
            print(comment_web)
            '''
    else:  pass
    j  = j+1
    time.sleep(random.uniform(1.0, 2.0)) 
print(result_list_all)

li = str(people_comment)

def cloud_analysis(text):
    text = re.sub(r'[a-zA-Z0-9_:+/\\@=\"\'{}]','',text)
    seg_list_all = jieba.cut(text)
    seg_list = [word for word in seg_list_all if word not in ["你","我","的","说","也","有","就","都","人","微博","是","来","可以"
                                                              ,"了","没","就算","现在","大","还","多","你们","它们","自己","怎么","好"
                                                              ,"这样","所以","看看","什么","斤","几个","他们","会","发","一个","禁言",
                                                              "被","太多要","对","有人","一下","一千多万","让","鱼","但凡","中","其实",
                                                              "谢谢","这里","两个","啊","私信","把","不","吧","不是","搞","反应","回复",
                                                              "然然儿","转发转发","转发","给","骂骂政府","看","按","去","下","吗","不会",
                                                              "不能","打通","看到","发布","骂骂","政府","希望","新闻","到位","统一","句式",
                                                              '上海',"共条","松江","活该","困难","九里","卢俊",'上海市','东京','佘山个','没有',
                                                              '辣椒酱','几天','人中','非常','一个月','以及','几片','比例','就是','大部分','任何',
                                                              '比如','以下','因为','所在','分布','所在','无法','控天','传说','好像','之一','能发'
                                                              ,'发出','怪不得','五分之一','那些','这么']]
    seg_list = [word for word in seg_list if len(word) != 1]
    word_list = " ".join(seg_list)
    return word_list

word_list = cloud_analysis(li)
wordcloud = WordCloud(font_path="msyh.ttc",width=800, height=400, background_color="white").generate(word_list)
fig = plt.figure(figsize=(10, 15))
fig.add_subplot(311)
plt.title('居民')
plt.rcParams['font.sans-serif']=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False 
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")  # 不显示坐标轴

text_offical = [unit for unit in result_list_all if unit[1] == 'Offical']
text_not_offical = [unit for unit in result_list_all if unit[1] == 'Not Offical']
offical_text = cloud_analysis(str([text[0] for text in text_offical]))
not_offical_text = cloud_analysis(str([text[0] for text in text_not_offical]))
print(text_offical)
wordcloud1 = WordCloud(font_path="msyh.ttc",width=800, height=400, background_color="white").generate(offical_text)
fig.add_subplot(312)
plt.title('官方')
plt.rcParams['font.sans-serif']=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False 
plt.imshow(wordcloud1, interpolation='bilinear')
plt.axis("off")  # 不显示坐标轴

wordcloud2 = WordCloud(font_path="msyh.ttc",width=800, height=400, background_color="white").generate(not_offical_text)
fig.add_subplot(313)
plt.title('民间')
plt.rcParams['font.sans-serif']=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False 
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")  # 不显示坐标轴


