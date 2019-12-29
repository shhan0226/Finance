
import bs4
from urllib.request import urlopen

import re
import datetime as dt
import pandas as pd


naver_index='https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page=1'

source = urlopen(naver_index).read()
source = bs4.BeautifulSoup(source, 'lxml')
print(source)
#last_page = source.find('td', class_='pgRR').find('a')['href']
#print(last_page)

