
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 오늘 날짜 계산
output_date = datetime.today()
output_date_str = output_date.strftime("%Y-%m-%d")

# 시작 날짜 계산 (오늘 날짜 365일 전)
start_date = output_date - timedelta(days=365)
start_date_str = start_date.strftime("%Y-%m-%d")


# 주식 데이터 가져오기
#삼성전자: 005930.KS
#SK하이닉스: 000660.KS
#엔씨소프트: 036570.KS

stock_symbol = "000660.KS"
stock_data = yf.download(stock_symbol, start=start_date_str)

# 주식 이름 확인
ticker = yf.Ticker(stock_symbol)
stock_name = ticker.info['shortName']

print(f"주식 이름: {stock_name}")



# 데이터 확인
if stock_data.empty:
    raise ValueError("입력한 날짜 범위에 데이터가 없습니다. 날짜를 다시 확인하세요.")

# 이동평균선 계산
stock_data['5D_MA'] = stock_data['Close'].rolling(window=5).mean()
stock_data['20D_MA'] = stock_data['Close'].rolling(window=20).mean()
stock_data['60D_MA'] = stock_data['Close'].rolling(window=60).mean()
stock_data['120D_MA'] = stock_data['Close'].rolling(window=120).mean()

# 현재 가격 정보 가져오기
current_price = stock_data['Close'].iloc[-1]

# 현재 날짜의 이동평균선 값 가져오기
latest_data = stock_data.iloc[-1]
five_day_ma = latest_data['5D_MA']
twenty_day_ma = latest_data['20D_MA']
sixty_day_ma = latest_data['60D_MA']
one_twenty_day_ma = latest_data['120D_MA']

print(f"오늘 날짜: {output_date_str}")
print(f"현재 {stock_name} 가격: ${current_price:.2f}")
print(f"====================================")
print(f"5일 이동평균: ${five_day_ma:.2f}")
print(f"20일 이동평균: ${twenty_day_ma:.2f}")
print(f"60일 이동평균: ${sixty_day_ma:.2f}")
print(f"120일 이동평균: ${one_twenty_day_ma:.2f}")

print(f"====================================")
# 매매 조건 확인
if (twenty_day_ma >= one_twenty_day_ma) and (sixty_day_ma >= one_twenty_day_ma):
    print(f"<우상향!!> 20일과 60일이, 120일보다 높음...")    
    if twenty_day_ma >= sixty_day_ma:
        action = "매수! (20일평균 > 60일평균)"
    if twenty_day_ma < sixty_day_ma:
        action = "매도! (20일평균 < 60일평균)"
else:
    print(f"<박스권 혹은 우하향!!> 20일 또는 60일이, 120일보다 낮음...")    
    if latest_data < twenty_day_ma:
        action = "매도! (종가가 20일평균선을 터치하면...)"
    elif twenty_day_ma >= one_twenty_day_ma:
        action = "매수! (20일평균선이 120일평균선을 돌파하면...)"

print(f"매매 조치: {action}")    





