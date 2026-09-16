import streamlit as st
import pandas as pd
from datetime import date

from database import SessionLocal
from crud import get_entries_dataframe, update_energy_entry, delete_energy_entry, get_cost_per_unit, get_outages_dataframe, get_total_outage_hours, get_current_month_spending, get_baseline_comparison, get_current_month_outage_summary, get_business_language, get_current_month_source_summaries, get_business_by_id
from models import EnergySource, Currency
from reports import generate_entries_pdf
from summary_card import generate_summary_card
from translations import t, month_name

session = SessionLocal()

if "active_business_id" not in st.session_state:
    st.warning(t("no_business_warning", "en"))
    st.stop()

business_id = st.session_state.active_business_id
language = get_business_language(session, business_id)

st.title(t("dashboard_title", language))

df = get_entries_dataframe(session, business_id)

if df.empty:
    st.info(t("no_entries_info", language))
    session.close()
else:
    total_cost = df["cost_usd"].sum()
    cost_by_source = df.groupby("source")["cost_usd"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric(t("total_cost_metric", language), f"${total_cost:,.2f}")
    col2.metric(t("entries_logged_metric", language), len(df))
    col3.metric(t("sources_used_metric", language), df["source"].nunique())
    budget_info = get_current_month_spending(session, business_id)
    if budget_info["threshold"] is not None:
        if budget_info["over_budget"]:
            st.error(
                t(
                    "over_budget_error", language,
                    spent=f"{budget_info['spent']:,.2f}",
                    threshold=f"{budget_info['threshold']:,.2f}",
                )
            )
        else:
            remaining = budget_info["threshold"] - budget_info["spent"]
            st.success(
                t(
                    "on_track_success", language,
                    spent=f"{budget_info['spent']:,.2f}",
                    remaining=f"{remaining:,.2f}",
                    threshold=f"{budget_info['threshold']:,.2f}",
                )
            )
    total_outage_hours = get_total_outage_hours(session, business_id)
    st.metric(t("total_outage_hours_metric", language), f"{total_outage_hours:.1f}")

    outage_summary = get_current_month_outage_summary(session, business_id)
    if outage_summary["scheduled_hours"] > 0:
        sched_col, logged_col = st.columns(2)
        sched_col.metric(t("scheduled_outage_hours_metric", language), f"{outage_summary['scheduled_hours']:.1f}")
        logged_col.metric(t("manually_logged_metric", language), f"{outage_summary['manually_logged_hours']:.1f}")
        st.caption(t("outage_overlap_caption", language))

    st.subheader(t("cost_efficiency_header", language))
    cost_per_unit = get_cost_per_unit(session, business_id)
    eff_col1, eff_col2, eff_col3 = st.columns(3)
    for col, source in zip([eff_col1, eff_col2, eff_col3], ["grid", "generator", "solar"]):
        data = cost_per_unit[source]
        metric_key = "cost_per_kwh_metric" if data["metric"] == "cost per kWh" else "cost_per_hour_metric"
        label = f"{t(f'source_{source}', language)} — {t(metric_key, language)}"
        if data["value"] is not None:
            col.metric(label, f"${data['value']:.3f}")
        else:
            col.metric(label, t("no_data_label", language))

    st.subheader(t("grid_rate_header", language))
    baseline = get_baseline_comparison(session, business_id)
    grid_baseline = baseline.get("grid")
    if grid_baseline and grid_baseline["value"] is not None:
        status = grid_baseline["status"]
        note = grid_baseline["baseline"]["note"]
        value_str = f"{grid_baseline['value']:.3f}"
        if status == "above typical":
            st.warning(t("grid_rate_above", language, value=value_str, note=note))
        elif status == "below typical":
            st.info(t("grid_rate_below", language, value=value_str, note=note))
        else:
            st.success(t("grid_rate_within", language, value=value_str, note=note))

    st.subheader(t("cost_by_source_header", language))
    st.bar_chart(cost_by_source)

    st.subheader(t("cost_over_time_header", language))
    cost_by_date = df.groupby("date")["cost_usd"].sum()
    st.line_chart(cost_by_date)

    st.subheader(t("outage_vs_generator_header", language))
    outages_df = get_outages_dataframe(session, business_id)
    generator_df = df[df["source"] == "generator"]

    if outages_df.empty or generator_df.empty:
        st.info(t("log_both_info", language))
    else:
        outage_by_date = outages_df.groupby("date")["hours_down"].sum()
        generator_cost_by_date = generator_df.groupby("date")["cost_usd"].sum()

        comparison_df = pd.DataFrame({
            t("outage_hours_series", language): outage_by_date,
            t("generator_cost_series", language): generator_cost_by_date,
        }).fillna(0)

        st.line_chart(comparison_df)

    st.subheader(t("all_entries_header", language))
    st.dataframe(df, use_container_width=True)
    st.download_button(
        t("download_csv_button", language),
        data=df.to_csv(index=False),
        file_name="energy_entries.csv",
        mime="text/csv",
    )
    st.download_button(
        t("download_pdf_button", language),
        data=generate_entries_pdf(df),
        file_name="energy_report.pdf",
        mime="application/pdf",
    )

    today = date.today()
    current_business = get_business_by_id(session, business_id)
    source_summaries = get_current_month_source_summaries(session, business_id)
    source_totals = {source: data["total_cost"] for source, data in source_summaries.items()}
    summary_card_bytes = generate_summary_card(
        business_name=current_business.name,
        month_label=f"{month_name(today.month, language)} {today.year}",
        total_cost=budget_info["spent"],
        source_totals=source_totals,
        language=language,
    )
    st.download_button(
        t("download_summary_card_button", language),
        data=summary_card_bytes,
        file_name="energy_summary_card.png",
        mime="image/png",
    )

    st.subheader(t("edit_delete_header", language))

    entry_options = {
        row["id"]: f"{row['date']} - {row['source']} - ${row['cost']:.2f}"
        for _, row in df.iterrows()
    }
    selected_entry_id = st.selectbox(
        t("select_entry_label", language),
        options=list(entry_options.keys()),
        format_func=lambda eid: entry_options[eid],
    )

    selected_row = df[df["id"] == selected_entry_id].iloc[0]

    source_options = [s.value for s in EnergySource]
    edit_source = st.selectbox(
        t("energy_source_label", language),
        options=source_options,
        index=source_options.index(selected_row["source"]),
        format_func=lambda s: t(f"source_{s}", language),
    )
    edit_date = st.date_input(t("date_label", language), value=selected_row["date"])
    edit_currency = st.selectbox(
        t("currency_label", language),
        options=["USD", "LBP"],
        index=["USD", "LBP"].index(selected_row["currency"]),
    )
    edit_cost = st.number_input(t("cost_label", language), min_value=0.0, step=0.5, value=float(selected_row["cost"]))

    edit_units_kwh = None
    edit_diesel_liters = None
    edit_hours_run = None

    if edit_source in ("grid", "solar"):
        edit_units_kwh = st.number_input(
            t("units_kwh_label", language), min_value=0.0, step=1.0,
            value=float(selected_row["units_kwh"]) if selected_row["units_kwh"] else 0.0,
        )

    if edit_source == "generator":
        edit_diesel_liters = st.number_input(
            t("diesel_liters_label", language), min_value=0.0, step=1.0,
            value=float(selected_row["diesel_liters"]) if selected_row["diesel_liters"] else 0.0,
        )
        edit_hours_run = st.number_input(
            t("hours_run_label", language), min_value=0.0, step=0.5,
            value=float(selected_row["hours_run"]) if selected_row["hours_run"] else 0.0,
        )

    edit_time_of_day = None
    if edit_source in ("grid", "generator"):
        time_options = ["morning", "afternoon", "evening_night"]
        current_time = selected_row.get("time_of_day")
        default_index = time_options.index(current_time) if current_time in time_options else 0
        edit_time_of_day = st.selectbox(
            t("time_of_day_label", language),
            options=time_options,
            index=default_index,
            format_func=lambda tod: t(f"time_of_day_{tod}", language),
        )

    edit_notes = st.text_area(t("notes_label", language), value=selected_row["notes"] or "")

    col_update, col_delete = st.columns(2)

    with col_update:
        if st.button(t("update_entry_button", language)):
            update_energy_entry(
                session=session,
                entry_id=selected_entry_id,
                entry_date=edit_date,
                source=EnergySource(edit_source),
                cost=edit_cost,
                currency=Currency(edit_currency),
                units_kwh=edit_units_kwh,
                diesel_liters=edit_diesel_liters,
                hours_run=edit_hours_run,
                notes=edit_notes if edit_notes else None,
                time_of_day=edit_time_of_day,
            )
            st.success(t("entry_updated_success", language))
            st.rerun()

    with col_delete:
        if st.button(t("delete_entry_button", language), type="primary"):
            st.session_state.confirm_delete_id = selected_entry_id

    if st.session_state.get("confirm_delete_id") == selected_entry_id:
        st.warning(t("confirm_delete_entry_warning", language))
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button(t("yes_delete_it", language)):
                delete_energy_entry(session, selected_entry_id)
                del st.session_state.confirm_delete_id
                st.success(t("entry_deleted_success", language))
                st.rerun()
        with col_no:
            if st.button(t("cancel_button", language)):
                del st.session_state.confirm_delete_id
                st.rerun()

    session.close()
