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

# 로그인 유지
if admin_id:
    st.session_state["admin_id"] = admin_id

    # 컨테이너 (환영 문구 + 로그아웃 버튼)
    container = st.container(border=True)
    container.write(f"{admin_id}님 환영합니다.")
    if container.button("로그아웃"):
        cookies["admin_id"] = ""
        cookies.save()
        st.session_state["admin_id"] = None
        st.success("로그아웃되었습니다.")
        st.switch_page("app.py")
else:
    st.warning("로그인이 필요합니다.")
    st.stop()

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
