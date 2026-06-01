import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="성북구 연령별 인구 현황", layout="wide")

@st.cache_data
def load_data():
    # 파일 인코딩 오류 방지를 위해 여러 인코딩 시도
    encodings = ['utf-8', 'cp949', 'euc-kr']
    df = None
    
    for enc in encodings:
        try:
            df = pd.read_csv('population.csv', encoding=enc)
            # 성공적으로 읽으면 루프 종료
            break
        except (UnicodeDecodeError, LookupError):
            continue
            
    if df is None:
        st.error("파일의 인코딩을 지원하지 않습니다. UTF-8 또는 CP949 형식인지 확인해주세요.")
        return None, None
    
    # 분석에 필요한 연령대 컬럼 정의
    age_columns = [
        '0~9세', '10~19세', '20~29세', '30~39세', '40~49세', 
        '50~59세', '60~69세', '70~79세', '80~89세', '90~99세', '100세 이상'
    ]
    
    # 숫자 데이터 전처리 (쉼표 제거 및 정수형 변환)
    for col in age_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').astype(int)
        
    return df, age_columns

try:
    df, age_columns = load_data()

    if df is not None:
        st.title('📊 성북구 행정동별 연령대 인구 분포')
        
        # 사이드바: 행정동 선택
        selected_region = st.sidebar.selectbox(
            '행정구역(동)을 선택하세요',
            df['행정구역'].unique()
        )

        # 선택된 데이터 추출
        region_df = df[df['행정구역'] == selected_region].iloc[0]
        plot_data = pd.DataFrame({
            '연령대': age_columns,
            '인구수': [region_df[col] for col in age_columns]
        })

        # 2. 꺾은선 그래프 시각화
        fig = px.line(
            plot_data, 
            x='연령대', 
            y='인구수', 
            title=f'<b>[{selected_region}]</b> 연령별 인구 추이',
            markers=True
        )

        # 3. 디자인 설정 (바탕 흰색, 선 파란색)
        fig.update_traces(line_color='#007BFF', line_width=3, marker=dict(size=8))
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgrey'),
            yaxis=dict(showgrid=True, gridcolor='lightgrey')
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(plot_data.set_index('연령대').T)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
