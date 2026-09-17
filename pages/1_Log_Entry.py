import streamlit as st
import pandas as pd

from database import SessionLocal
from models import EnergySource, Currency
from crud import create_energy_entry, get_business_language
from translations import t

session = SessionLocal()

if "active_business_id" not in st.session_state:
    st.warning(t("no_business_warning", "en"))
    st.stop()

business_id = st.session_state.active_business_id
language = get_business_language(session, business_id)

st.title(t("log_entry_title", language))

source_options = [s.value for s in EnergySource]
source = st.selectbox(
    t("energy_source_label", language),
    options=source_options,
    format_func=lambda s: t(f"source_{s}", language),
)

entry_date = st.date_input(t("date_label", language))
currency = st.selectbox(t("currency_label", language), options=["USD", "LBP"])
cost = st.number_input(t("cost_label", language), min_value=0.0, step=0.5)

units_kwh = None
diesel_liters = None
hours_run = None
time_of_day = None
notes = None

with st.expander(t("more_details_expander", language)):
    if source in ("grid", "solar"):
        units_kwh = st.number_input(
            t("units_kwh_label", language),
            min_value=0.0,
            step=1.0,
            value=None,
            placeholder=t("optional_placeholder", language),
        )

    if source == "generator":
        diesel_liters = st.number_input(
            t("diesel_liters_label", language),
            min_value=0.0,
            step=1.0,
            value=None,
            placeholder=t("optional_placeholder", language),
        )
        hours_run = st.number_input(
            t("hours_run_label", language),
            min_value=0.0,
            step=0.5,
            value=None,
            placeholder=t("optional_placeholder", language),
        )

    if source in ("grid", "generator"):
        time_of_day = st.selectbox(
            t("time_of_day_label", language),
            options=["morning", "afternoon", "evening_night"],
            format_func=lambda tod: t(f"time_of_day_{tod}", language),
            index=None,
            placeholder=t("optional_placeholder", language),
        )

    notes_input = st.text_area(t("notes_label", language))
    notes = notes_input if notes_input else None

if st.button(t("save_entry_button", language)):
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
        notes=notes,
        time_of_day=time_of_day,
    )
    st.success(t("entry_saved_success", language))

st.divider()
st.subheader(t("import_csv_header", language))
st.caption(t("import_csv_caption", language))

uploaded_file = st.file_uploader(t("choose_csv_label", language), type="csv")

if uploaded_file is not None:
    try:
        import_df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(t("could_not_read_csv", language, error=e))
        import_df = None

    if import_df is not None:
        st.write(t("preview_label", language))
        st.dataframe(import_df, use_container_width=True)

        if st.button(t("import_entries_button", language)):
            valid_sources = {s.value for s in EnergySource}
            valid_currencies = {c.value for c in Currency}
            valid_times_of_day = {"morning", "afternoon", "evening_night"}

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
                    skipped.append((row_num, t("missing_required_field", language)))
                    continue

                parsed_date = pd.to_datetime(raw_date, format="%Y-%m-%d", errors="coerce")
                if pd.isna(parsed_date):
                    skipped.append((row_num, t("invalid_date", language, value=raw_date)))
                    continue

                source_value = str(raw_source).strip().lower()
                if source_value not in valid_sources:
                    skipped.append((row_num, t("unrecognized_source", language, value=raw_source)))
                    continue

                raw_currency = row.get("currency")
                if raw_currency is None or pd.isna(raw_currency) or str(raw_currency).strip() == "":
                    currency_value = "USD"
                else:
                    currency_value = str(raw_currency).strip().upper()
                    if currency_value not in valid_currencies:
                        skipped.append((row_num, t("unrecognized_currency", language, value=raw_currency)))
                        continue

                try:
                    cost_value = float(raw_cost)
                except (TypeError, ValueError):
                    skipped.append((row_num, t("invalid_cost", language, value=raw_cost)))
                    continue

                raw_time_of_day = row.get("time_of_day")
                if raw_time_of_day is None or pd.isna(raw_time_of_day) or str(raw_time_of_day).strip() == "":
                    time_of_day_value = None
                else:
                    time_of_day_value = str(raw_time_of_day).strip().lower()
                    if time_of_day_value not in valid_times_of_day:
                        skipped.append((row_num, t("unrecognized_time_of_day", language, value=raw_time_of_day)))
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
                    time_of_day=time_of_day_value,
                )
                if result is not None:
                    imported += 1
                else:
                    skipped.append((row_num, t("database_error_while_saving", language)))
            st.success(t("imported_rows_success", language, imported=imported, total=len(import_df)))
            if skipped:
                st.warning(t("skipped_rows_warning", language, count=len(skipped)))
                st.dataframe(
                    pd.DataFrame(skipped, columns=[t("row_column", language), t("reason_column", language)]),
                    use_container_width=True,
                )

session.close()