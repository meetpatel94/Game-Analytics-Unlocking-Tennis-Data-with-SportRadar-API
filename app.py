import streamlit as st

from components.loader import show_loader

from streamlit_app.dashboard import show_dashboard
from streamlit_app.competitions import show_competitions
from streamlit_app.venues import show_venues
from streamlit_app.competitors import show_competitors
from streamlit_app.rankings import show_rankings

# =====================================
# =================CSS=================


# =====================================

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Tennis Game Analytics",
    page_icon="🎾",
    layout="wide"
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🎾 Tennis Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Competitions",
        "Venues",
        "Competitors",
        "Rankings"
    ]
)

# =====================================
# PAGE ROUTING
# =====================================

if page == "Dashboard":

    show_loader("Dashboard")
    show_dashboard()

elif page == "Competitions":

    show_loader("Competitions")
    show_competitions()

elif page == "Venues":

    show_loader("Venues")
    show_venues()

elif page == "Competitors":

    show_loader("Competitors")
    show_competitors()

elif page == "Rankings":

    show_loader("Rankings")
    show_rankings()