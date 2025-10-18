import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# 쿠키 매니저 초기화
def init_cookies(prefix="0331_admin_", password="my_secret_password_0331"):
    cookies = EncryptedCookieManager(prefix=prefix, password=password)
    if not cookies.ready():
        st.stop()
    return cookies

# 로그인 체크
def check_login(cookies):
    admin_id = st.session_state.get("admin_id") or cookies.get("admin_id")
    if not admin_id:
        st.warning("로그인이 필요합니다.")
        st.switch_page("app.py")
    st.session_state["admin_id"] = admin_id
    return admin_id
