import streamlit as st
import traceback
from admin_module.allowed_admin import ALLOWED_ADMINS_0331

# Streamlit 페이지 설정
st.set_page_config(page_title="Project 0331", layout="centered", page_icon="📊")

# 허용된 관리자
ALLOWED_ADMINS = ALLOWED_ADMINS_0331

# 세션 초기화
if "admin_id" not in st.session_state:
    st.session_state["admin_id"] = None

# 로그인 화면
if st.session_state["admin_id"] is None:
    st.title("🔐 로그인")
    admin_input = st.text_input("아이디를 입력하세요")

    if st.button("로그인"):
        if admin_input in ALLOWED_ADMINS:
            st.session_state["admin_id"] = admin_input
            try:
                st.switch_page("dashboard.py")
            except Exception as e:
                st.code(traceback.format_exc())
        else:
            st.error("🚫 접근이 허용되지 않은 아이디입니다.")
