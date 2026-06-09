import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="서울시 관광 음식점 안내", layout="wide")

st.title(" 🗺️ 서울시 관광 음식점 데이터 가이드")
st.markdown("서울시의 주요 관광 음식점 정보를 간단하게 정리하여 보여주는 대시보드입니다.")

# 2. 데이터 불러오기 함수 (안정성 강화)
@st.cache_data
def load_data():
    # 인코딩 깨짐을 방지하기 위해 utf-8-sig 또는 cp949를 시도합니다.
    try:
        df = pd.read_csv("서울시 관광 음식.csv", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv("서울시 관광 음식.csv", encoding="cp949")
        
    # 열 개수가 부족할 경우를 대비하여 안전하게 매핑 진행
    # 원본 파일 구성에 맞춤 매핑
    essential_cols = {}
    col_mapping = {
        1: "언어",
        2: "상호명",
        4: "지번 주소",
        5: "도로명 주소",
        8: "영업시간",
        9: "찾아오는 길"
    }
    
    for idx, name in col_mapping.items():
        if len(df.columns) > idx:
            essential_cols[df.columns[idx]] = name
            
    # 정의된 열만 추출 및 이름 변경
    df_clean = df[list(essential_cols.keys())].rename(columns=essential_cols)
    
    # 텍스트 검색 및 필터링 시 에러를 방지하기 위해 결측치(NaN)를 빈 문자열로 대체
    df_clean = df_clean.fillna("")
    
    # 앞뒤 공백 제거
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].astype(str).str.strip()
            
    return df_clean

# 데이터 로드 실행
try:
    df = load_data()

    # 3. 사이드바 검색 및 필터 기능
    st.sidebar.header("🔍 검색 및 필터")
    
    # 언어 선택 (빈 값 제외하고 고유값 추출)
    unique_langs = [lang for lang in df["언어"].unique() if lang != ""]
    languages = ["전체"] + list(unique_langs)
    selected_lang = st.sidebar.selectbox("언어 선택", languages)
    
    # 상호명 검색어 입력
    search_query = st.sidebar.text_input("식당 이름 검색", "")

    # 4. 데이터 필터링 안전하게 적용
    filtered_df = df.copy()
    
    if selected_lang != "전체":
        filtered_df = filtered_df[filtered_df["언어"] == selected_lang]
        
    if search_query:
        # na=False 및 전체를 문자열 처리하여 검색 오류 원천 차단
        filtered_df = filtered_df[filtered_df["상호명"].str.contains(search_query, case=False, na=False)]

    # 5. 메인 화면 통계 및 대시보드 출력
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="총 등록된 식당 수", value=f"{len(df)}개")
    with col2:
        st.metric(label="필터링된 식당 수", value=f"{len(filtered_df)}개")

    st.write("---")
    
    # 데이터 표 출력
    st.subheader("📋 음식점 정보 목록")
    
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.info("검색 조건에 맞는 음식점이 없습니다.")

except Exception as e:
    st.error(f"데이터를 불러오거나 처리하는 중 오류가 발생했습니다.")
    st.code(str(e), language="python")
    st.info("💡 팁: '서울시 관광 음식.csv' 파일이 이 파이썬 스크립트(app.py)와 동일한 폴더에 저장되어 있는지 다시 한번 확인해 주세요.")
