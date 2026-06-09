import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="서울시 관광 음식점 안내", layout="wide")

st.title("🗺️ 서울시 관광 음식점 데이터 가이드")
st.markdown("서울시의 주요 관광 음식점 정보를 깔끔하게 정리하여 보여주는 대시보드입니다.")

# 2. 사이드바에서 데이터 파일 업로드 받기
st.sidebar.header("📁 데이터 파일 업로드")
uploaded_file = st.sidebar.file_uploader("상단의 '서울시 관광 음식.csv' 파일을 여기에 드래그해 주세요.", type=["csv"])

# 데이터 처리 함수

def process_data(file_source):
    # 인코딩 깨짐 방지를 위해 예외 처리 구성
    try:
        df = pd.read_csv(file_source, encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(file_source, encoding="cp949")
        
    # 원본 파일 구성에 맞춘 핵심 열 이름 매핑
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
            
    # 유효 열 추출 및 이름 수정
    df_clean = df[list(essential_cols.keys())].rename(columns=essential_cols)
    
    # 결측치(NaN) 빈 문자열로 안전하게 처리
    df_clean = df_clean.fillna("")
    
    # 문자열 공백 제거
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].astype(str).str.strip()
            
    return df_clean

# 3. 파일이 업로드되었을 때만 화면 구현
if uploaded_file is not None:
    try:
        df = process_data(uploaded_file)

        # 사이드바 필터 영역
        st.sidebar.write("---")
        st.sidebar.header("🔍 검색 및 필터")
        
        # 언어 필터 (빈 값 제외)
        unique_langs = [lang for lang in df["언어"].unique() if lang != ""]
        languages = ["전체"] + list(unique_langs)
        selected_lang = st.sidebar.selectbox("언어 선택", languages)
        
        # 상호명 검색어
        search_query = st.sidebar.text_input("식당 이름 검색", "")

        # 데이터 필터링 안전 적용
        filtered_df = df.copy()
        if selected_lang != "전체":
            filtered_df = filtered_df[filtered_df["언어"] == selected_lang]
            
        if search_query:
            filtered_df = filtered_df[filtered_df["상호명"].str.contains(search_query, case=False, na=False)]

        # 메인 화면 수치 요약
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="총 등록된 식당 수", value=f"{len(df)}개")
        with col2:
            st.metric(label="필터링된 식당 수", value=f"{len(filtered_df)}개")

        st.write("---")
        
        # 데이터프레임 시각화 테이블 출력
        st.subheader("📋 음식점 정보 목록")
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.info("검색 조건에 맞는 음식점이 존재하지 않습니다.")

    except Exception as e:
        st.error(f"데이터를 분석하는 과정에서 오류가 발생했습니다.")
        st.code(str(e), language="python")
else:
    # 파일을 아직 올리지 않았을 때 안내 메시지
    st.info("💡 왼쪽 사이드바의 **[Browse files]** 버튼을 눌러 **'서울시 관광 음식.csv'** 파일을 업로드해 주세요!")
