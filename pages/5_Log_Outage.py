import streamlit as st
from datetime import date

from database import SessionLocal
from crud import log_outage, get_outages_dataframe, get_total_outage_hours

st.set_page_config(page_title="Log Outage", page_icon="🔌")
st.title("🔌 Log Grid Outage")

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id
session = SessionLocal()

outage_date = st.date_input("Date")
hours_down = st.number_input("Hours without grid power", min_value=0.0, max_value=24.0, step=0.5)
notes = st.text_area("Notes (optional)")

if st.button("Log Outage"):
    log_outage(session, business_id, outage_date, hours_down, notes if notes else None)
    st.success("Outage logged!")
    st.rerun()

st.subheader("Outage History")
df = get_outages_dataframe(session, business_id)

if df.empty:
    st.info("No outages logged yet.")
else:
    total_hours = get_total_outage_hours(session, business_id)
    st.metric("Total Outage Hours", f"{total_hours:.1f}")
    st.dataframe(df, use_container_width=True)

session.close()