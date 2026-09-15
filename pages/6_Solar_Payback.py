import streamlit as st

from database import SessionLocal
from crud import calculate_solar_payback, panels_to_kwh_per_day, SOLAR_PANEL_ASSUMPTIONS, get_business_language
from translations import t

if "active_business_id" not in st.session_state:
    st.warning(t("no_business_warning", "en"))
    st.stop()

business_id = st.session_state.active_business_id

lang_session = SessionLocal()
language = get_business_language(lang_session, business_id)
lang_session.close()

st.title(t("solar_payback_title", language))

st.write(t("solar_payback_intro", language))

upfront_cost = st.number_input(t("upfront_cost_label", language), min_value=0.0, step=50.0)

panels_option = t("estimate_method_panels", language)
kwh_option = t("estimate_method_kwh", language)
input_method = st.radio(t("estimate_method_label", language), [panels_option, kwh_option])

if input_method == panels_option:
    num_panels = st.number_input(t("num_panels_label", language), min_value=0.0, step=1.0)
    extra_kwh_per_day = panels_to_kwh_per_day(num_panels)
    st.caption(
        t(
            "panel_estimate_caption", language,
            kwh=extra_kwh_per_day,
            watts=SOLAR_PANEL_ASSUMPTIONS["panel_watts"],
            sun_hours=SOLAR_PANEL_ASSUMPTIONS["peak_sun_hours"],
            efficiency=f"{SOLAR_PANEL_ASSUMPTIONS['efficiency']*100:.0f}",
        )
    )
else:
    extra_kwh_per_day = st.number_input(t("extra_kwh_label", language), min_value=0.0, step=0.5)

if st.button(t("calculate_payback_button", language)):
    session = SessionLocal()
    result = calculate_solar_payback(session, business_id, upfront_cost, extra_kwh_per_day)
    session.close()

    if not result["possible"]:
        st.warning(t("payback_not_possible_warning", language))
    else:
        st.metric(t("estimated_monthly_savings_metric", language), f"${result['monthly_savings']:,.2f}")
        st.metric(t("payback_period_metric", language), t("months_suffix_value", language, months=f"{result['months_to_payback']:.1f}"))
