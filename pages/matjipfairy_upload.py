import streamlit as st
from common_module.styles import apply_placeholder_style

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="centered", page_icon="📊")

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
    raw_parts = [p.strip() for p in addr.split(",") if p.strip()]

    filtered_parts = []
    for p in raw_parts:
        if "South Korea" in p:
            continue
        if any(c.isdigit() for c in p):
            continue

        if p.lower() == "sejong-si":
            filtered_parts.append("Sejong")
        else:
            filtered_parts.append(p)

    parts = filtered_parts

    neighborhood = next(
        (p for p in parts if p.endswith("-dong") or p.endswith("-ri") or p.endswith("-eup")),
        ""
    )

    district_candidates = [p for p in parts if p.endswith("-gu") or p.endswith("-si")]

    special_cities = ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan", "Sejong"]

    city_candidates = []
    for p in reversed(parts):
        if p in special_cities:
            city_candidates.append(p)
        elif p.endswith("-do"):
            city_candidates.append(p.replace("-do", "").strip())
        elif p.endswith("-si") and p not in district_candidates:
            city_candidates.append(p.split("-")[0].strip())

    results = []

    for district in district_candidates:
        for city in city_candidates:
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

    unique_results = []
    seen = set()
    for r in results:
        key = (r["city"], r["district"])
        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    return unique_results


if st.button("데이터 확인"):
    parsed_data = parse_address(address, restaurant_name, restaurant_type, menu, summary_menu, link, station)
    st.json(parsed_data)
