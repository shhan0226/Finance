import yfinance as yf
from datetime import datetime, timedelta
import sys
import pandas as pd

# 조회할 종목 및 지수 심볼
stock_name_to_symbol = {
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




























# 파일에서 종목명과 심볼을 읽어오는 함수
def load_symbols_from_file(filename):
    stock_name_to_symbol = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    name, symbol = line.split(':')
                    stock_name_to_symbol[name] = symbol
    except FileNotFoundError:
        print(f"파일 '{filename}'을 찾을 수 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"파일을 처리하는 중 오류가 발생했습니다: {e}")
        sys.exit(1)
    return stock_name_to_symbol

# 심볼을 저장한 파일 읽기
stock_name_to_symbol = load_symbols_from_file('symbol.txt')

# 종목명과 기준 날짜 입력 받기
stock_name = input("종목명을 입력하세요 (예: 삼성전자): ")

# 종목명을 심볼로 변환
stock_symbol = stock_name_to_symbol.get(stock_name)

if not stock_symbol:
    print(f"{stock_name}에 대한 심볼을 찾을 수 없습니다. 정확한 종목명을 입력하세요.")
    sys.exit(1)  # 프로그램 종료

input_date = input("기준 날짜를 입력하세요 (예: 2024-08-05): ")

try:
    # 날짜 형식 확인 및 변환
    target_date = datetime.strptime(input_date, "%Y-%m-%d")
    target_date_str = target_date.strftime("%Y-%m-%d")

    start_date = target_date - timedelta(days=3*365)
    start_date_str = start_date.strftime("%Y-%m-%d")

except ValueError:
    raise ValueError("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력하세요.")

# 데이터 다운로드
data = yf.download(stock_symbol, start=start_date_str, end=target_date_str)

# 데이터가 비어있는지 확인
if data.empty:
    print(f"{stock_symbol}의 데이터가 없습니다. 종목 심볼 또는 날짜를 다시 확인하세요.")
    sys.exit(1)  # 프로그램 종료
else:
    print(data)

if target_date_str in data.index.strftime("%Y-%m-%d"):
    closing_price = data.loc[target_date_str]['Close']
    closest_date_str = target_date_str
    # print(f"{target_date_str} : {closing_price}")
else:    
    # 가장 가까운 날짜 찾기
    data.index = pd.to_datetime(data.index)
    target_date = pd.to_datetime(target_date_str)
    closest_index = data.index.get_indexer([target_date], method='nearest')[0]
    closest_date_str = data.index[closest_index].strftime("%Y-%m-%d")
    closing_price = data.iloc[closest_index]['Close']
    # print(f"{target_date_str}에 대한 데이터가 없습니다. 가장 가까운 날 {closest_date_str}의 종가는 {closing_price}입니다.")


# 최고점
all_time_high = data['Close'].max()

# 출력 시 천 단위 쉼표 추가
formatted_closing_price = f"{closing_price:,.0f}"
formatted_high = f"{all_time_high:,.0f}"

# 결과 출력
print(f"{closest_date_str} 기준 {stock_name} 종가: {formatted_closing_price}원")
print(f"지난 3년 내 {stock_name} 전고점: {formatted_high}원")
