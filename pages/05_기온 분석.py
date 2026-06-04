@st.cache_data
def load_data():
    # 에러 방지를 위해 다양한 한글 인코딩 방식을 순서대로 시도합니다.
    encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
    df = None
    
    for enc in encodings:
        try:
            df = pd.read_csv("seoul.csv", encoding=enc)
            break  # 읽기 성공 시 반복문 탈출
        except (UnicodeDecodeError, LookupError):
            continue  # 실패 시 다음 인코딩 시도
            
    if df is None:
        # 모든 인코딩 시도가 실패한 경우 예외 처리
        raise ValueError("seoul.csv 파일의 한글 인코딩을 인식할 수 없습니다. 파일 형식을 확인해 주세요.")
    
    # 컬럼명 공백 제거 및 날짜 데이터 앞의 \t 문자 제거
    df.columns = df.columns.str.strip()
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    
    # 날짜 데이터 타입 변경 및 결측치 제거
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜'])
    
    # 기온 데이터 숫자형 변환 및 결측치 제거
    df['최고기온(℃)'] = pd.to_numeric(df['최고기온(℃)'], errors='coerce')
    df['최저기온(℃)'] = pd.to_numeric(df['최저기온(℃)'], errors='coerce')
    df = df.dropna(subset=['최고기온(℃)', '최저기온(℃)'])
    
    # 날짜 순으로 정렬
    df = df.sort_values('날짜').reset_index(drop=True)
    return df
    
