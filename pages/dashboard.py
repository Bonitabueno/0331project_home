import streamlit as st

container = st.container(border=True)

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
