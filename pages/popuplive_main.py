import streamlit as st
import requests
import json

# 깃허브 JSON raw 주소
url = "https://raw.githubusercontent.com/Bonitabueno/0331project/refs/heads/main/popup_store.json"

# JSON 가져오기
try:
    response = requests.get(url)
    response.raise_for_status()  # 요청 에러 확인
    data = response.json()  # JSON 파싱
    st.json(data)  # 화면에 예쁘게 표시
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류 발생: {e}")

