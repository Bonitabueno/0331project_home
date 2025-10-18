import streamlit as st
import requests
import pandas as pd
from common_module.date_time import today
from admin_module.login_management import init_cookies
from admin_module.login_management import check_login

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="wide", page_icon="📊")

# 로그인 설정
cookies = init_cookies()
admin_id = check_login(cookies)

# JSON 불러오기
url = "https://raw.githubusercontent.com/Bonitabueno/0331project/refs/heads/main/popup_store.json"
data = requests.get(url).json()

# DataFrame 변환
df = pd.DataFrame(data)
df.index = df.index + 1 # 인덱스 열 1번부터 시작
df.index.name = "" # 인덱스 열 이름 지정

# 사용자 컨테이너 (문구 + 로그아웃 버튼)
container = st.container(border=True)
container.write(f"{admin_id}님 환영합니다.")
if container.button("로그아웃"):
    cookies["admin_id"] = ""
    cookies.save()
    st.session_state["admin_id"] = None
    st.switch_page("app.py")

# Streamlit 표시
st.markdown(today)
st.markdown("**팝업스토어 리스트**")
st.dataframe(df)
