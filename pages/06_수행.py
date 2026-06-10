import streamlit as str

# 웹페이지 제목 및 아이콘 설정
str.set_page_config(page_title="냉장고 파먹기 레시피 추천", page_icon="🍳")

# 간단한 레시피 데이터베이스
RECIPE_DB = {
    "계란": {
        "dish": "부드러운 계란찜",
        "ingredients": ["계란 3개", "물 100ml", "소금 소량", "쪽파 약간"],
        "steps": [
            "계란을 그릇에 풀고 물과 소금을 넣어 잘 섞어줍니다.",
            "체에 한번 거르면 더 부드러워집니다.",
            "전자레인지용 용기에 담아 랩을 씌운 후 구멍을 뚫어줍니다.",
            "전자레인지에서 3분 30초간 조리합니다."
        ]
    },
    "두부": {
        "dish": "매콤 두부조림",
        "ingredients": ["두부 1모", "간장 3스푼", "고춧가루 1스푼", "다진 마늘 0.5스푼", "물 0.5컵"],
        "steps": [
            "두부를 먹기 좋은 크기로 썰어 물기를 제거합니다.",
            "양념장 재료(간장, 고춧가루, 마늘, 물)를 한데 섞어줍니다.",
            "팬에 기름을 두르고 두부를 앞뒤로 노릇하게 구웁니다.",
            "양념장을 붓고 국물이 자작해질 때까지 졸입니다."
        ]
    },
    "김치": {
        "dish": "백종원풍 김치볶음밥",
        "ingredients": ["신김치 1컵", "밥 1공기", "대파 1/2대", "간장 1스푼", "설탕 0.5스푼"],
        "steps": [
            "대파를 송송 썰어 식용유를 두른 팬에 볶아 파기름을 냅니다.",
            "다진 김치와 설탕을 넣고 함께 볶아줍니다.",
            "재료를 한쪽으로 밀고 빈 공간에 간장을 눌려 불맛을 냅니다.",
            "불을 끄고 밥을 넣어 잘 비빈 후, 다시 불을 켜서 살짝 볶아 마무리합니다."
        ]
    },
    "닭고기": {
        "dish": "달콤 짭조름한 찜닭",
        "ingredients": ["닭고기 500g", "감자 1개", "양파 1/2개", "간장 5스푼", "올리고당 2스푼"],
        "steps": [
            "닭고기는 끓는 물에 데쳐 불순물을 제거합니다.",
            "냄비에 닭고기, 썰어둔 감자, 양파, 물을 넣고 끓입니다.",
            "간장과 올리고당으로 양념을 하고 중불에서 졸입니다.",
            "감자가 완전히 익고 양념이 잘 배어들면 완성입니다."
        ]
    }
}

# UI 구성
str.title("🍳 냉장고 파먹기! 레시피 추천 시스템")
str.write("가지고 있는 주요 식재료를 선택하면 맛있는 요리를 추천해 드려요.")

str.markdown("---")

# 식재료 선택 셀렉트박스
selected_ingredient = str.selectbox(
    "지금 냉장고에 있는 재료를 골라보세요 👇",
    options=list(RECIPE_DB.keys()),
    index=0
)

# 선택된 재료에 따른 레시피 출력
if selected_ingredient:
    recipe_info = RECIPE_DB[selected_ingredient]
    
    str.subheader(Target:= f"💡 추천 요리: **{recipe_info['dish']}**")
    
    # 2단 레이아웃 구성 (좌측: 재료, 우측: 조리 순서)
    col1, col2 = str.columns(2)
    
    with col1:
        str.markdown("### 🛒 필요 재료")
        for ing in recipe_info["ingredients"]:
            str.write(f"- {ing}")
            
    with col2:
        str.markdown("### 👨‍🍳 조리 순서")
        for i, step in enumerate(recipe_info["steps"], 1):
            str.write(f"{i}. {step}")

str.markdown("---")
str.caption("맛있는 식사 시간 되세요! 🍽️")
