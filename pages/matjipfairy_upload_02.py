import streamlit as st
from common_module.styles import apply_placeholder_style
from dotenv import load_dotenv
import os
import json
from pymongo import MongoClient

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="centered", page_icon="📊")

# CSS 설정
apply_placeholder_style()

# 데이터베이스 & 데이터 컬렉션 설정
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "matjip_db"
COLLECTION_NAME = "matjip_info"

# 세션 상태 초기화
if "matjip_data" not in st.session_state:
    st.session_state.matjip_data = None
    
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

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

# ============================
# 1️⃣ 데이터 확인 버튼
# ============================
if st.button("데이터 확인"):
    fixed_address = address.replace(" District", "-gu")

    st.session_state.matjip_data = {
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
    }

    st.json(st.session_state.matjip_data)
    st.info("데이터를 한번 더 확인한 후, 아래 버튼으로 업로드 해주세요.")

# ============================
# 2️⃣ 업로드 버튼 (데이터 확인 후 표시)
# ============================
if st.session_state.matjip_data is not None:
    if st.button("DB 업로드"):
        try:
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]

            result = collection.insert_one(st.session_state.matjip_data)

            client.close()

            st.success(f"데이터 업로드 완료! 문서 ID: {result.inserted_id}")

            # 업로드 완료 후 모든 입력 필드 + matjip_data 초기화
            for key in [
                "restaurant_name_input",
                "restaurant_type_input",
                "city_input",
                "district_input",
                "neighborhood_input",
                "address_input",
                "menu_input",
                "summary_menu_input",
                "link_input",
                "station_input",
                "matjip_data",
            ]:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

        except Exception as e:
            st.error(f"데이터 업로드 중 오류 발생: {e}")
