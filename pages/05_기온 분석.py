import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="서울 기온 데이터 시각화", layout="centered")

st.title("🌡️ 서울 기온 데이터 분석 대시보드")
st.write("1907년부터의 서울 기온 데이터를 분석하고 지정한 기간의 기온 변화를 시각화합니다.")

# 1. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
    df = None
    
    for enc in encodings:
        try:
            df = pd.read_csv("seoul.csv", encoding=enc)
            break
        except (UnicodeDecodeError, LookupError):
            continue
            
    if df is None:
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

try:
    df = load_data()
    
    # 데이터 날짜 범위 계산
    min_date = df['날짜'].min().date()
    max_date = df['날짜'].max().date()

    # 2. 사이드바 - 날짜 범위 선택 설정
    st.sidebar.header("📅 기간 필터 설정")
    
    # 기본값으로 가장 최근 데이터 기준 30일 설정
    default_start = max_date - pd.Timedelta(days=30)
    
    date_range = st.sidebar.date_input(
        "조회할 날짜 범위를 선택하세요",
        value=(default_start, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # 시작일과 종료일이 모두 선택되었을 때 그래프 렌더링
    if len(date_range) == 2:
        start_date, end_date = date_range
        
        # 선택한 날짜 데이터 필터링
        filtered_df = df[(df['날짜'].dt.date >= start_date) & (df['날짜'].dt.date <= end_date)].copy()
        
        if not filtered_df.empty:
            st.subheader(f"📊 {start_date} ~ {end_date} 기온 추이")
            
            # 3. 차트용 데이터 가공
            # X축이 될 '날짜'를 인덱스로 지정하고 최고기온과 최저기온만 컬럼으로 추출합니다.
            chart_data = filtered_df.set_index('날짜')[['최고기온(℃)', '최저기온(℃)']]
            
            # 4. 스트림릿 내장 line_chart 사용
            # 에러가 났던 'colors' 대신 'color' 옵션을 사용하여 최고기온(#FF0000 = 빨강), 최저기온(#0000FF = 파랑)을 매핑합니다.
            st.line_chart(
                chart_data, 
                color=["#FF0000", "#0000FF"]
            )
            
            # 하단 상세 데이터 테이블 표기
            with st.expander("📄 선택한 기간의 상세 데이터 보기"):
                st.dataframe(filtered_df[['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].set_index('날짜'))
                
        else:
            st.warning("선택하신 기간에는 데이터가 존재하지 않습니다. 다른 날짜를 선택해 주세요.")
            
except FileNotFoundError:
    st.error("📂 `seoul.csv` 파일을 찾을 수 없습니다. 이 스크립트 파일과 동일한 디렉토리에 `seoul.csv` 파일이 정상적으로 존재해야 합니다.")
except Exception as e:
    st.error(f"⚠️ 앱 실행 중 오류가 발생했습니다: {e}")
