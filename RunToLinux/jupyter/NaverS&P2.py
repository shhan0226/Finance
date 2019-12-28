#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd #json 크롤링한 데이터를 담기위한 팬더스 호출
from urllib.request import urlopen
import json #해외지수는 json 형태로 표출됨


# In[22]:


symbol = 'NII@NI255'
page = 1
d = dict()


# In[23]:


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
       
   return (d) 


# In[24]:


historical_index = pd.Series() #함수를 실행해 결과를 담을 Series를 만듦
historical_index = read_json(historical_index, symbol, page)
historical_index.head(3)


# In[25]:


indices = {
    'SPI@SPX' : 'S&P 500',
    'NAS@NDX' : 'Nasdaq 100',
    'NII@NI255' : 'Nikkei 225'
}


# In[26]:


historical_indices =dict()
for key, value in indices.items():
    print(key, value)
    s = dict()
    s = read_json(s, key, 1)
    historical_indices[value] = s
    
prices_df = pd.DataFrame(historical_indices)


# In[27]:


prices_df.tail(3) #NaN 값은 해당 증시 휴장일 때 추출됨


# In[28]:


#날짜를 받아 파이썬 날짜 형식으로 변경 함수
def date_format(d=''):
    if d != '':
        this_date = pd.to_datetime(d).date()
    else:
        this_date = pd.Timestamp.today().date()
    return (this_date)


# In[29]:


def index_global(d, symbol, start_date='', end_date='', page=1):
    
    end_date = date_format(end_date) #날짜 지정 없으면 오늘 날짜로 지정
    if start_date =='':
        start_date = end_date - pd.DateOffset(months=1)
    start_date = date_format(start_date)
    
    url ='https://finance.naver.com/world/worldDayListJson.nhn?symbol='+symbol+'&fdtc=0&page='+str(page)
    raw = urlopen(url)
    data = json.load(raw)
    
    if len(data) > 0 :
        
        for n in range(len(data)):
            date = pd.to_datetime(data[n]['xymd']).date()
            
            if date <= end_date and date >= start_date : #start_date와 end_date 사이에서 데이터 저장
                price = float(data[n]['clos']) #종가 처리
                d[date] = price #디셔너리 저장
                
            elif date < start_date :#start_date 이전이면 함수 종료
                return (d)
            
        if len(data) == 10 :
            page += 1
            index_global(d, symbol, start_date, end_date, page)
            
    return (d)


# In[30]:


historical_indices = dict()
start_date = '2019-01-01' #시작 날짜
end_date='2019-03-31' #끝 날짜

for key, value in indices.items():
    s = dict()
    s = index_global(s, key, start_date)
    historical_indices[value] = s
    
prices_df = pd.DataFrame(historical_indices)


# In[31]:


prices_df


# In[ ]:




