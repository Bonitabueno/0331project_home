import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# 쿠키 매니저 초기화
def init_cookies(prefix="0331_admin_", password="my_secret_password_0331"):
    cookies = EncryptedCookieManager(prefix=prefix, password=password)
    if not cookies.ready():
        st.stop()
    return cookies
