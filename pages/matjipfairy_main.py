import streamlit as st
import requests
import pandas as pd
from common_module.date_time import today
from admin_module.login_management import init_cookies
from admin_module.login_management import check_login

# Streamlit 페이지 설정
st.set_page_config(page_title="0331 Project", layout="wide", page_icon="📊")

# 로그인 설정
cookies = init_cookies()
admin_id = check_login(cookies)

st.write("페이지 준비중입니다.")
