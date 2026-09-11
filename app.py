import streamlit as st

from database import SessionLocal
from crud import get_all_businesses, create_business, get_or_create_default_business, get_business_by_id, update_exchange_rate, update_budget_threshold

st.set_page_config(page_title="Energy Cost Tracker", page_icon="⚡")

st.title("⚡ Energy Cost Tracker")
st.write("Track and understand your business's energy costs across grid, generator, and solar.")

session = SessionLocal()

if "active_business_id" not in st.session_state:
    default_business = get_or_create_default_business(session)
    st.session_state.active_business_id = default_business.id

businesses = get_all_businesses(session)
business_names = {b.id: b.name for b in businesses}

selected_id = st.selectbox(
    "Active Business",
    options=list(business_names.keys()),
    format_func=lambda biz_id: business_names[biz_id],
    index=list(business_names.keys()).index(st.session_state.active_business_id),
)
st.session_state.active_business_id = selected_id

with st.expander("➕ Add a new business"):
    new_name = st.text_input("Business name")
    if st.button("Create Business"):
        if new_name.strip():
            new_business = create_business(session, new_name.strip())
            st.session_state.active_business_id = new_business.id
            st.rerun()
        else:
            st.warning("Please enter a business name.")

current_business = get_business_by_id(session, st.session_state.active_business_id)

with st.expander("💱 Exchange Rate Settings"):
    st.write(f"Current rate: 1 USD = {current_business.exchange_rate:,.0f} LBP")
    new_rate = st.number_input(
        "Update exchange rate (LBP per 1 USD)",
        min_value=1.0,
        value=float(current_business.exchange_rate),
        step=1.0,
    )
    if st.button("Update Exchange Rate"):
        update_exchange_rate(session, current_business.id, new_rate)
        st.success("Exchange rate updated!")
        st.rerun()

with st.expander("🎯 Monthly Budget Alert"):
    current_threshold = current_business.budget_threshold
    st.write(
        f"Current budget: ${current_threshold:,.2f}" if current_threshold
        else "No budget set."
    )
    new_threshold = st.number_input(
        "Set monthly budget ($)",
        min_value=0.0,
        value=float(current_threshold) if current_threshold else 0.0,
        step=1.0,
    )
    if st.button("Update Budget"):
        update_budget_threshold(session, current_business.id, new_threshold if new_threshold > 0 else None)
        st.success("Budget updated!")
        st.rerun()

session.close()

st.write(f"Currently working with: **{business_names[st.session_state.active_business_id]}**")
st.write("Use the sidebar to log a new entry or view your dashboard.")