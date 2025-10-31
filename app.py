import streamlit as st
import traceback
from streamlit_cookies_manager import EncryptedCookieManager
from admin_module.allowed_admin import ALLOWED_ADMINS_0331

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="centered", page_icon="📊")

# 쿠키 매니저 설정
cookies = EncryptedCookieManager(
    prefix="0331_admin_",
    password="my_secret_password_0331"  # 원하는 임의 문자열 (비밀키)
)

# 허용된 관리자
ALLOWED_ADMINS = ALLOWED_ADMINS_0331

# 세션 + 쿠키 초기화
if "admin_id" not in st.session_state:
    st.session_state["admin_id"] = cookies.get("admin_id")

# 로그인 화면
if st.session_state["admin_id"] is None:
    st.title("🔐 로그인")
    admin_input = st.text_input("아이디를 입력하세요")

    if st.button("로그인"):
        if admin_input in ALLOWED_ADMINS:
            st.session_state["admin_id"] = admin_input
            cookies["admin_id"] = admin_input
            cookies.save()  # 쿠키 저장
            try:
                st.switch_page("pages/home.py")
            except Exception as e:
                st.code(traceback.format_exc())
        else:
            st.error("🚫 접근이 허용되지 않은 아이디입니다.")
