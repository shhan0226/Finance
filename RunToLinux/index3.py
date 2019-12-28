#/usr/bin/python
# -*- coding:utf-8 -*-
# 작성자 : 한석현


import bs4
from urllib.request import urlopen
from pprint import pprint

import re

k10_component = [ '005930', '000660', '068270', '207940', '005380', \
                  '005490', '051910', '028260', '035420', '012330']

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







if __name__ == '__main__':

    k10_outstanding = dict()
    k10_floating = dict()
    k10_name = dict()
    
    for stock_cd in k10_component:
        stock_info(stock_cd)

    print(k10_outstanding)
