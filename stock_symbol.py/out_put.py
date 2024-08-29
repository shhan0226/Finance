import pandas as pd

# CSV 파일에서 종목 정보를 읽어와 symbol1.txt 파일에 저장하는 함수
def save_symbols_to_file(csv_filename, output_filename):
    try:
        # CSV 파일 읽기
        df = pd.read_csv(csv_filename, encoding='euc-kr')  # 파일 인코딩에 맞게 설정
        with open(output_filename, 'w', encoding='utf-8') as file:
            for index, row in df.iterrows():
                stock_name = row['한글 종목약명']
                stock_code = row['단축코드']
                # "종목명:단축코드.KS" 형식으로 저장 (KOSPI는 .KS, KOSDAQ는 .KQ로 구분)
                market_suffix = ".KS" if row['시장구분'] == "KOSPI" else ".KQ"
                line = f"{stock_name}:{stock_code}{market_suffix}\n"
                file.write(line)
        print(f"'{output_filename}' 파일에 심볼이 성공적으로 저장되었습니다.")
    except FileNotFoundError:
        print(f"파일 '{csv_filename}'을 찾을 수 없습니다.")
    except Exception as e:
        print(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

# CSV 파일에서 종목 정보를 읽어와 symbol1.txt에 저장
csv_filename = 'data_4848_20240823.csv'
output_filename = 'symbol1.txt'
save_symbols_to_file(csv_filename, output_filename)
