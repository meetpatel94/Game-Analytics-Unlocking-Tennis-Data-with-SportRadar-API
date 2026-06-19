import streamlit as st

from components.loader import show_loader

from streamlit_app.dashboard import show_dashboard
from streamlit_app.competitions import show_competitions
from streamlit_app.venues import show_venues
from streamlit_app.competitors import show_competitors
from streamlit_app.rankings import show_rankings

# =====================================
# =================CSS=================
st.markdown("""
<style>
:root {
  /* Primary Colors */
  --tennis-green: #00C853;
  --tennis-green-dark: #009624;
  --tennis-green-light: #69f0ae;
  --tennis-yellow: #FFD600;
  --tennis-yellow-dark: #c7a600;
  --tennis-yellow-light: #ffe54e;
  
  /* Dark Theme Colors */
  --bg-primary: #0a0e0f;
  --bg-secondary: #141a1c;
  --bg-card: #1a2225;
  --bg-card-hover: #212c30;
  --bg-glass: rgba(26, 34, 37, 0.85);
  --bg-glass-hover: rgba(26, 34, 37, 0.95);
  
  /* Text Colors */
  --text-primary: #e8f0f2;
  --text-secondary: #a8bdc2;
  --text-muted: #6a848a;
  --text-green: #00C853;
  --text-yellow: #FFD600;
  
  /* Border Colors */
  --border-color: rgba(0, 200, 83, 0.15);
  --border-active: rgba(255, 214, 0, 0.3);
  --border-hover: rgba(0, 200, 83, 0.3);
  
  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);
  --shadow-glow-green: 0 0 30px rgba(0, 200, 83, 0.1);
  --shadow-glow-yellow: 0 0 30px rgba(255, 214, 0, 0.08);
  
  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 48px;
  
  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-xxl: 24px;
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
  --transition-slow: 350ms ease;
}

/* =====================================
   A. APP BACKGROUND
   ===================================== */
.stApp {
  background: radial-gradient(ellipse at 20% 50%, var(--bg-secondary) 0%, var(--bg-primary) 70%);
  font-family: var(--font-family);
  color: var(--text-primary);
}

/* App Container */
.block-container {
  padding: 2rem 2rem 4rem 2rem !important;
  max-width: 1400px !important;
  margin: 0 auto !important;
}

/* Background pattern overlay */
.stApp::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(0, 200, 83, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 90% 80%, rgba(255, 214, 0, 0.02) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* All content above background */
.block-container > * {
  position: relative;
  z-index: 1;
}

/* =====================================
   B. SIDEBAR
   ===================================== */
[data-testid="stSidebar"] {
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  padding: 1.5rem 0.75rem !important;
  min-width: 280px !important;
}

[data-testid="stSidebar"] .sidebar-content {
  background: transparent !important;
}

/* Sidebar Title */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: var(--tennis-green) !important;
  font-weight: 700 !important;
  letter-spacing: -0.5px !important;
  padding-bottom: 0.5rem !important;
  border-bottom: 2px solid var(--border-color) !important;
  margin-bottom: 1.5rem !important;
}

/* Sidebar Navigation Radio */
[data-testid="stSidebar"] .stRadio {
  margin-top: 1.5rem !important;
}

[data-testid="stSidebar"] .stRadio label {
  color: var(--text-secondary) !important;
  font-weight: 500 !important;
  padding: 0.6rem 0.8rem !important;
  border-radius: var(--radius-md) !important;
  transition: all var(--transition-fast) !important;
  cursor: pointer !important;
  width: 100% !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
  background: var(--bg-card) !important;
  color: var(--text-primary) !important;
  transform: translateX(4px) !important;
}

[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
  background: rgba(0, 200, 83, 0.12) !important;
  color: var(--tennis-green) !important;
  border-left: 3px solid var(--tennis-green) !important;
}

/* Sidebar Selectbox */
[data-testid="stSidebar"] .stSelectbox label {
  color: var(--text-secondary) !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
}

/* =====================================
   C. KPI CARDS (METRICS)
   ===================================== */
[data-testid="stMetric"] {
  background: var(--bg-glass) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.25rem 1.5rem !important;
  box-shadow: var(--shadow-sm), var(--shadow-glow-green) !important;
  transition: all var(--transition-normal) !important;
  cursor: default !important;
  height: 100% !important;
  min-height: 120px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
}

[data-testid="stMetric"]:hover {
  transform: translateY(-4px) !important;
  border-color: var(--tennis-green) !important;
  box-shadow: var(--shadow-md), var(--shadow-glow-green) !important;
  background: var(--bg-glass-hover) !important;
}

/* Metric Label */
[data-testid="stMetric"] label {
  color: var(--text-secondary) !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.75px !important;
  margin-bottom: 0.35rem !important;
}

/* Metric Value */
[data-testid="stMetric"] [data-testid="stMetricValue"] {
  color: var(--text-primary) !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  letter-spacing: -0.5px !important;
  line-height: 1.2 !important;
}

/* Metric Delta (if present) */
[data-testid="stMetric"] [data-testid="stMetricDelta"] {
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  margin-top: 0.25rem !important;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] svg {
  fill: var(--tennis-green) !important;
}

/* =====================================
   D. BUTTONS
   ===================================== */
.stButton {
  width: 100% !important;
}

.stButton button {
  background: linear-gradient(135deg, var(--tennis-green), var(--tennis-green-dark)) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  padding: 0.6rem 1.5rem !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.3px !important;
  transition: all var(--transition-normal) !important;
  box-shadow: 0 2px 12px rgba(0, 200, 83, 0.25) !important;
  width: 100% !important;
  cursor: pointer !important;
  position: relative !important;
  overflow: hidden !important;
}

.stButton button::after {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: -100% !important;
  right: 0 !important;
  bottom: 0 !important;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent) !important;
  transition: left var(--transition-slow) !important;
  pointer-events: none !important;
}

.stButton button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 20px rgba(0, 200, 83, 0.4) !important;
}

.stButton button:hover::after {
  left: 100% !important;
}

.stButton button:active {
  transform: translateY(0px) !important;
  box-shadow: 0 2px 8px rgba(0, 200, 83, 0.3) !important;
}

/* Secondary Button Variant */
.stButton button[data-kind="secondary"] {
  background: transparent !important;
  border: 1.5px solid var(--tennis-green) !important;
  color: var(--tennis-green) !important;
  box-shadow: none !important;
}

.stButton button[data-kind="secondary"]:hover {
  background: rgba(0, 200, 83, 0.08) !important;
  box-shadow: var(--shadow-glow-green) !important;
}

/* =====================================
   E. DATA TABLES
   ===================================== */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-lg) !important;
  overflow: hidden !important;
  background: var(--bg-card) !important;
  transition: all var(--transition-normal) !important;
  box-shadow: var(--shadow-sm) !important;
}

[data-testid="stDataFrame"]:hover {
  border-color: var(--border-hover) !important;
  box-shadow: var(--shadow-md), var(--shadow-glow-green) !important;
}

[data-testid="stDataFrame"] table {
  width: 100% !important;
  border-collapse: collapse !important;
}

[data-testid="stDataFrame"] thead {
  background: var(--bg-secondary) !important;
  border-bottom: 2px solid var(--border-color) !important;
}

[data-testid="stDataFrame"] th {
  color: var(--tennis-green) !important;
  font-weight: 600 !important;
  font-size: 0.8rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
  padding: 0.75rem 1rem !important;
  text-align: left !important;
}

[data-testid="stDataFrame"] td {
  color: var(--text-secondary) !important;
  padding: 0.6rem 1rem !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
  font-size: 0.9rem !important;
}

[data-testid="stDataFrame"] tbody tr {
  transition: background var(--transition-fast) !important;
}

[data-testid="stDataFrame"] tbody tr:hover {
  background: var(--bg-card-hover) !important;
}

[data-testid="stDataFrame"] tbody tr:last-child td {
  border-bottom: none !important;
}

/* DataFrame Pagination Controls */
[data-testid="stDataFrame"] .pagination {
  background: var(--bg-secondary) !important;
  padding: 0.5rem 1rem !important;
  border-top: 1px solid var(--border-color) !important;
}

[data-testid="stDataFrame"] .pagination button {
  background: transparent !important;
  color: var(--text-secondary) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-sm) !important;
  padding: 0.25rem 0.75rem !important;
  transition: all var(--transition-fast) !important;
}

[data-testid="stDataFrame"] .pagination button:hover {
  border-color: var(--tennis-green) !important;
  color: var(--tennis-green) !important;
}

/* =====================================
   F. EXPANDERS
   ===================================== */
[data-testid="stExpander"] {
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  background: var(--bg-glass) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  transition: all var(--transition-normal) !important;
  margin-bottom: 0.75rem !important;
  overflow: hidden !important;
}

[data-testid="stExpander"]:hover {
  border-color: var(--border-hover) !important;
  box-shadow: var(--shadow-sm), var(--shadow-glow-green) !important;
}

[data-testid="stExpander"] .stExpanderHeader {
  background: transparent !important;
  color: var(--text-primary) !important;
  font-weight: 600 !important;
  padding: 0.75rem 1rem !important;
  transition: all var(--transition-fast) !important;
  cursor: pointer !important;
}

[data-testid="stExpander"] .stExpanderHeader:hover {
  color: var(--tennis-green) !important;
}

[data-testid="stExpander"] .stExpanderHeader svg {
  fill: var(--tennis-green) !important;
}

[data-testid="stExpander"] .stExpanderContent {
  padding: 0.75rem 1rem 1rem 1rem !important;
  border-top: 1px solid var(--border-color) !important;
  color: var(--text-secondary) !important;
}

/* =====================================
   G. SELECT BOXES
   ===================================== */
.stSelectbox label,
.stMultiSelect label {
  color: var(--text-secondary) !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
  margin-bottom: 0.25rem !important;
}

.stSelectbox .stSelectboxContainer,
.stMultiSelect .stMultiSelectContainer {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  transition: all var(--transition-fast) !important;
}

.stSelectbox .stSelectboxContainer:hover,
.stMultiSelect .stMultiSelectContainer:hover {
  border-color: var(--border-hover) !important;
}

.stSelectbox .stSelectboxContainer:focus-within,
.stMultiSelect .stMultiSelectContainer:focus-within {
  border-color: var(--tennis-green) !important;
  box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.15) !important;
}

/* Selectbox dropdown options */
.stSelectbox .stSelectboxContainer select {
  background: transparent !important;
  color: var(--text-primary) !important;
  padding: 0.5rem 0.75rem !important;
  border: none !important;
}

.stSelectbox .stSelectboxContainer option {
  background: var(--bg-secondary) !important;
  color: var(--text-primary) !important;
  padding: 0.5rem !important;
}

/* MultiSelect tags */
.stMultiSelect .stMultiSelectContainer .stMultiSelectTags {
  background: transparent !important;
}

.stMultiSelect .stMultiSelectContainer .stMultiSelectTags span {
  background: rgba(0, 200, 83, 0.15) !important;
  color: var(--tennis-green) !important;
  border-radius: var(--radius-sm) !important;
  padding: 0.25rem 0.6rem !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
}

.stMultiSelect .stMultiSelectContainer .stMultiSelectTags span svg {
  fill: var(--text-muted) !important;
  transition: fill var(--transition-fast) !important;
  cursor: pointer !important;
}

.stMultiSelect .stMultiSelectContainer .stMultiSelectTags span svg:hover {
  fill: var(--tennis-yellow) !important;
}

/* =====================================
   H. TYPOGRAPHY
   ===================================== */

/* Headings */
h1, h2, h3, h4, h5, h6 {
  color: var(--text-primary) !important;
  font-weight: 700 !important;
  letter-spacing: -0.3px !important;
}

h1 {
  font-size: 2.5rem !important;
  background: linear-gradient(135deg, var(--tennis-green), var(--tennis-yellow)) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  margin-bottom: 1.5rem !important;
}

h2 {
  font-size: 1.8rem !important;
  color: var(--tennis-green) !important;
  border-bottom: 2px solid var(--border-color) !important;
  padding-bottom: 0.5rem !important;
  margin-top: 2rem !important;
  margin-bottom: 1rem !important;
}

h3 {
  font-size: 1.3rem !important;
  color: var(--text-primary) !important;
}

/* Labels and Text */
.stMarkdown p, .stMarkdown li {
  color: var(--text-secondary) !important;
  line-height: 1.6 !important;
}

.stMarkdown strong {
  color: var(--text-primary) !important;
}

/* Code Blocks */
.stCodeBlock {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  font-family: var(--font-mono) !important;
  color: var(--text-secondary) !important;
}

/* Captions */
.caption, .stCaption {
  color: var(--text-muted) !important;
  font-size: 0.8rem !important;
  font-style: italic !important;
}

/* Highlighted Text */
.highlight-green {
  color: var(--tennis-green) !important;
  font-weight: 600 !important;
}

.highlight-yellow {
  color: var(--tennis-yellow) !important;
  font-weight: 600 !important;
}

/* Tennis-themed Dividers */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--tennis-green), var(--tennis-yellow), var(--tennis-green), transparent) !important;
  margin: 2rem 0 !important;
  opacity: 0.3 !important;
}

/* =====================================
   I. RESPONSIVE DESIGN
   ===================================== */

/* Tablet */
@media screen and (max-width: 1024px) {
  .block-container {
    padding: 1.5rem 1.25rem !important;
  }
  
  [data-testid="stMetric"] {
    padding: 1rem 1.25rem !important;
    min-height: 100px !important;
  }
  
  [data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
  }
  
  [data-testid="stSidebar"] {
    min-width: 220px !important;
    padding: 1rem 0.5rem !important;
  }
}

/* Mobile */
@media screen and (max-width: 640px) {
  .block-container {
    padding: 1rem 0.75rem !important;
  }
  
  h1 {
    font-size: 1.8rem !important;
  }
  
  h2 {
    font-size: 1.4rem !important;
  }
  
  [data-testid="stSidebar"] {
    min-width: 100% !important;
    border-right: none !important;
    border-bottom: 1px solid var(--border-color) !important;
    padding: 0.75rem 0.5rem !important;
  }
  
  [data-testid="stMetric"] {
    padding: 0.75rem 1rem !important;
    min-height: 80px !important;
    margin-bottom: 0.5rem !important;
  }
  
  [data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.3rem !important;
  }
  
  [data-testid="stMetric"] label {
    font-size: 0.7rem !important;
  }
  
  [data-testid="stDataFrame"] {
    font-size: 0.8rem !important;
  }
  
  [data-testid="stDataFrame"] th,
  [data-testid="stDataFrame"] td {
    padding: 0.4rem 0.6rem !important;
    font-size: 0.75rem !important;
  }
  
  .stButton button {
    padding: 0.5rem 1rem !important;
    font-size: 0.8rem !important;
  }
  
  [data-testid="stExpander"] .stExpanderHeader {
    font-size: 0.9rem !important;
    padding: 0.5rem 0.75rem !important;
  }
}

/* Small Mobile */
@media screen and (max-width: 400px) {
  .block-container {
    padding: 0.75rem 0.5rem !important;
  }
  
  h1 {
    font-size: 1.5rem !important;
  }
  
  [data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.1rem !important;
  }
}

/* =====================================
   ADDITIONAL UTILITY CLASSES
   ===================================== */

/* Tennis Court Grid Pattern (subtle) */
.tennis-grid {
  background-image: 
    linear-gradient(rgba(0, 200, 83, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 200, 83, 0.02) 1px, transparent 1px) !important;
  background-size: 40px 40px !important;
}

/* Glass Card Utility */
.glass-card {
  background: var(--bg-glass) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.5rem !important;
  box-shadow: var(--shadow-sm) !important;
  transition: all var(--transition-normal) !important;
}

.glass-card:hover {
  border-color: var(--border-hover) !important;
  box-shadow: var(--shadow-md), var(--shadow-glow-green) !important;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 6px !important;
  height: 6px !important;
}

::-webkit-scrollbar-track {
  background: var(--bg-secondary) !important;
}

::-webkit-scrollbar-thumb {
  background: var(--tennis-green) !important;
  border-radius: 3px !important;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--tennis-green-dark) !important;
}

/* Selection */
::selection {
  background: rgba(0, 200, 83, 0.3) !important;
  color: var(--text-primary) !important;
}

/* Loading Spinner Override (if using custom loader) */
.stSpinner > div {
  border-top-color: var(--tennis-green) !important;
}

/* Toast/Message Override */
.stAlert {
  background: var(--bg-glass) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
}

.stAlert svg {
  fill: var(--tennis-green) !important;
}
</style>
""", unsafe_allow_html=True)
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