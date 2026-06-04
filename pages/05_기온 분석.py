import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
        filtered_df = df[(df['날짜'].dt.date >= start_date) & (df['날짜'].dt.date <= end_date)]
        
        if not filtered_df.empty:
            st.subheader(f"📊 {start_date} ~ {end_date} 기온 추이")
            
            # 3. 꺾은선 그래프 플롯 생성 (Matplotlib)
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # 최고기온: 빨강(red), 최저기온: 파랑(blue) + 범례(label) 설정
            ax.plot(filtered_df['날짜'], filtered_df
