#/usr/bin/python
# -*- coding:utf-8 -*-
# 작성자 : 한석현

from urllib.request import urlopen

import bs4
import datetime as dt

import pandas as pd
import json

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#%matplotlib inline

import numpy as np
from sklearn.lin

indices = {
    'SPI@SPX' : 'S&P 500',
    'NAS@NDX' : 'Nasdaq 100',
    'NII@NI225' : 'Nikkei 225'
}

def date_format(d):
    d = str(d).replace('-', '.')
    yyyy = int(d.split('.')[0])
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])
    this_date = dt.date(yyyy, mm, dd)
    return this_date

def historical_index_naver(index_cd, start_date='', end_date='', page_n=1, last_page=0):

    if start_date:   # start_date가 있으면
        start_date = date_format(start_date)   # date 포맷으로 변환
    else:    # 없으면
        start_date = dt.date.today()   # 오늘 날짜를 지정
    if end_date:
        end_date = date_format(end_date)
    else:
        end_date = dt.date.today()


    naver_index = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)

    source = urlopen(naver_index).read()   # 지정한 페이지에서 코드 읽기
    source = bs4.BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

    dates = source.find_all('td', class_='date')   # <td class="date">태그에서 날짜 수집
    prices = source.find_all('td', class_='number_1')   # <td class="number_1">태그에서 지수 수집

    for n in range(len(dates)):

        if dates[n].text.split('.')[0].isdigit():

            # 날짜 처리
            this_date = dates[n].text
            this_date= date_format(this_date)

            if this_date <= end_date and this_date >= start_date:
            # start_date와 end_date 사이에서 데이터 저장
                # 종가 처리
                this_close = prices[n*4].text   # prices 중 종가지수인 0,4,8,...번째 데이터 추출
                this_close = this_close.replace(',', '')
                this_close = float(this_close)

                # 딕셔너리에 저장
                historical_prices[this_date] = this_close

            elif this_date < start_date:
            # start_date 이전이면 함수 종료
                return historical_prices

    # 페이지 네비게이션
    if last_page == 0:
        last_page = source.find('td', class_='pgRR').find('a')['href']
        # 마지막페이지 주소 추출
        last_page = last_page.split('&')[1]   # & 뒤의 page=506 부분 추출
        last_page = last_page.split('=')[1]   # = 뒤의 페이지번호만 추출
        last_page = int(last_page)   # 숫자형 변수로 변환

    # 다음 페이지 호출
    if page_n < last_page:
        page_n = page_n + 1
        historical_index_naver(index_cd, start_date, end_date, page_n, last_page)

    return historical_prices


def date_today_format(d=''):
    if d != '':
        this_date = pd.to_datetime(d).date()
    else:
        this_date = pd.Timestamp.today().date()   # 오늘 날짜를 지정
    return (this_date)


def index_global(d, symbol, start_date='', end_date='', page=1):

    end_date = date_today_format(end_date)
    if start_date == '':
        start_date = end_date - pd.DateOffset(months=1)
    start_date = date_today_format(start_date)

    url = 'https://finance.naver.com/world/worldDayListJson.nhn?symbol='+symbol+'&fdtc=0&page='+str(page)
    raw = urlopen(url)
    data = json.load(raw)

    if len(data) > 0:

        for n in range(len(data)):
            date = pd.to_datetime(data[n]['xymd']).date()

            if date <= end_date and date >= start_date:
            # start_date와 end_date 사이에서 데이터 저장
                # 종가 처리
                price = float(data[n]['clos'])
                # 딕셔너리에 저장
                d[date] = price
            elif date < start_date:
            # start_date 이전이면 함수 종료
                return (d)

        if len(data) == 10:
            page += 1
            index_global(d, symbol, start_date, end_date, page)

    return (d)

def Show_(df):
    print("show... (Prices)")
    plt.close('all')
    plt.figure(figsize=(10, 5))
    S, = plt.plot(df['S&P500'],label='S&P500')
    K, = plt.plot(df['KOSPI200'], label='KOSPI200')
    plt.legend(handles=[S, K], loc=0)
    plt.grid(True, color='0.7', linestyle=':', linewidth=1)
    plt.savefig('Prices_'+start_d+'~'+end_d+'.png')
    plt.show()


def BCompare(A, B):
    if len(A)> len(B):
        return A
    else:
        return B

def SCompare(A, B):
    if len(A)< len(B):
        return A
    else:
        return B


def ShowIndex_(df):
    print("show... (Index)")
    plt.close('all')
    plt.figure(figsize=(10, 5))
    S, = plt.plot(df['S&P500']/df['S&P500'].loc[dt.date(2019, 1, 2)]*100,label='S&P500')
    K, = plt.plot(df['KOSPI200']/df['KOSPI200'].loc[dt.date(2019, 1, 2)]*100, label='KOSPI200')
    plt.legend(handles=[S, K], loc=0)
    plt.grid(True, color='0.7', linestyle=':', linewidth=1)
    plt.savefig('Index_'+start_d+'~'+end_d+'.png')
    plt.show()


def scatteredPlot_(df):
    print("show... (Index)")
    plt.close('all')
    plt.scatter(df_ratio_2019_now['S&P500'], df_ratio_2019_now['KOSPI200'], marker='.')
    plt.grid(True, color='0.7', linestyle=':', linewidth=1)
    plt.savefig('Scatter_'+start_d+'~'+end_d+'.png')
    plt.show()


if __name__ == '__main__':

    start_d = '2019-1-2'
    end_d = '2019-12-28'

    index_cd = 'KPI200'
    historical_prices = dict()
    kospi200 = historical_index_naver(index_cd, start_d, end_d)

    index_cd = 'SPI@SPX'
    historical_prices = dict()
    sp500 = index_global(historical_prices, index_cd, start_d, end_d)
    
    BigC = BCompare(sp500, kospi200)
    SmallC = SCompare(sp500, kospi200)


    for key in BigC.keys():
        if key not in SmallC.keys(): 
            SmallC[key]=None

    for key in SmallC.keys():
        if key not in BigC.keys(): 
            BigC[key]=None

    kospi200 = sorted(kospi200.items(), reverse=True)
    kospi200 =  dict(kospi200)
    sp500 = sorted(sp500.items(), reverse=True)
    sp500 =  dict(sp500) 

    tmp = {'S&P500':sp500, 'KOSPI200':kospi200}
    df = pd.DataFrame(tmp)
    df = df.fillna(method='ffill')
    if df.isnull().values.any():
        df = df.fillna(method='bfill')

    df.to_csv('Prices'+start_d+'~'+end_d+'.csv', mode='w')


#    Show_(df)
#    print(df.loc[dt.date(2019, 1, 2)])
#    ShowIndex_(df)
    scatteredPlot_(df)


