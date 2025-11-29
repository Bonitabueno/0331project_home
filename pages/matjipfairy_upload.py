import streamlit as st
from common_module.styles import apply_placeholder_style

apply_placeholder_style()

st.subheader("식당/카페 정보 업로드 (주소 기반)")

restaurant_name = st.text_input("식당명", key="restaurant_name_input")
restaurant_type = st.text_input("업종", key="restaurant_type_input")
address = st.text_input("전체 주소", key="address_input")
menu = st.text_input("메뉴", placeholder="여러 메뉴를 입력할 경우 쉼표로 구분", key="menu_input")
summary_menu = st.text_input("메뉴 요약", key="summary_menu_input")
link = st.text_input("링크", key="link_input")
station = st.text_input("주변 역", key="station_input")


def parse_address(addr, restaurant_name, restaurant_type, menu, summary_menu, link, station):
    # 쉼표로 분리 후 숫자 포함 항목, South Korea 제거
    parts = [p.strip() for p in addr.split(",") if p.strip() and not any(c.isdigit() for c in p) and "South Korea" not in p]

    # neighborhood 추출
    neighborhood = next((p for p in parts if p.endswith("-dong") or p.endswith("-ri") or p.endswith("-eup")), "")

    # district 후보
    district_candidates = [p for p in parts if p.endswith("-gu") or p.endswith("-si")]

    # city 후보
    special_cities = ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan", "Sejong"]
    city_candidates = []
    for p in reversed(parts):
        if p.endswith("-do"):
            city_candidates.append(p.replace("-do", "").strip())
        elif p in special_cities:
            city_candidates.append(p)
        elif p.endswith("-si") and p not in district_candidates:
            city_candidates.append(p.split("-")[0].strip())

    results = []

    # district와 city 순서대로 1:1 매칭
    for i, district in enumerate(district_candidates):
        if i < len(city_candidates):
            city = city_candidates[i]
        else:
            # city 후보 부족 시 마지막 city 반복 금지
            city = city_candidates[-1] if city_candidates else ""
        results.append({
            "restaurant_name": restaurant_name,
            "restaurant_type": restaurant_type,
            "city": city,
            "district": district,
            "neighborhood": neighborhood,
            "address": addr,
            "menu": [m.strip() for m in menu.split(",") if m.strip()],
            "summary_menu": summary_menu,
            "link": link,
            "station": station
        })

    # 일반 주소 처리: district 후보 1개, city 후보 1개만 있을 경우 JSON 1개 생성
    if not results and district_candidates and city_candidates:
        results.append({
            "restaurant_name": restaurant_name,
            "restaurant_type": restaurant_type,
            "city": city_candidates[0],
            "district": district_candidates[0],
            "neighborhood": neighborhood,
            "address": addr,
            "menu": [m.strip() for m in menu.split(",") if m.strip()],
            "summary_menu": summary_menu,
            "link": link,
            "station": station
        })

    return results


if st.button("데이터 확인"):
    parsed_data = parse_address(address, restaurant_name, restaurant_type, menu, summary_menu, link, station)
    st.json(parsed_data)
