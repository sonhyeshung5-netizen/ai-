import pandas as pd
import streamlit as st

# 1. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    # 한글 깨짐 방지를 위해 cp949 또는 utf-8-sig 사용
    try:
        df = pd.read_csv("adadawdadwa.csv", encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv("adadawdadwa.csv", encoding="cp949")
    
    # 공백 제거 및 열 이름 표준화
    df.columns = [col.strip() for col in df.columns]
    
    # 필요한 열들이 존재하는지 확인하고 이름 맞추기
    # 데이터 예시: '鼻貲'(이름/음식종류 예상), '輿模'(주소), '夔蘸隴URL'(URL) 등
    # 원본 컬럼명이 깨져있을 수 있으므로 인덱스로 접근하거나 이름을 변경합니다.
    return df

try:
    df = load_data()
    
    # 스트림릿 UI 구성
    st.title(" 서울 맛집 가이드 프로그램")
    st.write("원하는 음식점이나 키워드를 선택하시면 상세 정보를 안내해 드립니다.")
    st.write("---")

    # 원본 데이터의 컬럼 매핑 (제공된 파일 기준 설정)
    # 3번째 컬럼: 이름/종류, 4번째: URL, 5번째: 주소, 9번째: 영업시간, 10번째: 교통정보
    name_col = df.columns[2]  # 상호명 또는 음식 종류
    url_col = df.columns[3]   # URL
    addr_col = df.columns[4]  # 주소
    time_col = df.columns[8]  # 영업시간
    trans_col = df.columns[9] # 교통 정보

    # 데이터 정제 (결측치 제거 및 문자열 변환)
    df[name_col] = df[name_col].fillna("알 수 없음").astype(str)

    # 2. 음식/음식점 선택 창
    food_list = sorted(df[name_col].unique())
    selected_food = st.selectbox("궁금한 음식점이나 키워드를 선택하세요:", food_list)

    # 3. 선택된 항목의 데이터 필터링
    # 가장 많이 나타난 데이터(가장 많이 방문했거나 추천된 곳)를 기준으로 소개
    selected_data = df[df[name_col] == selected_food]
    
    if not selected_data.empty:
        st.success(f"🔍 '{selected_food}' 선택 완료! 가장 알맞은 정보를 매칭했습니다.")
        
        # 첫 번째 행을 대표 정보로 가져옴
        row = selected_data.iloc[0]
        
        # 4. 음식점 정보 출력
        st.subheader(f"🏪 음식점/명소 이름: {row[name_col]}")
        
        # 상세 정보 레이아웃 구성
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"📌 **기본 주소:** {row[addr_col]}")
            if len(df.columns) > 5:
                st.markdown(f"📮 **상세 주소:** {row[df.columns[5]]}")
        
        with col2:
            st.markdown(f"⏰ **영업 시간:** {row[time_col] if pd.notna(row[time_col]) else '정보 없음'}")
            st.markdown(f"🚇 **교통 안내:** {row[trans_col] if pd.notna(row[trans_col]) else '정보 없음'}")
            
        st.write("---")
        
        # 웹사이트 링크 버튼
        if pd.notna(row[url_col]):
            st.link_button("🔗 공식 visitseoul 웹사이트 방문하기", row[url_col])
            
        # 동일한 카테고리/이름으로 데이터가 여러 개 있을 경우 빈도수 표현
        st.info(f"💡 이 항목은 데이터 내에서 총 **{len(selected_data)}번** 언급/등록되었습니다.")

except Exception as e:
    st.error(f"데이터를 읽어오는 중 오류가 발생했습니다. 파일명과 컬럼을 확인해주세요. 오류 내용: {e}")
