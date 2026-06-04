import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="서울 역대 날짜별 기온 분석", layout="centered")

st.title("📅 서울 역대 특정 날짜(월/일) 기온 분석")
st.write("특정 월과 일을 선택하면, 1907년부터 현재까지 해당 날짜의 최고기온과 최저기온 변화 추이를 보여줍니다.")

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
    
    # 분석을 위한 연, 월, 일 컬럼 추가
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    # 날짜 순으로 정렬
    df = df.sort_values('날짜').reset_index(drop=True)
    return df

try:
    df = load_data()

    # 2. 사이드바 - 월 및 일 선택 UI 생성
    st.sidebar.header("🔍 분석할 날짜 선택")
    
    # 월 선택 (1월 ~ 12월)
    selected_month = st.sidebar.selectbox("월을 선택하세요", range(1, 13), index=11) # 기본값 12월
    
    # 선택한 월에 맞는 일 수 계산 (2월 윤년 고려하여 안전하게 31일까지 제공 후 필터링)
    selected_day = st.sidebar.selectbox("일을 선택하세요", range(1, 32), index=24) # 기본값 25일

    # 3. 데이터 필터링 (매년 선택한 월과 일에 해당하는 데이터만 추출)
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].copy()
    
    if not filtered_df.empty:
        st.subheader(f"📊 역대 {selected_month}월 {selected_day}일 기온 추이 변화")
        st.write(f"1907년부터 최근까지 기록된 총 {len(filtered_df)}개의 데이터를 기반으로 합니다.")
        
        # 4. 차트용 데이터 가공 (X축을 '연도'로 설정)
        chart_data = filtered_df.set_index('연도')[['최고기온(℃)', '최저기온(℃)']]
        
        # 5. 스트림릿 내장 line_chart 시각화
        # 최고기온 = 빨강색(#FF0000), 최저기온 = 파랑색(#0000FF)
        # 마우스를 올리면 각 연도별 정확한 기온이 툴팁과 함께 범례로 표시됩니다.
        st.line_chart(
            chart_data,
            color=["#FF0000", "#0000FF"]
        )
        
        # 요약 통계 정보 제공
        col1, col2 = st.columns(2)
        with col1:
            max_row = filtered_df.loc[filtered_df['최고기온(℃)'].idxmax()]
            st.metric(
                label=f"역대 가장 더웠던 {selected_month}/{selected_day}", 
                value=f"{max_row['최고기온(℃)']} ℃", 
                delta=f"{int(max_row['연도'])}년"
            )
        with col2:
            min_row = filtered_df.loc[filtered_df['최저기온(℃)'].idxmin()]
            st.metric(
                label=f"역대 가장 추웠던 {selected_month}/{selected_day}", 
                value=f"{min_row['최저기온(℃)']} ℃", 
                delta=f"{int(min_row['연도'])}년",
                delta_color="inverse"
            )

        # 하단 상세 데이터 테이블 표기
        with st.expander("📄 데이터 전체 보기"):
            st.dataframe(
                filtered_df[['연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].set_index('연도')
            )
            
    else:
        st.error(f"⚠️ {selected_month}월 {selected_day}일은 존재하지 않는 날짜이거나 데이터가 없습니다. 다시 확인해 주세요.")
            
except FileNotFoundError:
    st.error("📂 `seoul.csv` 파일을 찾을 수 없습니다. 메인 루트 디렉토리에 파일이 저장되어 있는지 확인해 주세요.")
except Exception as e:
    st.error(f"⚠️ 앱 실행 중 오류가 발생했습니다: {e}")
