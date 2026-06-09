
import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="서울시 관광 음식점 안내", layout="wide")

st.title(" 🗺️ 서울시 관광 음식점 데이터 가이드")
st.markdown("서울시의 주요 관광 음식점 정보를 간단하게 정리하여 보여주는 대시보드입니다.")

# 2. 데이터 불러오기 함수 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    # 인코딩 깨짐을 방지하기 위해 cp949 또는 utf-8-sig를 시도합니다.
    try:
        df = pd.read_csv("서울시 관광 음식.csv", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv("서울시 관광 음식.csv", encoding="cp949")
        
    # 필요한 핵심 열(Column)만 선택하고 이름을 직관적으로 변경
    # 원본 데이터의 열 순서에 맞춰 인덱스로 가져오는 것이 안전합니다.
    essential_cols = {
        df.columns[1]: "언어",
        df.columns[2]: "상호명",
        df.columns[4]: "지번 주소",
        df.columns[5]: "도로명 주소",
        df.columns[8]: "영업시간",
        df.columns[9]: "찾아오는 길"
    }
    
    df_clean = df[list(essential_cols.keys())].rename(columns=essential_cols)
    return df_clean

# 데이터 로드
try:
    df = load_data()

    # 3. 사이드바 필터 기능
    st.sidebar.header("🔍 검색 및 필터")
    
    # 언어별 필터 (한국어, 영어 등)
    languages = ["전체"] + list(df["언어"].dropna().unique())
    selected_lang = st.sidebar.selectbox("언어 선택", languages)
    
    # 상호명 검색어 입력
    search_query = st.sidebar.text_input("식당 이름 검색", "")

    # 4. 데이터 필터링 적용
    filtered_df = df.copy()
    
    if selected_lang != "전체":
        filtered_df = filtered_df[filtered_df["언어"] == selected_lang]
        
    if search_query:
        filtered_df = filtered_df[filtered_df["상호명"].str.contains(search_query, case=False, na=False)]

    # 5. 메인 화면 통계 및 테이블 출력
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="총 등록된 식당 수", value=f"{len(df)}개")
    with col2:
        st.metric(label="필터링된 식당 수", value=f"{len(filtered_df)}개")

    st.write("---")
    
    # 데이터 표 출력
    st.subheader("📋 음식점 정보 목록")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("파일 이름이 '서울시 관광 음식.csv'가 맞는지, 코드가 있는 폴더와 같은 위치에 있는지 확인해주세요.")
