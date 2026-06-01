import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="성북구 연령별 인구 현황", layout="wide")

@st.cache_data
def load_data():
    # 데이터 로드 (파일 경로 확인 필요)
    df = pd.read_csv('population.csv')
    
    # 분석에 필요한 연령대 컬럼 정의
    age_columns = [
        '0~9세', '10~19세', '20~29세', '30~39세', '40~49세', 
        '50~59세', '60~69세', '70~79세', '80~89세', '90~99세', '100세 이상'
    ]
    
    # 숫자 데이터 전처리 (쉼표 제거 및 정수형 변환)
    for col in age_columns:
        df[col] = df[col].astype(str).str.replace(',', '').astype(int)
        
    return df, age_columns

try:
    # 데이터 불러오기
    df, age_columns = load_data()

    # 상단 제목
    st.title('📊 성북구 행정동별 연령대 인구 분포')
    st.info('서울특별시 성북구의 2026년 4월 기준 데이터입니다.')

    # 사이드바: 행정동 선택 메뉴
    st.sidebar.header("조회 설정")
    selected_region = st.sidebar.selectbox(
        '조회할 행정구역을 선택하세요',
        df['행정구역'].unique()
    )

    # 선택된 동네의 데이터 필터링
    region_df = df[df['행정구역'] == selected_region].iloc[0]

    # 그래프용 데이터 재구성
    plot_data = pd.DataFrame({
        '연령대': age_columns,
        '인구수': [region_df[col] for col in age_columns]
    })

    # 2. 꺾은선 그래프 시각화 (Plotly)
    fig = px.line(
        plot_data, 
        x='연령대', 
        y='인구수', 
        title=f'<b>[{selected_region}]</b> 연령대별 인구 추이',
        markers=True,
        template='plotly_white' # 기본 바탕 흰색 설정
    )

    # 3. 그래프 색상 및 스타일 상세 설정
    fig.update_traces(
        line_color='#007BFF', # 파란색 그래프
        line_width=4, 
        marker=dict(size=10, color='#0056b3')
    )
    
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="연령대",
        yaxis_title="인구수(명)",
        font=dict(size=14)
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 하단 상세 데이터 표 출력
    with st.expander("원본 데이터 표 확인"):
        st.dataframe(plot_data.set_index('연령대').T)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.warning("동일한 폴더에 'population.csv' 파일이 있는지 확인해 주세요.")
