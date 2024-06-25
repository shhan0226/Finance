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

# 주식 데이터 가져오기
#삼성전자: 005930.KS
#SK하이닉스: 000660.KS
#엔씨소프트: 036570.KS

stock_symbol = "036570.KS"
stock_data = yf.download(stock_symbol, start=start_date_str)

# 주식 이름 확인
ticker = yf.Ticker(stock_symbol)
stock_name = ticker.info['shortName']

print(f"주식 이름: {stock_name}")



# 데이터 확인
if stock_data.empty:
    raise ValueError("입력한 날짜 범위에 데이터가 없습니다. 날짜를 다시 확인하세요.")

# 이동평균선 계산
aver120 = '120D_MA'
window120 = 120
aver60 = '60D_MA'
window60 = 60
aver20 = '20D_MA'
window20 = 20
aver5 = '5D_MA'
window5 = 5

stock_data[aver120] = stock_data['Close'].rolling(window=window120).mean()
stock_data[aver60] = stock_data['Close'].rolling(window=window60).mean()
stock_data[aver20] = stock_data['Close'].rolling(window=window20).mean()
stock_data[aver5] = stock_data['Close'].rolling(window=window5).mean()


# 출력 날짜부터의 데이터만 선택
stock_data_filtered = stock_data.loc[output_date_str:]

# 매매 조건에 따른 매수/매도 지점 찾기
buy_signals = []
sell_signals = []
position = None  # 현재 포지션: None, 'buy', 'sell'
initial_investment = 500
cash = initial_investment
shares = 0

# 매매 시점과 가격 저장
trades = []

for i in range(len(stock_data_filtered)):
    row = stock_data_filtered.iloc[i]

    if position is None or position == 'sell':
        if row[aver20] >= row[aver120]:
            buy_signals.append((row.name, row['Close']))
            position = 'buy'
            shares = cash / row['Close']
            cash = 0
            trades.append(('Buy', row.name, row['Close']))
    
    elif position == 'buy':
        if row[aver20] < row[aver60]:
            sell_signals.append((row.name, row['Close']))
            position = 'sell'
            cash = shares * row['Close']
            shares = 0
            trades.append(('Sell', row.name, row['Close']))


# 최종 수익률 계산
final_value = cash + (shares * stock_data_filtered.iloc[-1]['Close'])
profit_percentage = (final_value - initial_investment) / initial_investment * 100

# 개별 거래의 수익 및 손실 계산
trade_results = []
for i in range(1, len(trades), 2):
    buy_trade = trades[i - 1]
    sell_trade = trades[i]
    if buy_trade[0] == 'Buy' and sell_trade[0] == 'Sell':
        profit_loss = (sell_trade[2] - buy_trade[2]) * (initial_investment / buy_trade[2])
        trade_results.append({
            'Buy Date': buy_trade[1],
            'Buy Price': buy_trade[2],
            'Sell Date': sell_trade[1],
            'Sell Price': sell_trade[2],
            'Profit/Loss': profit_loss
        })

# 매매 지점 시각화
plt.figure(figsize=(14, 7))
plt.plot(stock_data_filtered['Close'], label='Close Price')
plt.plot(stock_data_filtered[aver120], label='120-Day MA', color='purple')
plt.plot(stock_data_filtered[aver60], label='60-Day MA', color='orange')
plt.plot(stock_data_filtered[aver20], label='20-Day MA', color='red')
plt.plot(stock_data_filtered[aver5], label='5-Day MA', color='blue')
plt.title(f'{stock_name} - Price and Moving Averages from {output_date_str}')
plt.xlabel('Date')
plt.ylabel('Price (KRW)')
plt.legend()

# 매수/매도 지점 표시
for signal in buy_signals:
    plt.plot(signal[0], signal[1], 'g^', markersize=10, label='Buy Signal')
for signal in sell_signals:
    plt.plot(signal[0], signal[1], 'rv', markersize=10, label='Sell Signal')

# 그래프를 파일로 저장
graph_filename = 'trading_signals.png'
plt.savefig(graph_filename)
print(f"매매 신호가 '{graph_filename}' 파일로 저장되었습니다.")

# 표 형식으로 출력 (출력 날짜 기준 데이터), Dividends, Stock Splits, Capital Gains 제외
columns_to_display = ['Open', 'High', 'Low', 'Close', 'Volume', '5D_MA', '20D_MA', '60D_MA', '120D_MA']
# print(stock_data_filtered[columns_to_display])

# CSV 파일로 저장 (Dividends, Stock Splits 제외)
csv_filename = 'trading_signals_filtered.csv'
stock_data_filtered[columns_to_display].to_csv(csv_filename)
print(f"매매 신호 데이터가 '{csv_filename}' 파일로 저장되었습니다.")

# 최종 수익률 출력
print(f"초기 투자금: ${initial_investment:.2f}")
print(f"최종 평가금: ${final_value:.2f}")
print(f"수익률: {profit_percentage:.2f}%")

# 개별 거래 결과 출력
trade_results_df = pd.DataFrame(trade_results)
# print("개별 거래 결과:")
# print(trade_results_df)

# CSV 파일로 저장
trade_results_filename = 'trade_results.csv'
trade_results_df.to_csv(trade_results_filename, index=False)
print(f"거래 결과가 '{trade_results_filename}' 파일로 저장되었습니다.")
