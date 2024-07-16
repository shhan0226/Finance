
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 오늘 날짜 계산
output_date = datetime.today()
output_date_str = output_date.strftime("%Y-%m-%d")

# 시작 날짜 계산 (오늘 날짜 365일 전)
start_date = output_date - timedelta(days=365)
start_date_str = start_date.strftime("%Y-%m-%d")

# SPY, SPDR S&P 500 ETF Trust
# NVDA, NVIDIA Corporation
# AAPL, Apple Inc.
# MSFT, Microsoft Corporation
# TSM, Taiwan Semiconductor Manufacturing Company Limited


# 주식 데이터 가져오기
stock = yf.Ticker("NVDA")
stock_data = stock.history(start=start_date_str, interval="1d")

# stock_data 기본 정보 가져오기
info = stock.info

# 이름 확인
print(info['longName'])


# 데이터 확인
if stock_data.empty:
    raise ValueError("입력한 날짜 범위에 데이터가 없습니다. 날짜를 다시 확인하세요.")

# 이동평균선 계산
stock_data['5D_MA'] = stock_data['Close'].rolling(window=5).mean()
stock_data['20D_MA'] = stock_data['Close'].rolling(window=20).mean()
stock_data['120D_MA'] = stock_data['Close'].rolling(window=120).mean()

# 현재 가격 정보 가져오기
current_price = stock.history(period="1d")['Close'].iloc[0]

# 현재 날짜의 이동평균선 값 가져오기
latest_data = stock_data.iloc[-1]
five_day_ma = latest_data['5D_MA']
twenty_day_ma = latest_data['20D_MA']
one_twenty_day_ma = latest_data['120D_MA']

print(f"오늘 날짜: {output_date_str}")
print(f"현재 {info['longName']} 가격: ${current_price:.2f}")
print(f"====================================")
print(f"5일 이동평균: ${five_day_ma:.2f}")
print(f"20일 이동평균: ${twenty_day_ma:.2f}")
print(f"120일 이동평균: ${one_twenty_day_ma:.2f}")

print(f"====================================")
# 매매 조건 확인
if twenty_day_ma >= one_twenty_day_ma:
    print(f"<우상향!!> 20일이 120일보다 높음...")  
    if five_day_ma >= twenty_day_ma:
        action = "매수! (5일>=20일)"
    else:
        action = "매도! (5일평균선이 20일평균선을 터치하면...)"
else:
    print(f"<박스권 혹은 우하향!!> 20일이 120일보다 낮음...")  
    action = "매도! (20일<120일)"

print(f"매매 조치: {action}")    





