import streamlit as st

from database import SessionLocal
from crud import get_entries_dataframe

st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("📊 Energy Cost Dashboard")

session = SessionLocal()

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id
df = get_entries_dataframe(session, business_id)
session.close()

if df.empty:
    st.info("No entries logged yet. Head to 'Log Entry' to add your first one.")
else:
    total_cost = df["cost"].sum()
    cost_by_source = df.groupby("source")["cost"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cost", f"${total_cost:,.2f}")
    col2.metric("Entries Logged", len(df))
    col3.metric("Sources Used", df["source"].nunique())

    st.subheader("Cost by Source")