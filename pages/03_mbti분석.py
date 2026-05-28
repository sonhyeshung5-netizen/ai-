# streamlit app code
app_code = """
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

try:
    df = load_data()
    mbti_types = df.columns[1:].tolist()

    st.title("🌍 국가별 MBTI 분포 분석기")
    st.markdown("데이터셋을 기반으로 선택한 국가의 MBTI 유형별 비율을 시각화합니다.")

    # 사이드바: 국가 선택
    selected_country = st.sidebar.selectbox(
        "국가를 선택하세요",
        options=df['Country'].unique(),
        index=list(df['Country'].unique()).index('South Korea') if 'South Korea' in df['Country'].values else 0
    )

    # 데이터 추출 및 정렬
    country_data = df[df['Country'] == selected_country].iloc[0, 1:]
    country_data = country_data.sort_values(ascending=False)
    
    # 그래프 데이터 준비
    labels = country_data.index.tolist()
    values = country_data.values.tolist()
    
    # 색상 설정 (1위는 빨간색, 나머지는 파란색 그라데이션)
    # 파란색 농도를 순위에 따라 조절 (rgba 사용)
    colors = []
    for i in range(len(values)):
        if i == 0:
            colors.append('rgba(255, 0, 0, 0.8)')  # 1등: 빨간색
        else:
            # 순위가 낮아질수록(i가 커질수록) 투명도를 낮춰 흐려지는 효과
            opacity = max(0.2, 0.8 - (i * 0.05))
            colors.append(f'rgba(0, 100, 255, {opacity})')

    # Plotly 막대 그래프 생성
    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=[f"{v*100:.1f}%" for v in values],
        textposition='auto',
    )])

    fig.update_layout(
        title=f"<b>{selected_country}</b> MBTI 성격 유형 분포",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (Ratio)",
        template="plotly_white",
        height=600,
        yaxis=dict(tickformat=".1%")
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_wide=True)

    # 데이터 요약 정보
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 데이터 요약")
        st.write(f"**가장 많은 유형:** {labels[0]} ({values[0]*100:.2f}%)")
        st.write(f"**가장 적은 유형:** {labels[-1]} ({values[-1]*100:.2f}%)")
    
    with col2:
        st.subheader("📋 전체 순위")
        rank_df = pd.DataFrame({'MBTI': labels, 'Ratio (%)': [v*100 for v in values]})
        st.dataframe(rank_df, hide_index=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("파일 이름이 'countriesMBTI_16types.csv'인지 확인해주세요.")
"""

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

# requirements.txt
requirements = """
streamlit
pandas
plotly
"""
with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements.strip())
