import yfinance as yf
import pandas as pd
import math
import warnings

# 경고 메시지 필터링
warnings.filterwarnings("ignore", message="Converting to PeriodArray/Index representation will drop timezone information.")

# 사용자 입력
start_date = input("시작 날짜를 입력하세요 (YYYY-MM-DD 형식): ")
monthly_investment_krw = float(input("월 투자 금액을 입력하세요 (KRW): "))

# SPY ETF 데이터 가져오기
spy = yf.Ticker("SPY")
spy_data = spy.history(start=start_date, interval="1mo")

# 데이터 확인
if spy_data.empty:
    raise ValueError("입력한 시작 날짜에 데이터가 없습니다. 날짜를 다시 확인하세요.")

dividends = spy.dividends[start_date:]

# 월별 첫 거래일 데이터 추출
spy_data.index = pd.to_datetime(spy_data.index)  # DatetimeIndex로 변환
spy_data['Month'] = spy_data.index.to_period('M')
monthly_data = spy_data.groupby('Month').nth(0)

# 기준 금액을 달러로 환산
exchange_rate = 1300
monthly_investment_usd = monthly_investment_krw / exchange_rate

# 초기화
total_shares = 0
cumulative_investment = 0
carried_over_amount = 0  # 이월 금액 초기화

# 결과 저장을 위한 리스트
results = []

# 최초 구매 시 SPY 1개의 가격
initial_spy_price = monthly_data.iloc[0]['Close']
print(f"투자 시작 시 SPY 1개의 가격: ${initial_spy_price:,.2f}")

# 월별 투자 및 배당금 계산
for date, row in monthly_data.iterrows():
    # 이월 금액 포함 가용 자금 계산
    available_funds = monthly_investment_usd + carried_over_amount

    # 배당금 확인 및 가용 자금에 추가
    dividend_income = 0
    dividend_per_share = 0
    if date in dividends.index:
        # 현재 월에 배당금 지급이 있는지 확인
        dividend_per_share = dividends[date]
        # 보유한 총 주식 수에 주식당 배당금을 곱하여 총 배당금 수익 계산
        dividend_income = total_shares * dividend_per_share
        # 배당금을 가용 자금에 추가
        available_funds += dividend_income

    # 주식 구매 전략
    # 가용 자금으로 살 수 있는 최대 주식 수 계산
    shares_bought = math.floor(available_funds / row['Close'])
    # 총 주식 수에 새로 구매한 주식 수를 추가
    total_shares += shares_bought
    # 이번 달에 사용한 투자 금액 계산
    investment_this_month = shares_bought * row['Close']
    # 누적 투자 금액에 이번 달 투자 금액을 추가
    cumulative_investment += investment_this_month

    # 사용하고 남은 금액 이월
    carried_over_amount = available_funds - investment_this_month

    # 포트폴리오 가치 계산
    portfolio_value_usd = total_shares * row['Close']

    # 결과 저장
    results.append((date.strftime('%Y-%m'), row['Close'], shares_bought, total_shares, round(portfolio_value_usd, 2), 
                    round(dividend_per_share, 2) if dividend_income > 0 else None, 
                    round(dividend_income, 2) if dividend_income > 0 else None))

# 결과 DataFrame으로 변환
results_df = pd.DataFrame(results, columns=['Month', 'SPY Price (USD)', 'Shares Bought', 'Total Shares', 'Portfolio Value (USD)', 'Dividend per Share (USD)', 'Dividend (USD)'])
results_df['Portfolio Value (USD)'] = results_df['Portfolio Value (USD)'].apply(lambda x: f"${x:,.2f}")
results_df['Dividend (USD)'] = results_df['Dividend (USD)'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else None)
results_df['Dividend per Share (USD)'] = results_df['Dividend per Share (USD)'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else None)

# 결과 출력
print(results_df)

# 현재 SPY 1개의 가격
current_spy_price = monthly_data.iloc[-1]['Close']
print(f"현재 SPY ETF 1개의 가격: ${current_spy_price:,.2f}")

# 순수 저축 금액
accumulated_savings = monthly_investment_krw * len(results_df)
print(f"순수 저축 금액: {accumulated_savings:>15,.2f}원")

# 투자 원금
cumulative_investment_krw = round(cumulative_investment * exchange_rate, 2)
print(f"주식 투자 원금: {cumulative_investment_krw:>15,.2f}원 ({cumulative_investment:>10,.2f} USD)")

# 포트폴리오 최종 가치
final_portfolio_value_krw = round(portfolio_value_usd * exchange_rate, 2)
print(f"포폴 최종 가치: {final_portfolio_value_krw:>15,.2f}원 ({portfolio_value_usd:>10,.2f} USD)")

# 투자 원금 대비 포트폴리오 최종 가치의 수익률 계산
return_rate = ((final_portfolio_value_krw - cumulative_investment_krw) / cumulative_investment_krw) * 100
print(f"투자 원금 대비 수익률: {return_rate:.2f}%")
