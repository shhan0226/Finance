import yfinance as yf
from datetime import datetime, timedelta

# 날짜 입력 받기
input_date = input("기준 날짜를 입력하세요 (예: 2024-08-05): ")

# 날짜 형식 확인 및 변환
try:
    target_date = datetime.strptime(input_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    start_date = datetime.strptime(input_date, "%Y-%m-%d") - timedelta(days=3*365)
    start_date_str = start_date.strftime("%Y-%m-%d")
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

# 전고점 정보를 저장할 딕셔너리
all_time_highs = {}

# 각 심볼에 대해 전고점 가져오기
for name, symbol in symbols.items():
    # 데이터 다운로드
    data = yf.download(symbol, start=start_date_str, end=target_date)
    
    if not data.empty:
        # 전고점 계산
        all_time_high = data['Close'].max()
        all_time_highs[name] = all_time_high
    else:
        all_time_highs[name] = "데이터 없음"

# 전고점 출력
for name, high in all_time_highs.items():
    if isinstance(high, (int, float)):
        formatted_high = f"{high:,.0f}"
        print(f"{name}의 종가기준 전고점 (지난 3년): {formatted_high}원")
    else:
        print(f"{name}의 전고점: {high}")
