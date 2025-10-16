import streamlit as st
import json
import requests

url = "https://raw.githubusercontent.com/Bonitabueno/0331project/refs/heads/main/popup_store.json"
data = requests.get(url).json()

json_str = json.dumps(data, indent=2, ensure_ascii=False)
edited_json = st.text_area("🧾 JSON 편집", json_str, height=300)

try:
    parsed_data = json.loads(edited_json)
    st.success("✅ JSON 구문 오류 없음")
    st.json(parsed_data)
except json.JSONDecodeError:
    st.error("❌ JSON 형식 오류가 있습니다.")
