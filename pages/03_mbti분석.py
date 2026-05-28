import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Analysis", layout="wide")

@st.cache_data
def load_data():
    try:
        # 데이터 파일 읽기
        df = pd.read_csv('countriesMBTI_16types.csv')
        # 데이터 수치화 (Country 제외한 모든 열)
        cols = df.columns[1:]
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
        return df
    except Exception as e:
        st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None:
    st.title("🌍 전세계 MBTI 데이터 분석 대시보드")
    
    # 탭 메뉴 구성
    tab1, tab2 = st.tabs(["국가별 분석", "MBTI 유형별 국가 순위"])

    # --- TAB 1: 국가별 분석 (기존 기능) ---
    with tab1:
        st.header("📍 국가별 MBTI 분포")
        countries = df['Country'].unique().tolist()
        default_index = countries.index('South Korea') if 'South Korea' in countries else 0
        
        selected_country = st.selectbox("국가를 선택하세요", options=countries, index=default_index, key='country_select')

        country_series = df[df['Country'] == selected_country].iloc[0, 1:].sort_values(ascending=False)
        
        labels = country_series.index.tolist()
        values = country_series.values.tolist()
        
        colors = ['rgba(255, 0, 0, 0.9)' if i == 0 else f'rgba(0, 100, 255, {max(0.1, 0.8 - (i * 0.05))})' for i in range(len(values))]

        fig1 = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=colors, text=[f"{v*100:.1f}%" for v in values], textposition='outside')])
        fig1.update_layout(title=f"<b>{selected_country}</b>의 MBTI 분포", yaxis=dict(tickformat=".1%"), template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

    # --- TAB 2: MBTI 유형별 국가 순위 (요청하신 새로운 기능) ---
    with tab2:
        st.header("🏆 MBTI 유형별 TOP 10 국가")
        mbti_types = df.columns[1:].tolist()
        selected_mbti = st.selectbox("MBTI 유형을 선택하세요", options=mbti_types, key='mbti_select')

        # 선택한 MBTI 유형 기준 정렬 및 상위 10개 추출
        top10_df = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)
        
        top10_countries = top10_df['Country'].tolist()
        top10_values = top10_df[selected_mbti].tolist()
        
        # 색상 설정 (1위는 빨간색, 나머지는 파란색 그라데이션)
        top10_colors = ['rgba(255, 0, 0, 0.9)' if i == 0 else f'rgba(0, 100, 255, {max(0.2, 0.8 - (i * 0.07))})' for i in range(10)]

        fig2 = go.Figure(data=[go.Bar(
            x=top10_countries, 
            y=top10_values, 
            marker_color=top10_colors,
            text=[f"{v*100:.2f}%" for v in top10_values],
            textposition='outside'
        )])

        fig2.update_layout(
            title=f"<b>{selected_mbti}</b> 비율이 가장 높은 국가 TOP 10",
            xaxis_title="국가",
            yaxis_title="비율",
            yaxis=dict(tickformat=".1%"),
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # 순위표 출력
        st.dataframe(top10_df.assign(Rank=range(1,11)).set_index('Rank'), use_container_width=True)

else:
    st.error("파일을 불러올 수 없습니다.")
