import streamlit as st

# 컬럼 생성 : 현재 2개
col1, col2 = st.columns(2)

# 첫 번째 컬럼 안에 컨테이너
with col1:
    container1 = st.container()
    with container1:
        if st.button("컬럼 1 버튼"):
            st.write("컬럼 1 버튼 클릭됨")

# 두 번째 컬럼 안에 컨테이너
with col2:
    container2 = st.container()
    with container2:
        if st.button("컬럼 2 버튼"):
            st.write("컬럼 2 버튼 클릭됨")
