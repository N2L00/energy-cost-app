import streamlit as st

from database import SessionLocal
from crud import get_or_create_default_business, get_business_language
from translations import t

session = SessionLocal()

if "active_business_id" not in st.session_state:
    default_business = get_or_create_default_business(session)
    st.session_state.active_business_id = default_business.id

language = get_business_language(session, st.session_state.active_business_id)
session.close()

st.set_page_config(page_title=t("app_title", language), page_icon="⚡")

pages = [
    st.Page("home.py", title=t("nav_home", language), icon="⚡", default=True),
    st.Page("pages/1_Log_Entry.py", title=t("nav_log_entry", language), icon="📝"),
    st.Page("pages/2_Dashboard.py", title=t("nav_dashboard", language), icon="📊"),
    st.Page("pages/3_Ask_AI.py", title=t("nav_ask_ai", language), icon="🤖"),
    st.Page("pages/4_Recommendations.py", title=t("nav_recommendations", language), icon="💡"),
    st.Page("pages/5_Log_Outage.py", title=t("nav_log_outage", language), icon="🔌"),
    st.Page("pages/6_Solar_Payback.py", title=t("nav_solar_payback", language), icon="☀️"),
    st.Page("pages/7_What_If_Simulator.py", title=t("nav_whatif", language), icon="🔮"),
]

pg = st.navigation(pages)
pg.run()
