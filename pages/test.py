import streamlit as st
import json
import requests

# JSON 데이터 불러오기
url = "https://raw.githubusercontent.com/Bonitabueno/0331project/refs/heads/main/popup_store.json"
data = requests.get(url).json()

json_str = json.dumps(data, indent=2, ensure_ascii=False)

# 편집 모드 상태
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False

# 텍스트 영역 (편집 가능 여부)
edited_json = st.text_area(
    "🧾 JSON 데이터",
    json_str,
    height=800,
    disabled=not st.session_state["edit_mode"]
)

# 편집 버튼
if not st.session_state["edit_mode"]:
    if st.button("✏️ 편집"):
        st.session_state["edit_mode"] = True
else:
    if st.button("🔒 편집 종료"):
        st.session_state["edit_mode"] = False

# JSON 유효성 검사
try:
    parsed_data = json.loads(edited_json)
    st.success("✅ JSON 구문 오류 없음")
except json.JSONDecodeError:
    st.error("❌ JSON 형식 오류가 있습니다.")
