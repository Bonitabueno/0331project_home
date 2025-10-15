import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# 쿠키 매니저 설정
cookies = EncryptedCookieManager(
    prefix="0331_admin_",
    password="my_secret_password_0331"
)
if not cookies.ready():
    st.stop()

# 세션에 저장된 admin_id 불러오기
admin_id = st.session_state.get("admin_id") or cookies.get("admin_id")

# Streamlit UI
container = st.container(border=True)
container.write(f"{admin_id}님 환영합니다.")

# 컬럼 생성 : 현재 2개
col1, col2 = st.columns(2)

with col1:
    container1 = st.container(border=True)
    with container1:
        if st.button("팝업라이브"):
            st.write("컬럼 1 버튼 클릭됨")

with col2:
    container2 = st.container(border=True)
    with container2:
        if st.button("포스트26"):
            st.write("컬럼 2 버튼 클릭됨")
