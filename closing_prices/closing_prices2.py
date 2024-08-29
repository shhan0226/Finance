import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# 미리 정의된 종목명과 심볼 리스트
stock_name_to_symbol = {
    "삼성전자": "005930.KS",
    "현대자동차": "005380.KS",
    "카카오": "035720.KS",
    "네이버": "035420.KS"
}

# 기준 날짜 입력 받기
input_date = input("기준 날짜를 입력하세요 (예: 2024-08-05): ")

try:
    # 날짜 형식 확인 및 변환
    target_date = datetime.strptime(input_date, "%Y-%m-%d")
    target_date_str = target_date.strftime("%Y-%m-%d")

    start_date = target_date - timedelta(days=3*365)
    start_date_str = start_date.strftime("%Y-%m-%d")

except ValueError:
    raise ValueError("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력하세요.")

# 각 종목에 대해 가격 정보 출력
for stock_name, stock_symbol in stock_name_to_symbol.items():
    # 데이터 다운로드
    data = yf.download(stock_symbol, start=start_date_str, end=target_date_str)

    # 데이터가 비어있는지 확인
    if data.empty:
        print(f"{stock_name} ({stock_symbol})의 데이터가 없습니다.")
        continue

    # 기준일의 종가 또는 가장 가까운 날짜의 종가 찾기
    if target_date_str in data.index.strftime("%Y-%m-%d"):
        closing_price = data.loc[target_date_str]['Close']
        closest_date_str = target_date_str
    else:
        # 가장 가까운 날짜 찾기
        data.index = pd.to_datetime(data.index)
        closest_index = data.index.get_indexer([target_date], method='nearest')[0]
        closest_date_str = data.index[closest_index].strftime("%Y-%m-%d")
        closing_price = data.iloc[closest_index]['Close']

    # 지난 3년 내 최고점 찾기
    all_time_high = data['Close'].max()

    # 출력 시 천 단위 쉼표 추가
    formatted_closing_price = f"{closing_price:,.0f}"
    formatted_high = f"{all_time_high:,.0f}"

    # 결과 출력
    print(f"{closest_date_str} 기준 {stock_name} 종가: {formatted_closing_price}원")
    print(f"지난 3년 내 {stock_name} 전고점: {formatted_high}원")
    print("=" * 50)  # 각 종목 간 구분선
