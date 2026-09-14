import streamlit as st
import pandas as pd
from database import SessionLocal
from crud import get_entries_dataframe, update_energy_entry, delete_energy_entry, get_cost_per_unit, get_outages_dataframe, get_total_outage_hours, get_current_month_spending, get_baseline_comparison, get_current_month_outage_summary
from models import EnergySource, Currency
from reports import generate_entries_pdf


st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("📊 Energy Cost Dashboard")

session = SessionLocal()

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id
df = get_entries_dataframe(session, business_id)

if df.empty:
    st.info("No entries logged yet. Head to 'Log Entry' to add your first one.")
    session.close()
else:
    total_cost = df["cost_usd"].sum()
    cost_by_source = df.groupby("source")["cost_usd"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cost", f"${total_cost:,.2f}")
    col2.metric("Entries Logged", len(df))
    col3.metric("Sources Used", df["source"].nunique())
    budget_info = get_current_month_spending(session, business_id)
    if budget_info["threshold"] is not None:
        if budget_info["over_budget"]:
            st.error(
                f"⚠️ Over budget: spent ${budget_info['spent']:,.2f} this month, "
                f"budget is ${budget_info['threshold']:,.2f}"
            )
        else:
            remaining = budget_info["threshold"] - budget_info["spent"]
            st.success(
                f"✅ On track: ${budget_info['spent']:,.2f} spent this month, "
                f"${remaining:,.2f} remaining of your ${budget_info['threshold']:,.2f} budget"
            )
    total_outage_hours = get_total_outage_hours(session, business_id)
    st.metric("Total Outage Hours", f"{total_outage_hours:.1f}")
    outage_summary = get_current_month_outage_summary(session, business_id)
    if outage_summary["scheduled_hours"] > 0:
        sched_col, logged_col = st.columns(2)
        sched_col.metric("Scheduled Outage Hours (this month)", f"{outage_summary['scheduled_hours']:.1f}")
        logged_col.metric("Manually Logged (this month)", f"{outage_summary['manually_logged_hours']:.1f}")
        st.caption(
            "These are shown separately and never added together, since a scheduled estimate "
            "and a specific logged outage may overlap on the same day."
        )


    st.subheader("Cost Efficiency by Source")
    cost_per_unit = get_cost_per_unit(session, business_id)
    eff_col1, eff_col2, eff_col3 = st.columns(3)
    for col, source in zip([eff_col1, eff_col2, eff_col3], ["grid", "generator", "solar"]):
        data = cost_per_unit[source]
        if data["value"] is not None:
            col.metric(f"{source.capitalize()} — {data['metric']}", f"${data['value']:.3f}")
        else:
            col.metric(f"{source.capitalize()} — {data['metric']}", "No data")

    st.subheader("How Your Grid Rate Compares")
    baseline = get_baseline_comparison(session, business_id)
    grid_baseline = baseline.get("grid")
    if grid_baseline and grid_baseline["value"] is not None:
        status = grid_baseline["status"]
        note = grid_baseline["baseline"]["note"]
        if status == "above typical":
            st.warning(f"Your grid rate (\\${grid_baseline['value']:.3f}/kWh) is above the typical range. Reference: {note}")
        elif status == "below typical":
            st.info(f"Your grid rate (\\${grid_baseline['value']:.3f}/kWh) is below the typical range. Reference: {note}")
        else:
            st.success(f"Your grid rate (\\${grid_baseline['value']:.3f}/kWh) is within the typical range. Reference: {note}")

    st.subheader("Cost by Source")
    st.bar_chart(cost_by_source)

    st.subheader("Cost Over Time")
    cost_by_date = df.groupby("date")["cost_usd"].sum()
    st.line_chart(cost_by_date)

    st.subheader("Outage Hours vs. Generator Cost")
    outages_df = get_outages_dataframe(session, business_id)
    generator_df = df[df["source"] == "generator"]

    if outages_df.empty or generator_df.empty:
        st.info("Log both outages and generator entries to see this comparison.")
    else:
        outage_by_date = outages_df.groupby("date")["hours_down"].sum()
        generator_cost_by_date = generator_df.groupby("date")["cost_usd"].sum()

        comparison_df = pd.DataFrame({
            "Outage Hours": outage_by_date,
            "Generator Cost": generator_cost_by_date,
        }).fillna(0)

        st.line_chart(comparison_df)

    st.subheader("All Entries")
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "Download CSV",
        data=df.to_csv(index=False),
        file_name="energy_entries.csv",
        mime="text/csv",
    
    )
    st.download_button(
        "Download PDF Report",
        data=generate_entries_pdf(df),
        file_name="energy_report.pdf",
        mime="application/pdf",
    )

    st.subheader("Edit or Delete an Entry")

    entry_options = {
        row["id"]: f"{row['date']} - {row['source']} - ${row['cost']:.2f}"
        for _, row in df.iterrows()
    }
    selected_entry_id = st.selectbox(
        "Select an entry",
        options=list(entry_options.keys()),
        format_func=lambda eid: entry_options[eid],
    )

    selected_row = df[df["id"] == selected_entry_id].iloc[0]

    edit_source = st.selectbox(
        "Energy Source",
        options=[s.value for s in EnergySource],
        index=[s.value for s in EnergySource].index(selected_row["source"]),
    )
    edit_date = st.date_input("Date", value=selected_row["date"])
    edit_currency = st.selectbox(
        "Currency",
        options=["USD", "LBP"],
        index=["USD", "LBP"].index(selected_row["currency"]),
    )
    edit_cost = st.number_input("Cost", min_value=0.0, step=0.5, value=float(selected_row["cost"]))

    edit_units_kwh = None
    edit_diesel_liters = None
    edit_hours_run = None

    if edit_source in ("grid", "solar"):
        edit_units_kwh = st.number_input(
            "Units Consumed (kWh)", min_value=0.0, step=1.0,
            value=float(selected_row["units_kwh"]) if selected_row["units_kwh"] else 0.0,
        )

    if edit_source == "generator":
        edit_diesel_liters = st.number_input(
            "Diesel Used (liters)", min_value=0.0, step=1.0,
            value=float(selected_row["diesel_liters"]) if selected_row["diesel_liters"] else 0.0,
        )
        edit_hours_run = st.number_input(
            "Hours Run", min_value=0.0, step=0.5,
            value=float(selected_row["hours_run"]) if selected_row["hours_run"] else 0.0,
        )

    edit_notes = st.text_area("Notes (optional)", value=selected_row["notes"] or "")

    col_update, col_delete = st.columns(2)

    with col_update:
        if st.button("Update Entry"):
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
            )
            st.success("Entry updated!")
            st.rerun()

    with col_delete:
        if st.button("Delete Entry", type="primary"):
            st.session_state.confirm_delete_id = selected_entry_id

    if st.session_state.get("confirm_delete_id") == selected_entry_id:
        st.warning("Are you sure you want to delete this entry? This cannot be undone.")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Yes, delete it"):
                delete_energy_entry(session, selected_entry_id)
                del st.session_state.confirm_delete_id
                st.success("Entry deleted!")
                st.rerun()
        with col_no:
            if st.button("Cancel"):
                del st.session_state.confirm_delete_id
                st.rerun()

    session.close()