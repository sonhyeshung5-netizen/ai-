
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
    # 파일 읽기 (UTF-8 인코딩)
    df = pd.read_csv("seoul.csv", encoding="utf-8")
    
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
    
    # 데이터 기본 정보 산출
    min_date = df['날짜'].min().date()
    max_date = df['날짜'].max().date()

    # 2. 사이드바 - 날짜 범위 선택 사이드바
    st.sidebar.header("📅 기간 필터 설정")
    
    # 유저가 조회할 시작일과 종료일 선택
    date_range = st.sidebar.date_input(
        "조회할 날짜 범위를 선택하세요",
        value=(max_date - pd.Timedelta(days=30), max_date), # 기본값: 최근 30일
        min_value=min_date,
        max_value=max_date
    )

    # 시작일과 종료일이 모두 선택되었을 때만 그래프 그리기
    if len(date_range) == 2:
        start_date, end_date = date_range
        
        # 선택한 날짜에 맞게 데이터 필터링
        filtered_df = df[(df['날짜'].dt.date >= start_date) & (df['날짜'].dt.date <= end_date)]
        
        if not filtered_df.empty:
            st.subheader(f"📊 {start_date} ~ {end_date} 기온 추이")
            
            # 3. 꺾은선 그래프 그리기 (Matplotlib 이용)
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # 최고기온 (빨강), 최저기온 (파랑) 선그래프 + 범례 표시
            ax.plot(filtered_df['날짜'], filtered_df['최고기온(℃)'], color='red', marker='o', linestyle='-', linewidth=2, label='최고기온(℃)')
            ax.plot(filtered_df['날짜'], filtered_df['최저기온(℃)'], color='blue', marker='o', linestyle='-', linewidth=2, label='최저기온(℃)')
            
            # 그래프 데코레이션
            ax.set_title("Top & Bottom Temperature Trend", fontsize=14, pad=15)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Temperature (℃)", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # 범례 표시 활성화
            ax.legend(loc='upper right', fontsize=11)
            
            # X축 날짜 포맷팅 (데이터 양에 따라 자동 조절되도록 설정)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate() # 날짜 글자 겹침 방지 회전
            
            # 스트림릿 화면에 그래프 출력
            st.pyplot(fig)
            
            # 상세 데이터 테이블 탑재
            with st.expander("📄 선택한 기간의 상세 데이터 보기"):
                st.dataframe(filtered_df[['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].set_index('날짜'))
                
        else:
            st.warning("선택하신 기간에는 기록된 날씨 데이터가 없습니다. 다른 기간을 선택해 주세요.")
            
except FileNotFoundError:
    st.error("📂 `seoul.csv` 파일을 찾을 수 없습니다. GitHub 저장소(Repository)에 앱 코드 파일(`app.py`)과 `seoul.csv` 파일을 같은 폴더 내에 함께 업로드해 주세요.")
