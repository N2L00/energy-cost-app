import streamlit as st

from database import SessionLocal
from ai_query import get_recommendation

st.set_page_config(page_title="Recommendations", page_icon="💡")
st.title("💡 Cost-Saving Recommendations")

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id

st.write("Get an AI-generated recommendation on how to shift your energy usage to reduce costs.")

if st.button("Generate Recommendation"):
    with st.spinner("Analyzing your energy data..."):
        session = SessionLocal()
        recommendation = get_recommendation(session, business_id)
        session.close()

    st.text(recommendation)