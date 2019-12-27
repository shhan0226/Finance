#!/usr/bin/env python
# coding: utf-8

# In[1]:


#finance.naver.com/sise/sise_index_day.nhn?code=KPI200


# In[2]:


index_cd='KPI200'
page_n=1
naver_index='http://finance.naver.com/sise/sise_index_day.nhn?code='+index_cd+'&page='+str(page_n)


# In[3]:


from urllib.request import urlopen
source=urlopen(naver_index).read()
source


# In[4]:


#소스명.prettify() 태그별 정돈
import bs4
source = bs4.BeautifulSoup(source, 'lxml')

print(source.prettify())


# In[5]:


td = source.find_all('td')
len(td) #td 개수 


# In[6]:


# XPath 확인 
# /html/body/div/table[1]/tbody/tr[3]/td[1] , 0부터 숫자 카운팅 -1 필요

source.find_all('table')[0].find_all('tr')[2].find_all('td')[0]


# In[7]:


d = source.find_all('td', class_='date')[0].text
d


# In[8]:


#파이썬 날짜 라이브러리 사용
import datetime as dt


# In[9]:


#문자열.split(구분자)
yyyy = int(d.split('.')[0])
mm = int(d.split('.')[1])
dd = int(d.split('.')[2])
this_date = dt.date(yyyy, mm, dd)
this_date


# In[10]:


#날자 변경 함수 정의
def date_format(d):
    #문자열 변환 replace
    d = str(d).replace('-', '.')
    yyyy = int(d.split('.')[0])
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])
    
    this_date = dt.date(yyyy, mm, dd)
    return this_date


# In[11]:


# XPath종가를 받아오기
# /html/body/div/table[1]/tbody/tr[3]/td[2]
this_close = source.find_all('tr')[2].find_all('td')[1].text
this_close = this_close.replace(',', '') #쉼표(,) 제거
this_close = float(this_close)
this_close


# In[12]:


#<td class="number_1">178.98</td>
p = source.find_all('td', class_='number_1')[0].text
p


# In[13]:


dates = source.find_all('td', class_='date')
prices = source.find_all('td', class_='number_1')


# In[14]:


dates


# In[15]:


prices


# In[16]:


len(dates)


# In[17]:


len(prices)


# In[18]:


#한페이지 출력
#<td class = "number_1">
#체결가(종가), 등락률, 거래량, 거래대금


for n in range(len(dates)): #dates 개수만큼 반복
    this_date = dates[n].text #n번째 dates 값 추출
    this_date = date_format(this_date) #날짜 형식으로 변환
    
    this_close = prices[n*4].text
    #0, 4, 8, 등 4의배수 해당 종가 추출
    this_close = this_close.replace(',', '') #쉼표(,) 제거
    this_close = float(this_close) #숫자 형식 변환
    this_close
    print(this_date, this_close)


# In[19]:


#맨뒤 패이지 UPL
paging = source.find('td', class_='pgRR').find('a')['href']
paging


# In[20]:


#맨뒤 페이지 숫자 따오기
paging = paging.split('&')[1]
paging


# In[21]:


paging = paging.split('=')[1]
paging


# In[22]:


last_page = source.find('td', class_='pgRR').find('a')['href']
last_page = last_page.split('&')[1]
last_page = last_page.split('=')[1]
last_page = int(last_page)


# In[23]:


#일일 종가 추출 함수
def historical_index_naver(index_cd, start_date='', end_date='', page_n=1, last_page=0):
    print(page_n)
    
    if start_date: #start_date가 있으면
        start_date = date_format(start_date) # date 포맷 변환
    else: #없으면
        start_date = dt.date.today() #오늘 날짜를 지정
    
    if end_date:
        end_date = date_format(end_date)
    else:
        end_date =dt.date.today()
        
    
    naver_index='http://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)
    print (naver_index)
    source=urlopen(naver_index).read() # 지정한 페이지에서 코드 읽기
    source = bs4.BeautifulSoup(source, 'lxml') # 뷰티플수프로 태그별 코드 분류
    
    dates = source.find_all('td', class_='date') #<td class="data"> 태그에서 날짜 수집
    prices = source.find_all('td', class_='number_1') #<td class="number_1"> 태그에서 지수 수집
   
    for n in range(len(dates)): 
        
        if dates[n].text.split('.')[0].isdigit():
           
            #날짜 처리
            this_date = dates[n].text 
            this_date = date_format(this_date) 
            
            
            if this_date <= end_date and this_date >= start_date: #start_date와 end_date 사이 데이터 저장            
                #종가 처리
                this_close = prices[n*4].text  #prices 중 종가지수 0, 4, 8 번째 데이터 추출
                this_close = this_close.replace(',', '')       
                this_close = float(this_close)
                                
                #딕녀너리 저장
                print(this_date, this_close)
                historical_prices[this_date] = this_close
                
            elif this_date < start_date: #start_date 이전이면 함수 종료
                return historical_prices
                
            
    #페이지 내비게이션
    if last_page == 0 :
        last_page = source.find('td', class_='pgRR').find('a')['href']      
        #마지막 페이지 주소 추출    
        last_page = last_page.split('&')[1]
        last_page = last_page.split('=')[1]
        last_page = int(last_page) 

        
    #다음 페이지 호출
    if page_n < last_page:
        page_n = page_n + 1
        historical_index_naver(index_cd, start_date, end_date, page_n, last_page)               
    
    return historical_prices
        


# In[24]:


index_cd='KPI200'
historical_prices = dict()
historical_index_naver(index_cd, '2019-12-2', '2019-12-16')
historical_prices


# In[25]:


index_cd='KPI200'
historical_prices = historical_index_naver(index_cd, '2019-11-2', '2019-11-15')
historical_prices

