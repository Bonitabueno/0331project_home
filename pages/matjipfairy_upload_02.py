import streamlit as st
from common_module.styles import apply_placeholder_style
from dotenv import load_dotenv
import os
import json

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="centered", page_icon="📊")

# CSS 설정
apply_placeholder_style()

# 데이터베이스 & 데이터 컬렉션 설정
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "matjip_db"
COLLECTION_NAME = "matjip_info"

st.subheader("식당/카페 정보 업로드")

restaurant_name = st.text_input("식당명", key="restaurant_name_input")
restaurant_type = st.text_input("업종", key="restaurant_type_input")
city = st.text_input("특별시/광역시/도(City)", key="city_input")
district = st.text_input("시/군/구(District)", key="district_input")
neighborhood = st.text_input("읍/면/동(Neighborhood)", key="neighborhood_input")
address = st.text_input("전체 주소", key="address_input")
menu = st.text_input("메뉴", placeholder ="여러 메뉴를 입력할 경우 쉼표로 구분해서 입력해주세요.", key="menu_input")
summary_menu = st.text_input("메뉴 요약", key="summary_menu_input")
link = st.text_input("링크", key="link_input")
station = st.text_input("주변 역", key="station_input")

if st.button("데이터 확인"):
    fixed_address = address.replace(" District", "-gu")
    
    st.json({
        "restaurant_name": restaurant_name,
        "restaurant_type": restaurant_type,
        "city": city,
        "district": district,
        "neighborhood": neighborhood,
        "address": fixed_address,
        "menu": [m.strip() for m in menu.split(",") if m.strip()],
        "summary_menu": summary_menu,
        "link": link,
        "station": station
    })
