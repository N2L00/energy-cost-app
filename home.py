import streamlit as st

from database import SessionLocal
from crud import get_all_businesses, create_business, get_business_by_id, update_exchange_rate, update_budget_threshold, delete_business, get_outage_schedule, set_outage_schedule, get_business_language, update_business_language, update_generator_capacity
from translations import t, LANGUAGE_NAMES

session = SessionLocal()

language = get_business_language(session, st.session_state.active_business_id)

st.title(t("app_title", language))
st.write(t("app_subtitle", language))

businesses = get_all_businesses(session)
business_names = {b.id: b.name for b in businesses}

selected_id = st.selectbox(
    t("active_business_label", language),
    options=list(business_names.keys()),
    format_func=lambda biz_id: business_names[biz_id],
    index=list(business_names.keys()).index(st.session_state.active_business_id),
)
st.session_state.active_business_id = selected_id

with st.expander(t("add_business_expander", language)):
    new_name = st.text_input(t("business_name_label", language))
    if st.button(t("create_business_button", language)):
        if new_name.strip():
            new_business = create_business(session, new_name.strip())
            st.session_state.active_business_id = new_business.id
            st.rerun()
        else:
            st.warning(t("enter_business_name_warning", language))

current_business = get_business_by_id(session, st.session_state.active_business_id)

with st.expander(t("exchange_rate_expander", language)):
    st.write(t("current_rate_text", language, rate=f"{current_business.exchange_rate:,.0f}"))
    new_rate = st.number_input(
        t("update_exchange_rate_label", language),
        min_value=1.0,
        value=float(current_business.exchange_rate),
        step=1.0,
    )
    if st.button(t("update_exchange_rate_button", language)):
        update_exchange_rate(session, current_business.id, new_rate)
        st.success(t("exchange_rate_updated_success", language))
        st.rerun()

with st.expander(t("budget_expander", language)):
    current_threshold = current_business.budget_threshold
    st.write(
        t("current_budget_text", language, threshold=f"{current_threshold:,.2f}") if current_threshold
        else t("no_budget_set", language)
    )
    new_threshold = st.number_input(
        t("set_budget_label", language),
        min_value=0.0,
        value=float(current_threshold) if current_threshold else 0.0,
        step=1.0,
    )
    if st.button(t("update_budget_button", language)):
        update_budget_threshold(session, current_business.id, new_threshold if new_threshold > 0 else None)
        st.success(t("budget_updated_success", language))
        st.rerun()

with st.expander(t("outage_schedule_expander", language)):
    st.write(t("outage_schedule_description", language))
    current_schedule = get_outage_schedule(session, current_business.id)
    current_hours = current_schedule.hours_per_day if current_schedule else 0.0
    st.write(
        t("current_schedule_text", language, hours=current_hours) if current_schedule
        else t("no_schedule_set", language)
    )
    new_hours = st.number_input(
        t("typical_outage_hours_label", language),
        min_value=0.0,
        max_value=24.0,
        value=float(current_hours),
        step=0.5,
    )
    if st.button(t("update_schedule_button", language)):
        set_outage_schedule(session, current_business.id, new_hours)
        st.success(t("schedule_updated_success", language))
        st.rerun()

with st.expander(t("generator_capacity_expander", language)):
    st.write(t("generator_capacity_description", language))
    current_capacity = current_business.generator_capacity_kva
    st.write(
        t("current_generator_capacity_text", language, capacity=f"{current_capacity:,.1f}") if current_capacity
        else t("no_generator_capacity_set", language)
    )
    new_capacity = st.number_input(
        t("set_generator_capacity_label", language),
        min_value=0.0,
        value=float(current_capacity) if current_capacity else 0.0,
        step=1.0,
    )
    if st.button(t("update_generator_capacity_button", language)):
        update_generator_capacity(session, current_business.id, new_capacity if new_capacity > 0 else None)
        st.success(t("generator_capacity_updated_success", language))
        st.rerun()

with st.expander(t("language_expander", language)):
    language_options = list(LANGUAGE_NAMES.keys())
    new_language = st.selectbox(
        t("language_select_label", language),
        options=language_options,
        format_func=lambda code: LANGUAGE_NAMES[code],
        index=language_options.index(language) if language in language_options else 0,
    )
    if st.button(t("update_language_button", language)):
        update_business_language(session, current_business.id, new_language)
        st.success(t("language_updated_success", new_language))
        st.rerun()

with st.expander(t("delete_business_expander", language)):
    st.warning(t("delete_business_warning", language))
    if st.button(t("delete_business_button", language)):
        st.session_state.confirm_delete_business_id = current_business.id

    if st.session_state.get("confirm_delete_business_id") == current_business.id:
        st.error(t("confirm_delete_business_text", language, name=current_business.name))
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button(t("confirm_delete_yes", language)):
                delete_business(session, current_business.id)
                del st.session_state.confirm_delete_business_id
                del st.session_state.active_business_id
                st.success(t("business_deleted_success", language))
                st.rerun()
        with col_no:
            if st.button(t("cancel_button", language), key="cancel_delete_business"):
                del st.session_state.confirm_delete_business_id
                st.rerun()

session.close()

st.write(t("currently_working_with", language, name=business_names[st.session_state.active_business_id]))
st.write(t("use_sidebar_hint", language))
