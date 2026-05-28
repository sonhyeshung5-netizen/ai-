import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Dashboard", layout="wide")

@st.cache_data
def load_data():
    # 데이터 파일 읽기
    try:
        df = pd.read_csv('countriesMBTI_16types.csv')
        return df
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일이 같은 경로에 있는지 확인해주세요.")
        return None

df = load_data()

if df is not None:
    st.title("🌍 국가별 MBTI 분포 분석기")
    st.markdown("선택한 국가의 MBTI 유형별 비율을 시각화합니다.")

    # 사이드바: 국가 선택 (기본값: South Korea)
    countries = df['Country'].unique().tolist()
    default_idx = countries.index('South Korea') if 'South Korea' in countries else 0
    
    selected_country = st.sidebar.selectbox(
        "국가를 선택하세요",
        options=countries,
        index=default_idx
    )

    # 데이터 추출 및 정렬 (비율이 높은 순서대로)
    country_data = df[df['Country'] == selected_country].iloc[0, 1:]
    country_data = country_data.astype(float).sort_values(ascending=False)
    
    labels = country_data.index.tolist()
    values = country_data.values.tolist()
    
    # 색상 설정 (1등은 빨간색, 나머지는 파란색 그라데이션)
    colors = []
    for i in range(len(values)):
        if i == 0:
            colors.append('rgba(255, 0, 0, 0.9)')  # 1등: 빨간색
        else:
            # 순위가 낮아질수록 투명도를 낮춰 흐려지는 효과 (0.8 -> 0.1)
            opacity = max(0.1, 0.8 - (i * 0.05))
            colors.append(f'rgba(0, 100, 255, {opacity})')

    # Plotly 막대 그래프 생성
    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=[f"{v*100:.1f}%" for v in values],
        textposition='outside',
    )])

    fig.update_layout(
        title=f"<b>{selected_country}</b>의 MBTI 유형 분포 (높은 순)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis=dict(tickformat=".1%"),
        template="plotly_white",
        height=600
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_wide=True)

    # 전체 순위 표 출력
    with st.expander("데이터 표로 보기"):
        rank_df = pd.DataFrame({
            '순위': range(1, 17),
            'MBTI 유형': labels,
            '비율 (%)': [f"{v*100:.2f}%" for v in values]
        })
        st.table(rank_df)
