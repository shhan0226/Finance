#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd #json 크롤링한 데이터를 담기위한 팬더스 호출
from urllib.request import urlopen
import json #해외지수는 json 형태로 표출됨

symbol = 'NII@NI225'
page = 1

url ='https://finance.naver.com/world/worldDayListJson.nhn?symbol='+symbol+'&fdtc=0&page='+str(page)
raw = urlopen(url)
data = json.load(raw)

data[0]


# In[2]:


data[0]['xymd'] #날짜


# In[3]:


data[0]['clos'] #주가


# In[4]:


d = dict()
for n in range(len(data)):
    date = pd.to_datetime(data[n]['xymd']).date()
    price =float(data[n]['clos'])
    d[date] = price
print(d)


# In[5]:


def read_json(d, symbol, page=1): #page=1은 디폴트 값이 페이지 1이라는 것임
    url ='https://finance.naver.com/world/worldDayListJson.nhn?symbol='+symbol+'&fdtc=0&page='+str(page)
    raw = urlopen(url)
    data = json.load(raw)
    
    for n in range(len(data)):
        date = pd.to_datetime(data[n]['xymd']).date()
        price =float(data[n]['clos'])
        d[date] = price
        
    if len(data) == 10: #페이지가 10개 이면 다음으로, 10개 미만이면 다음 페이지로 넘어가지 안음
        page += 1
        read_json(d, symbol, page)
        
    return(d)   


# In[ ]:


historical_index = pd.Series() #함수를 실행해 결과를 담을 Series를 만듦
historical_index = read_json(historical_index, symbol, page)
historical_index.head(3)

