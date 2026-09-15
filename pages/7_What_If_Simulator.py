import streamlit as st

from database import SessionLocal
from crud import simulate_savings, get_business_language
from translations import t

if "active_business_id" not in st.session_state:
    st.warning(t("no_business_warning", "en"))
    st.stop()

business_id = st.session_state.active_business_id

lang_session = SessionLocal()
language = get_business_language(lang_session, business_id)
lang_session.close()

st.title(t("whatif_title", language))

st.write(t("whatif_intro", language))

st.subheader(t("scenario_inputs_header", language))

generator_hours_reduction = st.number_input(
    t("generator_hours_reduction_label", language),
    min_value=0.0,
    step=0.5,
)
grid_to_solar_kwh_shift = st.number_input(
    t("grid_to_solar_shift_label", language),
    min_value=0.0,
    step=0.5,
)

if st.button(t("simulate_savings_button", language)):
    session = SessionLocal()
    result = simulate_savings(
        session, business_id, generator_hours_reduction, grid_to_solar_kwh_shift
    )
    session.close()

    if not result["possible"]:
        st.warning(t("simulation_not_possible_warning", language))
    else:
        col1, col2 = st.columns(2)
        col1.metric(
            t("generator_hours_savings_metric", language),
            t("amount_per_month_value", language, amount=f"{result['generator_daily_savings'] * 30:,.2f}"),
        )
        col2.metric(
            t("grid_shift_savings_metric", language),
            t("amount_per_month_value", language, amount=f"{result['grid_shift_daily_savings'] * 30:,.2f}"),
        )
        st.metric(t("total_projected_savings_metric", language), f"${result['total_monthly_savings']:,.2f}")
