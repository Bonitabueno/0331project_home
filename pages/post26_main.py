import streamlit as st
from admin_module.login_management import init_cookies
from admin_module.login_management import check_login

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="wide", page_icon="📊")

# 로그인 설정
cookies = init_cookies()
admin_id = check_login(cookies)

# 사용자 컨테이너 (문구 + 로그아웃 버튼)
with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("홈"):
            st.switch_page("pages/home.py")

    with col2:
        if st.button("로그아웃"):
            cookies["admin_id"] = ""
            cookies.save()
            st.session_state["admin_id"] = None
            st.switch_page("app.py")

st.write("페이지 준비중입니다.")
