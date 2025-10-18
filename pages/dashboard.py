import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from admin_module.login_management import init_cookies
from admin_module.login_management import check_login

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="centered", page_icon="📊")

cookies = init_cookies()
admin_id = check_login(cookies)

# 사용자 컨테이너 (문구 + 로그아웃 버튼)
container = st.container(border=True)
container.write(f"{admin_id}님 환영합니다.")
if container.button("로그아웃"):
    cookies["admin_id"] = ""
    cookies.save()
    st.session_state["admin_id"] = None
    st.switch_page("app.py")

# 구분선
st.divider()

# 컬럼 생성 : 현재 2개
col1, col2 = st.columns(2)

with col1:
    container1 = st.container(border=True)
    with container1:
        if st.button("팝업라이브"):
            st.switch_page("pages/popuplive_main.py")

with col2:
    container2 = st.container(border=True)
    with container2:
        if st.button("포스트26"):
            st.write("컬럼 2 버튼 클릭됨")
