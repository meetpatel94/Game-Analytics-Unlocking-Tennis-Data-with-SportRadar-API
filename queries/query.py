import pandas as pd
import streamlit as st
from database.db import get_engine

@st.cache_data(ttl=600)
def run_query(query):
    engine = get_engine()
    return pd.read_sql(query, engine)