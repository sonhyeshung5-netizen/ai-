import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="Seoul Top 10 Tourist Attractions", layout="wide")

st.title("🇰🇷 외국인이 사랑하는 서울 관광지 TOP 10")
st.subheader("마커 위에 마우스를 올리면 인근 지하철역을 확인할 수 있습니다.")

# 관광지 데이터 (이름, 위도, 경도, 인근역, 즐길거리)
locations = [
    {"name": "경복궁", "lat": 37.5796, "lon": 126.9770, "station": "경복궁역 (3호선)", "todo": "한복 체험, 수문장 교대식 관람"},
    {"name": "명동", "lat": 37.5637, "lon": 126.9841, "station": "명동역 (4호선)", "todo": "길거리 음식 탐방, K-뷰티 쇼핑"},
    {"name": "N서울타워", "lat": 37.5512, "lon": 126.9882, "station": "명동역/충무로역 (셔틀 이용)", "todo": "서울 파노라마 뷰 감상, 사랑의 자물쇠"},
    {"name": "롯데월드 & 타워", "lat": 37.5111, "lon": 127.1004, "station": "잠실역 (2, 8호선)", "todo": "테마파크 이용, 서울스카이 전망대"},
    {"name": "북촌 한옥마을", "lat": 37.5829, "lon": 126.9835, "station": "안국역 (3호선)", "todo": "전통 가옥 산책, 전통차 시음"},
    {"name": "홍대 거리", "lat": 37.5567, "lon": 126.9236, "station": "홍대입구역 (2호선, 공항철도)", "todo": "버스킹 관람, 이색 카페 및 클럽"},
    {"name": "이태원", "lat": 37.5345, "lon": 126.9946, "station": "이태원역 (6호선)", "todo": "세계 음식 맛집 탐방, 루프탑 바"},
    {"name": "동대문 디자인 플라자(DDP)", "lat": 37.5665, "lon": 127.0092, "station": "동대문역사문화공원역 (2, 4, 5호선)", "todo": "전시회 관람, 야간 패션 시장 쇼핑"},
    {"name": "익선동", "lat": 37.5744, "lon": 126.9897, "station": "종로3가역 (1, 3, 5호선)", "todo": "개량 한옥 카페 투어, 아기자기한 소품숍"},
    {"name": "광장시장", "lat": 37.5701, "lon": 126.9993, "station": "종로5가역 (1호선)", "todo": "빈대떡, 육회 등 전통 시장 먹거리"}
]

# 1. 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 2. 마커 추가
for loc in locations:
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=f"<b>{loc['name']}</b><br>{loc['todo']}", # 클릭 시 표시
        tooltip=f"가까운 역: {loc['station']}",      # 마우스 오버 시 표시
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# 스트림릿에 지도 표시
st_folium(m, width=1000, height=500)

---

# 3. 하단 상세 설명 (Table)
st.write("### 📍 관광지별 상세 정보")
for loc in locations:
    with st.expander(f"{loc['name']}"):
        st.write(f"🚉 **가까운 지하철역:** {loc['station']}")
        st.write(f"🎡 **추천 놀거리:** {loc['todo']}")
