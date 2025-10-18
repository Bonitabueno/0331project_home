import streamlit as st
import requests
import pandas as pd

# JSON 불러오기
url = "https://raw.githubusercontent.com/Bonitabueno/0331project/refs/heads/main/popup_store.json"
data = requests.get(url).json()

# DataFrame 변환
df = pd.DataFrame(data)

# Streamlit 표시
st.title("📋 팝업스토어 리스트")
st.dataframe(df, use_container_width=True)
