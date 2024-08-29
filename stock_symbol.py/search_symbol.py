import pandas as pd

# CSV 파일에서 종목 정보를 읽어오는 함수
def load_stock_data(filename):
    try:
        df = pd.read_csv(filename, encoding='euc-kr')  # 인코딩을 'euc-kr'로 변경
        return df
    except FileNotFoundError:
        print(f"파일 '{filename}'을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"파일을 처리하는 중 오류가 발생했습니다: {e}")
        return None

# 한글 종목명으로 단축코드를 찾는 함수
def get_stock_code_by_name(df, stock_name):
    try:
        result = df[df['한글 종목약명'] == stock_name]
        if not result.empty:
            stock_code = result.iloc[0]['단축코드']
            print(f"종목명: {stock_name}, 단축코드: {stock_code}")
            return stock_code
        else:
            print(f"'{stock_name}'에 대한 단축코드를 찾을 수 없습니다.")
            return None
    except KeyError:
        print("CSV 파일에 '한글 종목명' 또는 '단축코드' 컬럼이 없습니다.")
        return None

# CSV 파일 로드
filename = 'data_4848_20240823.csv'
df = load_stock_data(filename)

if df is not None:
    # 종목명 입력받기
    stock_name = input("종목명을 입력하세요: ")
    get_stock_code_by_name(df, stock_name)
