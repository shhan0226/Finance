import yfinance as yf
import pandas as pd
import math
import warnings

# 경고 메시지 필터링
warnings.filterwarnings("ignore", message="Converting to PeriodArray/Index representation will drop timezone information.")

# 사용자 입력
start_date = input("시작 날짜를 입력하세요 (YYYY-MM-DD 형식): ")
base_amount = float(input("기준 금액을 입력하세요 (KRW): "))

# SPY ETF 데이터 가져오기
spy = yf.Ticker("SPY")
spy_data = spy.history(start=start_date, interval="1mo")
dividends = spy.dividends[start_date:]

# 월별 첫 거래일 데이터 추출
spy_data['Month'] = spy_data.index.to_period('M')
monthly_data = spy_data.groupby('Month').nth(0)

# 기준 금액을 달러로 환산
exchange_rate = 1300
base_investment_usd = base_amount / exchange_rate
max_investment_usd = 1.1 * base_investment_usd

# 초기화
total_shares = 0
cumulative_investment = 0

# 결과 저장을 위한 리스트
results = []

# 최초 구매 시 SPY 1개의 가격
initial_spy_price = monthly_data.iloc[0]['Close']
print(f"투자 시작 시 SPY 1개의 가격: ${initial_spy_price:,.2f}")

# 월별 투자 및 배당금 계산
for date, row in monthly_data.iterrows():
    # 주식 구매 전략
    if row['Close'] >= base_investment_usd:
        shares_bought = 1
    else:
        max_shares = math.floor(max_investment_usd / row['Close'])
        shares_bought = min(math.floor(base_investment_usd / row['Close']), max_shares)

    total_shares += shares_bought
    cumulative_investment += shares_bought * row['Close']

    # 배당금 재투자
    if date in dividends.index:
        dividend_income = total_shares * dividends[date]
        reinvested_shares = math.floor(dividend_income / row['Close'])
        total_shares += reinvested_shares

    # 포트폴리오 가치 계산
    portfolio_value_usd = total_shares * row['Close']

    # 결과 저장
    results.append((date.strftime('%Y-%m'), total_shares, round(portfolio_value_usd, 2), 
                    round(total_shares * dividends[date], 2) if date in dividends.index else None))

# 결과 DataFrame으로 변환
results_df = pd.DataFrame(results, columns=['Month', 'Total Shares', 'Portfolio Value (USD)', 'Dividend (USD)'])
results_df['Portfolio Value (USD)'] = results_df['Portfolio Value (USD)'].apply(lambda x: f"${x:,.2f}")
results_df['Dividend (USD)'] = results_df['Dividend (USD)'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else None)

# 결과 출력
print(results_df)

# 현재 SPY 1개의 가격
current_spy_price = monthly_data.iloc[-1]['Close']
print(f"현재 SPY ETF 1개의 가격: ${current_spy_price:,.2f}")

# 순수 저축 금액
accumulated_savings = base_amount * len(results_df)
print(f"순수 저축 금액: {accumulated_savings:>15,.2f}원")

# 투자 원금
cumulative_investment_krw = round(cumulative_investment * exchange_rate, 2)
print(f"주식 투자 원금: {cumulative_investment_krw:>15,.2f}원 ({cumulative_investment:>10,.2f} USD)")

# 배당 누적 금액
dividend_accumulated = results_df['Dividend (USD)'].str.replace('$', '').str.replace(',', '').astype(float).sum()
dividend_accumulated_krw = round(dividend_accumulated * exchange_rate, 2)
print(f"배당 누적 금액: {dividend_accumulated_krw:>15,.2f}원 ({dividend_accumulated:>10,.2f} USD)")

# 포트폴리오 최종 가치
final_portfolio_value_krw = round(portfolio_value_usd * exchange_rate, 2) + dividend_accumulated_krw
print(f"포폴 최종 가치: {final_portfolio_value_krw:>15,.2f}원 ({portfolio_value_usd:>10,.2f} USD + {dividend_accumulated:,.2f} USD)")

