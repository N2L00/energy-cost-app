import streamlit as st

from database import SessionLocal
from crud import calculate_solar_payback, panels_to_kwh_per_day, SOLAR_PANEL_ASSUMPTIONS

st.set_page_config(page_title="Solar Payback Calculator", page_icon="☀️")
st.title("☀️ Solar Payback Calculator")

st.write(
    "Estimate how many months it would take for additional solar capacity "
    "to pay for itself, based on your current grid cost per kWh."
)

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id

upfront_cost = st.number_input("Upfront cost of new solar capacity ($)", min_value=0.0, step=50.0)

input_method = st.radio("How do you want to estimate output?", ["Number of panels", "I know the kWh/day"])

if input_method == "Number of panels":
    num_panels = st.number_input("Number of new panels", min_value=0.0, step=1.0)
    extra_kwh_per_day = panels_to_kwh_per_day(num_panels)
    st.caption(
        f"Estimated at {extra_kwh_per_day} kWh/day, assuming {SOLAR_PANEL_ASSUMPTIONS['panel_watts']}W panels, "
        f"{SOLAR_PANEL_ASSUMPTIONS['peak_sun_hours']} peak sun hours/day, "
        f"{SOLAR_PANEL_ASSUMPTIONS['efficiency']*100:.0f}% real-world efficiency."
    )
else:
    extra_kwh_per_day = st.number_input("Additional kWh per day this would produce", min_value=0.0, step=0.5)
if st.button("Calculate Payback"):
    session = SessionLocal()
    result = calculate_solar_payback(session, business_id, upfront_cost, extra_kwh_per_day)
    session.close()

    if not result["possible"]:
        st.warning(
            "Not enough data to calculate this. Make sure you've logged at least one "
            "grid entry, and that additional kWh per day is greater than zero."
        )
    else:
        st.metric("Estimated Monthly Savings", f"${result['monthly_savings']:,.2f}")
        st.metric("Payback Period", f"{result['months_to_payback']:.1f} months")