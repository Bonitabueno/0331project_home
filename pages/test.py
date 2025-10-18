import streamlit as st
import json
import requests

# JSON 데이터 불러오기
url = "https://raw.githubusercontent.com/Bonitabueno/0331project/refs/heads/main/popup_store.json"
data = requests.get(url).json()

json_str = json.dumps(data, indent=2, ensure_ascii=False)

# 세션 상태 초기화
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False
if "json_valid" not in st.session_state:
    st.session_state["json_valid"] = False

# 텍스트 영역 (편집 가능 여부)
edited_json = st.text_area(
    "🧾 **JSON 데이터**",
    json_str,
    height=800,
    disabled=not st.session_state["edit_mode"]
)

# 버튼 영역
col1, col2, col3 = st.columns([1, 1, 1])

# 편집 모드 OFF
if not st.session_state["edit_mode"]:
    with col1:
        if st.button("편집"):
            st.session_state["edit_mode"] = True
            st.session_state["json_valid"] = False
else:
    with col1:
        if st.button("취소"):
            st.session_state["edit_mode"] = False
            st.session_state["json_valid"] = False

    with col2:
        if st.button("확인"):
            try:
                json.loads(edited_json)
                st.session_state["json_valid"] = True
                st.success("✅ JSON 구문 오류 없음")
            except json.JSONDecodeError:
                st.session_state["json_valid"] = False
                st.error("❌ JSON 형식 오류가 있습니다.")

    with col3:
        if st.button("저장", disabled=not st.session_state["json_valid"]):
            # 저장 동작
            st.session_state["edit_mode"] = False
            st.session_state["json_valid"] = False
            st.success("💾 저장 완료!")
