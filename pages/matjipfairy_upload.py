import streamlit as st
from common_module.styles import apply_placeholder_style

# CSS 설정
apply_placeholder_style()

st.subheader("식당/카페 정보 업로드 (주소 기반)")

# 기본 입력
restaurant_name = st.text_input("식당명", key="restaurant_name_input")
restaurant_type = st.text_input("업종", key="restaurant_type_input")
address = st.text_input("전체 주소", key="address_input")
menu = st.text_input("메뉴", placeholder="여러 메뉴를 입력할 경우 쉼표로 구분", key="menu_input")
summary_menu = st.text_input("메뉴 요약", key="summary_menu_input")
link = st.text_input("링크", key="link_input")
station = st.text_input("주변 역", key="station_input")

def parse_address(addr):
    """
    주소 문자열을 받아 city, district, neighborhood 추출.
    특수 케이스: 기초단체 중복 시 모든 조합으로 반환
    """
    addr_parts = [p.strip() for p in addr.split(",") if p.strip()]

    # South Korea와 상세 번호 제외
    filtered = [p for p in addr_parts if "South Korea" not in p and not any(c.isdigit() for c in p)]

    # neighborhood: 보통 -dong, -ri, -eup
    neighborhood = ""
    for p in filtered:
        if p.endswith("-dong") or p.endswith("-ri") or p.endswith("-eup"):
            neighborhood = p
            break

    # 후보 district: -gu, -si 등
    district_candidates = [p for p in filtered if p.endswith("-gu") or p.endswith("-si")]

    # 후보 city: -do 제거, 특별시/광역시 처리
    special_cities = ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan", "Sejong"]
    city_candidates = []
    for p in reversed(filtered):
        if p.endswith("-do"):
            city_candidates.append(p.replace("-do","").strip())
        elif p.endswith("-si") or p.endswith("-gu"):
            city_candidates.append(p.split("-")[0].strip())
        elif p in special_cities:
            city_candidates.append(p)

    # 모든 조합 생성
    results = []
    for city in city_candidates:
        for district in district_candidates:
            results.append({
                "restaurant_name": restaurant_name,
                "restaurant_type": restaurant_type,
                "city": city,
                "district": district,
                "neighborhood": neighborhood,
                "address": address,
                "menu": [m.strip() for m in menu.split(",") if m.strip()],
                "summary_menu": summary_menu,
                "link": link,
                "station": station
            })
    return results

if st.button("데이터 확인"):
    parsed_data = parse_address(address)
    st.json(parsed_data)
