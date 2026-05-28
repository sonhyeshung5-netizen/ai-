import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Dashboard", layout="wide")

@st.cache_data
def load_data():
    try:
        # 데이터 파일 읽기
        df = pd.read_csv('countriesMBTI_16types.csv')
        return df
    except Exception as e:
        st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None:
    st.title("🌍 국가별 MBTI 분포 분석기")
    
    # 사이드바: 국가 선택
    countries = df['Country'].unique().tolist()
    # 'South Korea'가 목록에 있으면 기본값으로 설정, 없으면 첫 번째 국가 선택
    default_index = countries.index('South Korea') if 'South Korea' in countries else 0
    
    selected_country = st.sidebar.selectbox(
        "분석할 국가를 선택하세요",
        options=countries,
        index=default_index
    )

    # 해당 국가 데이터 추출
    row = df[df['Country'] == selected_country].iloc[0]
    # MBTI 유형 열만 추출 (첫 번째 열인 'Country' 제외)
    country_series = row.drop('Country')
    
    # 숫자형으로 변환 후 내림차순 정렬
    country_series = pd.to_numeric(country_series).sort_values(ascending=False)
    
    labels = country_series.index.tolist()
    values = country_series.values.tolist()
    
    # 색상 설정 (1위는 빨간색, 나머지는 순위에 따라 파란색 그라데이션)
    colors = []
    for i in range(len(values)):
        if i == 0:
            colors.append('rgba(255, 0, 0, 0.9)')  # 1등: 빨간색
        else:
            # 순위가 낮아질수록 파란색이 투명해지도록 설정
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
        title=dict(text=f"<b>{selected_country}</b>의 MBTI 유형 분포 (높은 순)", font=dict(size=20)),
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis=dict(tickformat=".1%"),
        template="plotly_white",
        height=600,
        margin=dict(t=80, b=40, l=40, r=40)
    )

    # 그래프 출력 (오류 수정됨: use_container_width)
    st.plotly_chart(fig, use_container_width=True)

    # 상세 데이터 확인
    with st.expander("📊 상세 데이터 순위표 보기"):
        rank_df = pd.DataFrame({
            '순위': range(1, 17),
            'MBTI 유형': labels,
            '비율': [f"{v*100:.2f}%" for v in values]
        })
        st.dataframe(rank_df, use_container_width=True, hide_index=True)
else:
    st.info("파일 'countriesMBTI_16types.csv'가 소스 코드와 같은 폴더에 있는지 확인해주세요.")
