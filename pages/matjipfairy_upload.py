import streamlit as st
from common_module.styles import apply_placeholder_style

# CSS placeholder 적용
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
    # 쉼표 분리, 숫자/불필요 항목 제거
    parts = [p.strip() for p in addr.split(",") if p.strip() and "South Korea" not in p]

    # neighborhood 추출
    neighborhood = next((p for p in parts if p.endswith("-dong") or p.endswith("-ri") or p.endswith("-eup")), "")

    # district 후보: -gu, -si
    district_candidates = [p for p in parts if p.endswith("-gu") or p.endswith("-si")]

    # city 후보: 특별시, -do, -si
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

    # 1. 일반 district × city 조합 생성
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

    # 2. 특수 중첩: 도+시+구+동 패턴에서 city/district 위치 조합 생성
    if len(district_candidates) >= 2 and len(city_candidates) >= 2:
        for city_orig in city_candidates:
            if city_orig.endswith("-do"):
                do_name = city_orig
                si_candidates = [c for c in city_candidates if c.endswith("-si")]
                for si in si_candidates:
                    for district in district_candidates:
                        key = (si, district)
                        if not any(r["city"] == si and r["district"] == district for r in results):
                            results.append({
                                "restaurant_name": restaurant_name,
                                "restaurant_type": restaurant_type,
                                "city": si,
                                "district": district,
                                "neighborhood": neighborhood,
                                "address": addr,
                                "menu": [m.strip() for m in menu.split(",") if m.strip()],
                                "summary_menu": summary_menu,
                                "link": link,
                                "station": station
                            })

    # 3. 중복 제거
    unique_results = []
    seen = set()
    for r in results:
        key = (r["city"], r["district"])
        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    return unique_results


# 버튼 클릭 시
if st.button("데이터 확인"):
    parsed_data = parse_address(
        address, restaurant_name, restaurant_type,
        menu, summary_menu, link, station
    )
    st.json(parsed_data)
