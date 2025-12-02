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
    # 원본 구조 그대로 유지 + sejong-si → Sejong 예외 처리 추가
    raw_parts = [p.strip() for p in addr.split(",") if p.strip()]

    parts = []
    for p in raw_parts:
        if "South Korea" in p:
            continue
        if any(c.isdigit() for c in p):
            continue

        # 세종 예외
        if p.lower() == "sejong-si":
            parts.append("Sejong")
        else:
            parts.append(p)

    neighborhood = next((p for p in parts if p.endswith("-dong") or p.endswith("-ri") or p.endswith("-eup")), "")

    district_candidates = [p for p in parts if p.endswith("-gu") or p.endswith("-si")]

    special_cities = ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan", "Sejong"]

    city_candidates = []
    for p in reversed(parts):
        if p.endswith("-do"):
            city_candidates.append(p)
        elif p in special_cities:
            city_candidates.append(p)
        elif p.endswith("-si") and p not in district_candidates:
            city_candidates.append(p)

    results = []
    for city in city_candidates:
        for district in district_candidates:
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

    do_candidates = [p for p in parts if p.endswith("-do")]
    si_candidates = [p for p in parts if p.endswith("-si")]
    gu_candidates = [p for p in parts if p.endswith("-gu")]

    if do_candidates and si_candidates and gu_candidates and neighborhood:
        do_name = do_candidates[0]
        for si in si_candidates:
            for gu in gu_candidates:
                if not any(r["city"] == si.split("-")[0] and r["district"] == gu for r in results):
                    results.append({
                        "restaurant_name": restaurant_name,
                        "restaurant_type": restaurant_type,
                        "city": si.split("-")[0],
                        "district": gu,
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
