import yfinance as yf
from datetime import datetime, timedelta

# 날짜 입력 받기
input_date = input("종가를 확인할 날짜를 입력하세요 (예: 2024-08-05): ")

# 날짜 형식 확인 및 변환
try:
    target_date = datetime.strptime(input_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    start_date = datetime.strptime(input_date, "%Y-%m-%d") - timedelta(days=1)
    end_date = datetime.strptime(input_date, "%Y-%m-%d") + timedelta(days=1)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
except ValueError:
    raise ValueError("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력하세요.")

# 조회할 종목 및 지수 심볼
symbols = {
    "LG에너지솔루션": "373220.KS",
    "에코프로": "086520.KQ",
    "에코프로비엠": "247540.KQ",
    "삼아알미늄": "006110.KS",
    "SK하이닉스": "000660.KS",
    "삼성전자": "005930.KS",
    "현대차": "005380.KS",
    "기업은행": "024110.KS",
    "하나금융지주": "086790.KS",
    "우리금융지주": "316140.KS",
    "키움증권": "039490.KQ",
    "S-Oil": "010950.KS",
    "코스피": "^KS11",
    "코스닥": "^KQ11"
}

# 종가 정보를 저장할 딕셔너리
closing_prices = {}

# 각 심볼에 대해 종가 가져오기
for name, symbol in symbols.items():
    # 데이터 다운로드
    data = yf.download(symbol, start=start_date_str, end=end_date_str)
    
    if not data.empty:
        closest_date = data.index[-1].strftime("%Y-%m-%d")
        closing_prices[name] = (data['Close'].iloc[-1], closest_date)
    else:
        closing_prices[name] = ("데이터 없음", None)

# 종가 출력
for name, (price, date) in closing_prices.items():
    if date:
        formatted_price = f"{price:,.2f}"
        print(f"{name} ({date}): {formatted_price}원")
    else:
        print(f"{name} ({target_date}): {price}")
