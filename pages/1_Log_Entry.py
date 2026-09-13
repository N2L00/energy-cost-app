import streamlit as st
import pandas as pd

from database import SessionLocal
from models import EnergySource, Currency
from crud import create_energy_entry

st.set_page_config(page_title="Log Entry", page_icon="📝")
st.title("📝 Log Energy Entry")

session = SessionLocal()

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id

source = st.selectbox(
    "Energy Source",
    options=[s.value for s in EnergySource],
)

entry_date = st.date_input("Date")
currency = st.selectbox("Currency", options=["USD", "LBP"])
cost = st.number_input("Cost", min_value=0.0, step=0.5)

units_kwh = None
diesel_liters = None
hours_run = None

if source in ("grid", "solar"):
    units_kwh = st.number_input("Units Consumed (kWh)", min_value=0.0, step=1.0)

if source == "generator":
    diesel_liters = st.number_input("Diesel Used (liters)", min_value=0.0, step=1.0)
    hours_run = st.number_input("Hours Run", min_value=0.0, step=0.5)

notes = st.text_area("Notes (optional)")

if st.button("Save Entry"):
    create_energy_entry(
        session=session,
        business_id=business_id,
        entry_date=entry_date,
        source=EnergySource(source),
        cost=cost,
        currency=Currency(currency),
        units_kwh=units_kwh,
        diesel_liters=diesel_liters,
        hours_run=hours_run,
        notes=notes if notes else None,
    )
    st.success("Entry saved!")

st.divider()
st.subheader("Import Entries from CSV")
st.caption(
    "Columns: date (YYYY-MM-DD), source (grid/generator/solar), "
    "currency (USD/LBP, optional, default USD), cost, units_kwh (optional), "
    "diesel_liters (optional), hours_run (optional), notes (optional)"
)

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        import_df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        import_df = None

    if import_df is not None:
        st.write("Preview:")
        st.dataframe(import_df, use_container_width=True)

        if st.button("Import Entries"):
            valid_sources = {s.value for s in EnergySource}
            valid_currencies = {c.value for c in Currency}

            def optional_float(row, col):
                val = row.get(col)
                if val is None or pd.isna(val):
                    return None
                try:
                    return float(val)
                except (TypeError, ValueError):
                    return None

            imported = 0
            skipped = []

            for idx, row in import_df.iterrows():
                row_num = idx + 2  # +1 for header row, +1 for 1-indexing

                raw_date = row.get("date")
                raw_source = row.get("source")
                raw_cost = row.get("cost")

                if pd.isna(raw_date) or pd.isna(raw_source) or pd.isna(raw_cost):
                    skipped.append((row_num, "missing required field (date, source, or cost)"))
                    continue

                parsed_date = pd.to_datetime(raw_date, format="%Y-%m-%d", errors="coerce")
                if pd.isna(parsed_date):
                    skipped.append((row_num, f"invalid date: {raw_date}"))
                    continue

                source_value = str(raw_source).strip().lower()
                if source_value not in valid_sources:
                    skipped.append((row_num, f"unrecognized source: {raw_source}"))
                    continue

                raw_currency = row.get("currency")
                if raw_currency is None or pd.isna(raw_currency) or str(raw_currency).strip() == "":
                    currency_value = "USD"
                else:
                    currency_value = str(raw_currency).strip().upper()
                    if currency_value not in valid_currencies:
                        skipped.append((row_num, f"unrecognized currency: {raw_currency}"))
                        continue

                try:
                    cost_value = float(raw_cost)
                except (TypeError, ValueError):
                    skipped.append((row_num, f"invalid cost: {raw_cost}"))
                    continue

                raw_notes = row.get("notes")
                notes_value = None if raw_notes is None or pd.isna(raw_notes) else str(raw_notes)

                result = create_energy_entry(
                    session=session,
                    business_id=business_id,
                    entry_date=parsed_date.date(),
                    source=EnergySource(source_value),
                    cost=cost_value,
                    currency=Currency(currency_value),
                    units_kwh=optional_float(row, "units_kwh"),
                    diesel_liters=optional_float(row, "diesel_liters"),
                    hours_run=optional_float(row, "hours_run"),
                    notes=notes_value,
                )
                if result is not None:
                    imported += 1
                else:
                    skipped.append((row_num, "database error while saving"))
            st.success(f"Imported {imported} of {len(import_df)} row(s).")
            if skipped:
                st.warning(f"Skipped {len(skipped)} row(s):")
                st.dataframe(
                    pd.DataFrame(skipped, columns=["Row", "Reason"]),
                    use_container_width=True,
                )

session.close()