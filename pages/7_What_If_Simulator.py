import streamlit as st

from database import SessionLocal
from crud import simulate_savings

st.set_page_config(page_title="What-If Savings Simulator", page_icon="🔮")
st.title("🔮 What-If Savings Simulator")

st.write(
    "Explore hypothetical changes to your energy usage and see the projected "
    "monthly savings, based on your logged cost history."
)

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id

st.subheader("Scenario inputs")

generator_hours_reduction = st.number_input(
    "Run the generator this many fewer hours/day",
    min_value=0.0,
    step=0.5,
)
grid_to_solar_kwh_shift = st.number_input(
    "Shift this many kWh/day from grid to solar",
    min_value=0.0,
    step=0.5,
)

if st.button("Simulate Savings"):
    session = SessionLocal()
    result = simulate_savings(
        session, business_id, generator_hours_reduction, grid_to_solar_kwh_shift
    )
    session.close()

    if not result["possible"]:
        st.warning(
            "Not enough data to calculate this. Make sure you've logged at least one "
            "entry for the sources involved, and that at least one scenario input is "
            "greater than zero."
        )
    else:
        col1, col2 = st.columns(2)
        col1.metric("From fewer generator hours", f"${result['generator_daily_savings'] * 30:,.2f}/mo")
        col2.metric("From shifting grid to solar", f"${result['grid_shift_daily_savings'] * 30:,.2f}/mo")
        st.metric("Total Projected Monthly Savings", f"${result['total_monthly_savings']:,.2f}")
