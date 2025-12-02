import streamlit as st



st.markdown("")
st.markdown("**맛집요정 Global**")
st.markdown("")

# 컬럼 생성 : 현재 2개
left_col, right_col = st.columns(2)

with left_col:
    st.link_button("STG", "https://port-0-matjip-fairy-global-mbrrqxp1539f7d68.sel4.cloudtype.app")

with right_col:
    st.link_button("PRD", "https://matjipfairy.netlify.app")
