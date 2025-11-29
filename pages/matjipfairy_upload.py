import streamlit as st

# placeholder 글씨 크기 줄이기 위한 CSS
st.markdown("""
    <style>
    input::placeholder {
        font-size: 12px !important;   /* 원하는 크기로 조절 */
        color: #999999 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("식당/카페 정보 업로드")

restaurant_name = st.text_input("식당명", key="restaurant_name_input")
restaurant_type = st.text_input("업종", key="restaurant_type_input")
city = st.text_input("특별시/광역시/도(City)", key="city_input")
district = st.text_input("시/군/구(District)", key="district_input")
neighborhood = st.text_input("읍/면/동("Neighborhood"), key="neighborhood_input")
address = st.text_input("전체 주소", key="address_input")
menu = st.text_input("메뉴", placeholder ="여러 메뉴를 입력할 경우 쉼표로 구분해서 입력해주세요.", key="menu_input")
summary_menu = st.text_input("메뉴 요약", key="summary_menu_input")
link = st.text_input("링크", key="link_input")
station = st.text_input("주변 역", key="station_input")

if st.button("데이터 확인"):
    st.json({
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
