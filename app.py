import streamlit as st
import traceback
from streamlit_cookies_manager import EncryptedCookieManager
from admin_module.allowed_admin import ALLOWED_ADMINS_0331

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="centered", page_icon="📊")

st.title("테스트")
