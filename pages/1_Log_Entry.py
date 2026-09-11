import streamlit as st

from database import SessionLocal
from models import EnergySource, Currency
from crud import create_energy_entry

st.set_page_config(page_title="Log Entry", page_icon="📝")
st.title("📝 Log Energy Entry")

session = SessionLocal()

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id

source = st.selectbox(
    "Energy Source",
    options=[s.value for s in EnergySource],
)

entry_date = st.date_input("Date")
currency = st.selectbox("Currency", options=["USD", "LBP"])
cost = st.number_input("Cost", min_value=0.0, step=0.5)

units_kwh = None
diesel_liters = None
hours_run = None

if source in ("grid", "solar"):
    units_kwh = st.number_input("Units Consumed (kWh)", min_value=0.0, step=1.0)

if source == "generator":
    diesel_liters = st.number_input("Diesel Used (liters)", min_value=0.0, step=1.0)
    hours_run = st.number_input("Hours Run", min_value=0.0, step=0.5)

notes = st.text_area("Notes (optional)")

if st.button("Save Entry"):
    create_energy_entry(
        session=session,
        business_id=business_id,
        entry_date=entry_date,
        source=EnergySource(source),
        cost=cost,
        currency=Currency(currency),
        units_kwh=units_kwh,
        diesel_liters=diesel_liters,
        hours_run=hours_run,
        notes=notes if notes else None,
    )
    st.success("Entry saved!")

session.close()