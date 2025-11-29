import streamlit as st
from common_module.styles import apply_placeholder_style

apply_placeholder_style()

st.subheader("식당/카페 정보 업로드 (주소 기반)")

# 입력 필드
restaurant_name = st.text_input("식당명", key="restaurant_name_input")
restaurant_type = st.text_input("업종", key="restaurant_type_input")
address = st.text_input("전체 주소", key="address_input")
menu = st.text_input("메뉴", placeholder="여러 메뉴를 입력할 경우 쉼표로 구분", key="menu_input")
summary_menu = st.text_input("메뉴 요약", key="summary_menu_input")
link = st.text_input("링크", key="link_input")
station = st.text_input("주변 역", key="station_input")


def parse_address(addr, restaurant_name, restaurant_type, menu, summary_menu, link, station):
    # 쉼표 분리 후 숫자/불필요 항목(South Korea) 제거
    parts = [p.strip() for p in addr.split(",") if p.strip() and "South Korea" not in p and not any(c.isdigit() for c in p)]

    # neighborhood 추출
    neighborhood = next((p for p in parts if p.endswith("-dong") or p.endswith("-ri") or p.endswith("-eup")), "")

    # district 후보: -gu, -si
    district_candidates = [p for p in parts if p.endswith("-gu") or p.endswith("-si")]

    # city 후보
    special_cities = ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan", "Sejong"]
    do_candidates = [p for p in parts if p.endswith("-do")]

    si_candidates = [p for p in parts if p.endswith("-si") and p not in district_candidates]

    city_candidates = []
    if do_candidates:
        city_candidates.extend(do_candidates)
    if si_candidates:
        city_candidates.extend(si_candidates)
    for p in reversed(parts):
        if p in special_cities:
            city_candidates.append(p)

    results = []

    # 일반 주소: 특별시/광역시+구+동 또는 도+시+동
    if len(do_candidates) <= 1 and len(district_candidates) <= 1:
        city = city_candidates[0] if city_candidates else ""
        district = district_candidates[0] if district_candidates else ""
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
    # 특수 중첩 주소: 도+시+구+동
    elif len(do_candidates) == 1 and len(si_candidates) == 1 and len(district_candidates) == 2:
        do_name = do_candidates[0]
        si_name = si_candidates[0]
        gu_name = next(d for d in district_candidates if d != si_name)

        # 3가지 조합 생성
        results.append({
            "restaurant_name": restaurant_name,
            "restaurant_type": restaurant_type,
            "city": do_name,
            "district": si_name,
            "neighborhood": neighborhood,
            "address": addr,
            "menu": [m.strip() for m in menu.split(",") if m.strip()],
            "summary_menu": summary_menu,
            "link": link,
            "station": station
        })
        results.append({
            "restaurant_name": restaurant_name,
            "restaurant_type": restaurant_type,
            "city": do_name,
            "district": gu_name,
            "neighborhood": neighborhood,
            "address": addr,
            "menu": [m.strip() for m in menu.split(",") if m.strip()],
            "summary_menu": summary_menu,
            "link": link,
            "station": station
        })
        results.append({
            "restaurant_name": restaurant_name,
            "restaurant_type": restaurant_type,
            "city": si_name,
            "district": gu_name,
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
