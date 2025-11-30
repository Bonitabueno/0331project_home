import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from admin_module.login_management import init_cookies
from admin_module.login_management import check_login
from admin_module.allowed_admin import ALLOWED_ADMINS_0331
import requests
import pandas as pd

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="centered", page_icon="📊")

cookies = init_cookies()
admin_id = check_login(cookies)

# 아이디별 접근 페이지 설정
allowed_pages = ALLOWED_ADMINS.get(admin_id, [])

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
col1, col2, col3 = st.columns(3)

with col1:
    container1 = st.container()
    with container1:
        if "popuplive" in allowed_pages:
            if st.button("팝업라이브"):
                st.switch_page("pages/popuplive_main.py")
        else:
            st.button("관리자에게 권한을 요청하세요.", disabled=True)

with col2:
    container2 = st.container(border=True)
    with container2:
        if "post26" in allowed_pages:
            if st.button("포스트26"):
                st.write("페이지 준비중입니다.")
        else:
            st.button("관리자에게 권한을 요청하세요.", disabled=True)

with col3:
    container2 = st.container(border=True)
    with container2:
        if "matjipfairy" in allowed_pages:
            if st.button("맛집요정"):
                st.switch_page("pages/matjipfairy_main.py")
        else:
            st.button("관리자에게 권한을 요청하세요.", disabled=True)
            
# 구분선
st.divider()

# 다중 탭
tab1, tab2, tab3 = st.tabs(["클라우드타입", "테스트1", "테스트2"])

with tab1:
    try:
        response = requests.get("https://status.cloudtype.io/ko/index.json")
        data = response.json()

        included = data.get("included", [])

        resources = []
        for item in included:
            if item.get("type") == "status_page_resource":
                attr = item.get("attributes", {})
                resources.append({
                    "리소스 이름": attr.get("public_name"),
                    "상태": attr.get("status"),
                    "가용성": f"{attr.get('availability') * 100:.2f}%" if attr.get("availability") is not None else "N/A"
                })
        if resources:
            df = pd.DataFrame(resources)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📭 표시할 리소스 상태 정보가 없습니다.")
    except Exception as e:
        st.error(f"❌ 상태 정보를 불러오는 데 실패했습니다: {str(e)}")

    st.link_button("상태조회페이지", "https://status.cloudtype.io/ko")
