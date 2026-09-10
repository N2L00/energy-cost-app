import streamlit as st

from database import SessionLocal
from crud import get_all_businesses, create_business, get_or_create_default_business

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

session.close()

st.write(f"Currently working with: **{business_names[st.session_state.active_business_id]}**")
st.write("Use the sidebar to log a new entry or view your dashboard.")