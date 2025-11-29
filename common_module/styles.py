import streamlit as st

def apply_placeholder_style():
    st.markdown("""
        <style>
        input::placeholder {
            font-size: 12px !important;
            color: #999999 !important;
        }
        </style>
    """, unsafe_allow_html=True)
