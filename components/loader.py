import streamlit as st
import time


def show_loader(page_name):

    with st.spinner(
        f"🎾 Loading {page_name} Analytics..."
    ):
        time.sleep(1)