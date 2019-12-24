#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd #json 크롤링한 데이터를 담기위한 팬더스 호출
from urllib.request import urlopen
import json #해외지수는 json 형태로 표출됨


# In[2]:


symbol = 'NII@NI255'
page = 1
d = dict()


# In[3]:


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


# In[4]:


historical_index = pd.Series() #함수를 실행해 결과를 담을 Series를 만듦
historical_index = read_json(historical_index, symbol, page)
historical_index.head(3)


# In[6]:


indices = {
    'SPI@SPX' : 'S&P 500',
    'NAS@NDX' : 'Nasdaq 100',
    'NII@NI255' : 'Nikkei 225'
}


# In[8]:


historical_indices =dict()
for key, value in indices.items():
    print(key, value)
    s = dict()
    s = read_json(s, key, 1)
    historical_indices[value] = s
    
prices_df = pd.DataFrame(historical_indices)


# In[9]:


prices_df.tail(3) #NaN 값은 해당 증시 휴장일 때 추출됨


# In[ ]:




