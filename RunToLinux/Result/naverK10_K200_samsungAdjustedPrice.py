#/usr/bin/python
# -*- coding:utf-8 -*-
# 작성자 : 한석현


import bs4
from urllib.request import urlopen

import re
import datetime as dt
import pandas as pd


import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


k10_component = [ '005930', '000660', '068270', '207940', '005380', \
                  '005490', '051910', '028260', '035420', '012330']

def historical_index_naver(index_cd, start_date='', end_date='', page_n=1, last_page=0):

    index_cd = index_cd
    page_n = page_n

    if start_date:
        start_date = date_format(start_date)
    else:
        start_date = dt.date.today()

    if not end_date:
        end_date = dt.date.today()
    else:
        end_date = date_format(end_date)


    naver_index='https://finance.naver.com/sise/sise_index_day.nhn?code='+index_cd+'&page='+str(page_n)
    source = urlopen(naver_index).read()
    source = bs4.BeautifulSoup(source, 'lxml')

    dates = source.find_all('td', class_='date')
    prices = source.find_all('td', class_='number_1')

    for n in range(len(dates)):
        if dates[n].text.split('.')[0].isdigit():
            this_date = dates[n].text
            this_date = date_format(this_date)

            if this_date <= end_date and this_date >= start_date:
                this_close = prices[n*4].text
                this_close = this_close.replace(',', '')
                this_close = float(this_close)

                historical_prices[this_date]=this_close

            elif this_date < start_date:
                return historical_prices

    if last_page == 0:
        last_page = source.find('td', class_='pgRR').find('a')['href']
        last_page = last_page.split('&')[1]
        last_page = last_page.split('=')[1]
        last_page = int(last_page)

    if page_n < last_page:
        page_n = page_n + 1
        historical_index_naver(index_cd, start_date, end_date, page_n, last_page)

    return historical_prices



def call_component():
    url = 'https://finance.naver.com/sise/sise_market_sum.nhn'




def stock_info(stock_cd):
    url_float = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd='+stock_cd

#    print(url_float)

    source = urlopen(url_float).read()
    soup = bs4.BeautifulSoup(source, 'lxml')
#    print(soup)

#copy>Xpath : //*[@id="cTB11"]/tbody/tr[7]/td 
    tmp = soup.find(id='cTB11').find_all('tr')[6].td.text
#    print(tmp)

    tmp = tmp.replace('\r', '')
    tmp = tmp.replace('\n', '')
    tmp = tmp.replace('\t', '')
#    print(tmp)

    tmp = re.split('/', tmp)
#    print(tmp[0])

    #상장주식
    outstanding = tmp[0].replace(',', '')
    outstanding = outstanding.replace('주', '')
    outstanding = outstanding.replace(' ', '')
#    print(outstanding)

    #유동비율
    floating = tmp[1].replace(' ', '')
    floating = floating.replace('%', '')
#    print(floating)

    outstanding = int(outstanding)
#    print(outstanding)
    floating = float(floating)
#    print(floating)

#//*[@id="pArea"]/div[1]/div/table/tbody/tr[1]/td/dl/dt[1]/span
    name = soup.find(id='pArea').find('div').find('div').find('tr').find('td').find('span').text
    k10_outstanding[stock_cd] = outstanding
    k10_floating[stock_cd] = floating
    k10_name[stock_cd] = name

def date_format(d):
    d = str(d).replace('-', '.')
    yyyy = int(d.split('.')[0])
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])
    this_date = dt.date(yyyy, mm, dd)
    return this_date


def historical_stock_naver(stock_cd, start_date='', end_date='', page_n=1, last_page=0):

    if start_date:
        start_date = date_format(start_date)
    else:
        start_date = dt.date.today()

    if end_date:
        end_date = date_format(end_date)
    else:
        end_date = dt.date.today()

               

    naver_stock = 'https://finance.naver.com/item/sise_day.nhn?code='+stock_cd + '&page=' + str(page_n)

    source = urlopen(naver_stock).read()
    source = bs4.BeautifulSoup(source, 'lxml')
