import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from datetime import datetime, timedelta

# 경고 메시지 필터링
warnings.filterwarnings("ignore", message="Converting to PeriodArray/Index representation will drop timezone information.")

# 사용자 입력
output_date_str = input("출력 날짜를 입력하세요 (YYYY-MM-DD 형식): ")
output_date = datetime.strptime(output_date_str, "%Y-%m-%d")

# 시작 날짜 계산 (출력 날짜 365일 전)
start_date = output_date - timedelta(days=365)
start_date_str = start_date.strftime("%Y-%m-%d")

# SPY ETF 데이터 가져오기
spy = yf.Ticker("SPY")
spy_data = spy.history(start=start_date_str, interval="1d")

# 데이터 확인
if spy_data.empty:
    raise ValueError("입력한 날짜 범위에 데이터가 없습니다. 날짜를 다시 확인하세요.")

# 이동평균선 계산
spy_data['5D_MA'] = spy_data['Close'].rolling(window=5).mean()
spy_data['20D_MA'] = spy_data['Close'].rolling(window=20).mean()
spy_data['60D_MA'] = spy_data['Close'].rolling(window=50).mean()
spy_data['120D_MA'] = spy_data['Close'].rolling(window=100).mean()

# 출력 날짜부터의 데이터만 선택
spy_data_filtered = spy_data.loc[output_date_str:]

# 이동평균선 시각화
plt.figure(figsize=(14, 7))
plt.plot(spy_data_filtered['Close'], label='Close Price')
plt.plot(spy_data_filtered['5D_MA'], label='5-Day MA')
plt.plot(spy_data_filtered['20D_MA'], label='20-Day MA')
plt.plot(spy_data_filtered['60D_MA'], label='60-Day MA')
plt.plot(spy_data_filtered['120D_MA'], label='120-Day MA')
plt.title(f'SPY ETF Price and Moving Averages from {output_date_str}')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.savefig('spy_moving_averages.png')  # 플롯을 파일로 저장
print("이동평균선 그래프가 'spy_moving_averages.png' 파일로 저장되었습니다.")

# 표 형식으로 출력 (출력 날짜 기준 데이터), Dividends, Stock Splits, Capital Gains 제외
columns_to_display = ['Open','High', 'Low','Close','Volume', '5D_MA', '20D_MA', '60D_MA', '120D_MA']
print(spy_data_filtered[columns_to_display])

# CSV 파일로 저장 (Dividends, Stock Splits 제외)
spy_data_filtered[columns_to_display].to_csv('spy_moving_averages_filtered.csv')
print("이동평균선 데이터가 'spy_moving_averages_filtered.csv' 파일로 저장되었습니다.")

# CSV 파일 읽기 및 표로 출력
csv_file_path = 'spy_moving_averages_filtered.csv'
df = pd.read_csv(csv_file_path, index_col=0)
print("CSV 파일 내용을 표로 출력합니다:")
print(df)
