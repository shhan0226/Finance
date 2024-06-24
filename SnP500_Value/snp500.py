import yfinance as yf
import pandas as pd
import math
import warnings

# 경고 메시지 필터링
warnings.filterwarnings("ignore", message="Converting to PeriodArray/Index representation will drop timezone information.")


# 사용자로부터 시작 날짜와 기준 금액 입력 받기
start_date = input("시작 날짜를 입력하세요 (YYYY-MM-DD 형식): ")
base_amount = float(input("기준 금액을 입력하세요 (KRW): "))  # 기준 금액을 정수로 입력 받음

# SPY ETF 데이터 가져오기
spy = yf.Ticker("SPY")

# 시작 날짜부터 현재까지의 월별 데이터와 배당금 데이터 가져오기
spy_data = spy.history(start=start_date, interval="1mo")
dividends = spy.dividends[start_date:]

# 매월 5일 데이터 추출 (혹은 가장 가까운 날짜)
spy_data['Month'] = spy_data.index.to_period('M')
monthly_data = spy_data.groupby('Month').nth(0)  # 각 월의 첫번째 데이터 사용

# 기준 금액과 기준 금액 * 1.1을 달러로 환산 (환율 1,300원/달러 가정)
base_investment_usd = base_amount / 1300
max_investment_usd = 1.1 * base_investment_usd

# 초기화
total_shares = 0  # 누적 주식 수
cumulative_investment = 0  # 누적 투자액

# 월별 결과 출력
results = []

# 최초 구매 시 SPY 1개의 가격
initial_spy_price = monthly_data.iloc[0]['Close']
print(f"투자 시작 시 SPY 1개의 가격: ${initial_spy_price:,.2f}")

for date, row in monthly_data.iterrows():
    # 주식 가격에 따른 구매 전략 조정
    if row['Close'] >= base_investment_usd:
        # SPY 1주 가격이 기준 금액 이상일 경우, 1주만 구매
        shares_bought = 1
    else:
        # SPY 1주 가격이 기준 금액 미만일 경우, 10% 추가 투자
        max_shares = math.floor(max_investment_usd / row['Close'])
        shares_bought = min(math.floor(base_investment_usd / row['Close']), max_shares)

    total_shares += shares_bought
    cumulative_investment += shares_bought * row['Close']  # 실제 투자액 업데이트

    # 해당 월의 배당금 확인 및 재투자
    if date in dividends.index:
        # 배당금을 보유 주식 수에 곱하여 배당금을 계산
        dividend_income = total_shares * dividends[date]
        reinvested_shares = math.floor(dividend_income / row['Close'])  # 배당금으로 구매 가능한 정수 주식 수
        total_shares += reinvested_shares

    # 해당 월의 포트폴리오 가치 계산
    portfolio_value_usd = total_shares * row['Close']

    # 결과 저장
    results.append((date.strftime('%Y-%m'), total_shares, round(portfolio_value_usd, 2), round(total_shares * dividends[date], 2) if date in dividends.index else None))

# 결과를 DataFrame으로 변환하여 출력
results_df = pd.DataFrame(results, columns=['Month', 'Total Shares', 'Portfolio Value (USD)', 'Dividend (USD)'])
# 포트폴리오 가치와 배당금을 콤마를 추가하여 출력
results_df['Portfolio Value (USD)'] = results_df['Portfolio Value (USD)'].apply(lambda x: f"${x:,.2f}")
results_df['Dividend (USD)'] = results_df['Dividend (USD)'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else None)
print(results_df)

# 현재 SPY 1개의 가격 출력
current_spy_price = monthly_data.iloc[-1]['Close']
print(f"현재 SPY ETF 1개의 가격: ${current_spy_price:,.2f}")

# 매월 저축한 금액을 누적하여 계산
accumulated_savings = base_amount * len(results_df)
print(f"순수 저축 금액: {accumulated_savings:>15,.2f}원")

# 투자 원금 출력
cumulative_investment_krw = round(cumulative_investment * 1300, 2)
print(f"주식 투자 원금: {cumulative_investment_krw:>15,.2f}원 ({cumulative_investment:>10,.2f} )")

# 배당 누적 금액 계산
dividend_accumulated = results_df['Dividend (USD)'].str.replace('$', '').str.replace(',', '').astype(float).sum()
dividend_accumulated_krw = round(dividend_accumulated * 1300, 2)

print(f"배당 누적 금액: {dividend_accumulated_krw:>15,.2f}원 ({dividend_accumulated:>10,.2f} )")

# 포트폴리오의 최종 가치를 원화(KRW)로 출력
final_portfolio_value_krw = round(portfolio_value_usd * 1300, 2) + dividend_accumulated_krw
print(f"포폴 최종 가치: {final_portfolio_value_krw:>15,.2f}원 ({portfolio_value_usd:>10,.2f} + {dividend_accumulated:,.2f} )")