#    print(soup)
# /html/body/table[1]/tbody/tr[3]/td[1]/span

    dates = source.find_all('span', class_='tah p10 gray03')
    prices = source.find_all('td', class_='num')

    for n in range(len(dates)):

        if len(dates) > 0:
            this_date = dates[n].text
            this_date = date_format(this_date)

            if this_date <= end_date and this_date >= start_date:

                this_close = prices[n*6].text
                this_close = this_close.replace(',','')
                this_close = float(this_close)

                historical_prices[this_date]=this_close

            elif this_date < start_date:
                return historical_prices
        
        if last_page == 0:
            last_page = source.find_all('table')[1].find('td', class_='pgRR').find('a')['href']
            last_page = last_page.split('&')[1]
            last_page = last_page.split('=')[1]
            last_page = float(last_page)

    if page_n < last_page:
        page_n = page_n + 1
        historical_stock_naver(stock_cd, start_date, end_date, page_n, last_page)

    return historical_prices


            
def Show(K10, K200):
    plt.figure(figsize=(10, 5))
    plt.plot(K10['K10'], label='K10' )
    plt.plot(K200['K200'] / K200['K200'][0] * 100 , label='K200' )
    plt.legend(loc=0)
    plt.grid(True, color='0.7', linestyle=':', linewidth=1)
    plt.savefig('K10_K200_Index_'+start_date+'~'+end_date+'.png')
    plt.show()


if __name__ == '__main__':

    k10_outstanding = dict()
    k10_floating = dict()
    k10_name = dict()

    k10_historical_prices = dict()

    start_date = '2017-1-2'
    end_date = '2017-12-31'



########### KOSPI 10
    
    for stock_cd in k10_component:
        stock_info(stock_cd)
        
        historical_prices = dict()
        historical_prices = historical_stock_naver(stock_cd, start_date, end_date)
        k10_historical_prices[stock_cd] = historical_prices

    k10_historical_price = pd.DataFrame(k10_historical_prices)
    k10_historical_price.sort_index(axis=1, inplace=True)
    k10_historical_price = k10_historical_price.fillna(method='ffill')
    if k10_historical_price.isnull().values.any():
        k10_historical_price = k10_historical_price.fillna(method='bfill')

    #2018.5.4 samsung : Adjusted price        
    k10_historical_price['005930'] = k10_historical_price['005930'] / 50  
    k10_historical_price.to_csv('k10_Prices'+start_date+'~'+end_date+'.csv', mode='w')


    tmp = { 'Outstanding' : k10_outstanding,\
            'Floating' : k10_floating,\
            'Price' : k10_historical_price.loc[date_format(start_date)],\
            'Name' : k10_name}

    k10_info = pd.DataFrame(tmp)
    k10_info['f Market Cap'] =  k10_info['Outstanding'] * k10_info['Floating'] * k10_info['Price'] * 0.01
    k10_info['Market Cap'] =  k10_info['Outstanding'] * k10_info['Price'] * 0.01
    k10_info.to_csv('k10_info'+start_date+'~'+end_date+'.csv', mode='w')

    #market capitalization with floating ratio, 유동비율을 반영한 시가총액
    k10_historical_mc = k10_historical_price * k10_info['Outstanding'] * k10_info['Floating']*0.01

    #.sum()은 열의 합(세로방향), sum(axis=1)은 각 행의 합(가로방향)
    k10 = pd.DataFrame()
    k10['K10 Market Cap'] =  k10_historical_mc.sum(axis=1)
    ReferencePoint = len(k10['K10 Market Cap']) - 1
    k10['K10'] = k10['K10 Market Cap'] / k10['K10 Market Cap'][ReferencePoint] * 100
    k10.to_csv('k10_Index_'+start_date+'~'+end_date+'.csv', mode='w')

########### KOSPI 200

    historical_prices = dict()
    kospi200 = historical_index_naver('KPI200', start_date, end_date)

    k200 = pd.DataFrame({'K200': kospi200})
    k200.to_csv('k200_price_'+start_date+'~'+end_date+'.csv', mode='w')

##################### Show

#    print('k10 len:', len(k10['K10']), '/ k10[K10] >>',  k10['K10'])
#    print('===================================')
#    print('k200 len:', len(k200['K200']), '/ k200[K200] >>', k200['K200'])


    Show(k10, k200)
