import streamlit as st
from datetime import date

from database import SessionLocal
from crud import log_outage, get_outages_dataframe, get_total_outage_hours, get_business_language
from translations import t

if "active_business_id" not in st.session_state:
    st.warning(t("no_business_warning", "en"))
    st.stop()

business_id = st.session_state.active_business_id
session = SessionLocal()
language = get_business_language(session, business_id)

st.title(t("log_outage_title", language))

outage_date = st.date_input(t("date_label", language))
hours_down = st.number_input(t("hours_without_power_label", language), min_value=0.0, max_value=24.0, step=0.5)
notes = st.text_area(t("notes_label", language))

if st.button(t("log_outage_button", language)):
    log_outage(session, business_id, outage_date, hours_down, notes if notes else None)
    st.success(t("outage_logged_success", language))
    st.rerun()

st.subheader(t("outage_history_header", language))
df = get_outages_dataframe(session, business_id)

if df.empty:
    st.info(t("no_outages_info", language))
else:
    total_hours = get_total_outage_hours(session, business_id)
    st.metric(t("total_outage_hours_metric", language), f"{total_hours:.1f}")
    st.dataframe(df, use_container_width=True)

session.close()
