import pandas as pd
from functools import wraps
from datetime import date as date_type
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models import Business, EnergyEntry, EnergySource, Currency, Outage, Recommendation


def handle_db_errors(fallback):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SQLAlchemyError:
                return fallback
        return wrapper
    return decorator


def to_usd(cost: float, currency: Currency, exchange_rate: float) -> float:
    if currency == Currency.LBP:
        return cost / exchange_rate
    return cost


@handle_db_errors(fallback=None)
def get_or_create_default_business(session: Session) -> Business:
    business = session.query(Business).first()
    if business is None:
        business = Business(name="My Business")
        session.add(business)
        session.commit()
        session.refresh(business)
    return business


@handle_db_errors(fallback=None)
def create_energy_entry(
    session: Session,
    business_id: int,
    entry_date,
    source: EnergySource,
    cost: float,
    currency: Currency = Currency.USD,
    units_kwh: float | None = None,
    diesel_liters: float | None = None,
    hours_run: float | None = None,
    notes: str | None = None,
) -> EnergyEntry:
    entry = EnergyEntry(
        business_id=business_id,
        date=entry_date,
        source=source,
        cost=cost,
        currency=currency,
        units_kwh=units_kwh,
        diesel_liters=diesel_liters,
        hours_run=hours_run,
        notes=notes,
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@handle_db_errors(fallback=pd.DataFrame())
def get_entries_dataframe(session: Session, business_id: int) -> pd.DataFrame:
    business = session.query(Business).filter(Business.id == business_id).first()
    exchange_rate = business.exchange_rate if business else 89000.0

    entries = (
        session.query(EnergyEntry)
        .filter(EnergyEntry.business_id == business_id)
        .all()
    )
    data = [
        {
            "id": e.id,
            "date": e.date,
            "source": e.source.value,
            "currency": e.currency.value,
            "cost": e.cost,
            "cost_usd": to_usd(e.cost, e.currency, exchange_rate),
            "units_kwh": e.units_kwh,
            "diesel_liters": e.diesel_liters,
            "hours_run": e.hours_run,
            "notes": e.notes,
        }
        for e in entries
    ]
    return pd.DataFrame(data)


_EMPTY_SUMMARY = {
    "entry_count": 0,
    "total_cost": 0.0,
    "total_kwh": 0.0,
    "total_diesel_liters": 0.0,
    "total_hours_run": 0.0,
}


@handle_db_errors(fallback=_EMPTY_SUMMARY)
def get_cost_summary(
    session: Session,
    business_id: int,
    source: str | None = None,
    start_date: date_type | None = None,
    end_date: date_type | None = None,
) -> dict:
    business = session.query(Business).filter(Business.id == business_id).first()
    exchange_rate = business.exchange_rate

    query = session.query(EnergyEntry).filter(EnergyEntry.business_id == business_id)

    if source is not None:
        query = query.filter(EnergyEntry.source == EnergySource(source))
    if start_date is not None:
        query = query.filter(EnergyEntry.date >= start_date)
    if end_date is not None:
        query = query.filter(EnergyEntry.date <= end_date)

    entries = query.all()

    total_cost = sum(to_usd(e.cost, e.currency, exchange_rate) for e in entries)
    total_kwh = sum(e.units_kwh or 0 for e in entries)
    total_diesel = sum(e.diesel_liters or 0 for e in entries)
    total_hours = sum(e.hours_run or 0 for e in entries)

    return {
        "entry_count": len(entries),
        "total_cost": round(total_cost, 2),
        "total_kwh": round(total_kwh, 2),
        "total_diesel_liters": round(total_diesel, 2),
        "total_hours_run": round(total_hours, 2),
    }


def get_all_source_summaries(session: Session, business_id: int) -> dict:
    return {
        source.value: get_cost_summary(session, business_id, source=source.value)
        for source in EnergySource
    }


@handle_db_errors(fallback=None)
def create_business(session: Session, name: str) -> Business:
    business = Business(name=name)
    session.add(business)
    session.commit()
    session.refresh(business)
    return business


@handle_db_errors(fallback=[])
def get_all_businesses(session: Session) -> list[Business]:
    return session.query(Business).all()


@handle_db_errors(fallback=None)
def get_business_by_id(session: Session, business_id: int) -> Business | None:
    return session.query(Business).filter(Business.id == business_id).first()


@handle_db_errors(fallback=None)
def update_exchange_rate(session: Session, business_id: int, new_rate: float) -> Business | None:
    business = get_business_by_id(session, business_id)
    if business is None:
        return None
    business.exchange_rate = new_rate
    session.commit()
    session.refresh(business)
    return business


@handle_db_errors(fallback=None)
def update_budget_threshold(session: Session, business_id: int, new_threshold: float | None) -> Business | None:
    business = get_business_by_id(session, business_id)
    if business is None:
        return None
    business.budget_threshold = new_threshold
    session.commit()
    session.refresh(business)
    return business


@handle_db_errors(fallback={"spent": 0.0, "threshold": None, "over_budget": False})
def get_current_month_spending(session: Session, business_id: int) -> dict:
    business = get_business_by_id(session, business_id)
    if business is None:
        return {"spent": 0.0, "threshold": None, "over_budget": False}

    today = date_type.today()
    month_start = today.replace(day=1)

    summary = get_cost_summary(session, business_id, start_date=month_start, end_date=today)

    return {
        "spent": summary["total_cost"],
        "threshold": business.budget_threshold,
        "over_budget": (
            business.budget_threshold is not None
            and summary["total_cost"] > business.budget_threshold
        ),
    }


@handle_db_errors(fallback=None)
def get_entry_by_id(session: Session, entry_id: int) -> EnergyEntry | None:
    return session.query(EnergyEntry).filter(EnergyEntry.id == entry_id).first()


@handle_db_errors(fallback=None)
def update_energy_entry(
    session: Session,
    entry_id: int,
    entry_date,
    source: EnergySource,
    cost: float,
    currency: Currency = Currency.USD,
    units_kwh: float | None = None,
    diesel_liters: float | None = None,
    hours_run: float | None = None,
    notes: str | None = None,
) -> EnergyEntry | None:
    entry = get_entry_by_id(session, entry_id)
    if entry is None:
        return None

    entry.date = entry_date
    entry.source = source
    entry.cost = cost
    entry.currency = currency
    entry.units_kwh = units_kwh
    entry.diesel_liters = diesel_liters
    entry.hours_run = hours_run
    entry.notes = notes

    session.commit()
    session.refresh(entry)
    return entry


@handle_db_errors(fallback=False)
def delete_energy_entry(session: Session, entry_id: int) -> bool:
    entry = get_entry_by_id(session, entry_id)
    if entry is None:
        return False

    session.delete(entry)
    session.commit()
    return True


def get_cost_per_unit(session: Session, business_id: int) -> dict:
    summaries = get_all_source_summaries(session, business_id)
    result = {}

    for source, data in summaries.items():
        if source in ("grid", "solar"):
            if data["total_kwh"] > 0:
                result[source] = {
                    "metric": "cost per kWh",
                    "value": round(data["total_cost"] / data["total_kwh"], 3),
                }
            else:
                result[source] = {"metric": "cost per kWh", "value": None}
        elif source == "generator":
            if data["total_hours_run"] > 0:
                result[source] = {
                    "metric": "cost per hour",
                    "value": round(data["total_cost"] / data["total_hours_run"], 2),
                }
            else:
                result[source] = {"metric": "cost per hour", "value": None}

    return result


def calculate_solar_payback(session: Session, business_id: int, upfront_cost: float, extra_kwh_per_day: float) -> dict:
    cost_per_unit = get_cost_per_unit(session, business_id)
    grid_rate = cost_per_unit["grid"]["value"]

    if grid_rate is None or extra_kwh_per_day <= 0:
        return {"possible": False}

    daily_savings = extra_kwh_per_day * grid_rate
    monthly_savings = daily_savings * 30
    months_to_payback = upfront_cost / monthly_savings if monthly_savings > 0 else None

    return {
        "possible": True,
        "monthly_savings": round(monthly_savings, 2),
        "months_to_payback": round(months_to_payback, 1) if months_to_payback else None,
    }


def simulate_savings(
    session: Session,
    business_id: int,
    generator_hours_reduction: float = 0.0,
    grid_to_solar_kwh_shift: float = 0.0,
) -> dict:
    if generator_hours_reduction < 0 or grid_to_solar_kwh_shift < 0:
        return {"possible": False}

    cost_per_unit = get_cost_per_unit(session, business_id)
    generator_rate = cost_per_unit.get("generator", {}).get("value")
    grid_rate = cost_per_unit.get("grid", {}).get("value")
    solar_rate = cost_per_unit.get("solar", {}).get("value") or 0.0

    generator_daily_savings = 0.0
    if generator_hours_reduction > 0:
        if generator_rate is None:
            return {"possible": False}
        generator_daily_savings = generator_hours_reduction * generator_rate

    grid_shift_daily_savings = 0.0
    if grid_to_solar_kwh_shift > 0:
        if grid_rate is None:
            return {"possible": False}
        grid_shift_daily_savings = grid_to_solar_kwh_shift * (grid_rate - solar_rate)

    if generator_hours_reduction == 0 and grid_to_solar_kwh_shift == 0:
        return {"possible": False}

    total_daily_savings = generator_daily_savings + grid_shift_daily_savings

    return {
        "possible": True,
        "generator_daily_savings": round(generator_daily_savings, 2),
        "grid_shift_daily_savings": round(grid_shift_daily_savings, 2),
        "total_daily_savings": round(total_daily_savings, 2),
        "total_monthly_savings": round(total_daily_savings * 30, 2),
    }


@handle_db_errors(fallback=None)
def save_recommendation(session: Session, business_id: int, recommendation_text: str):
    rec = Recommendation(business_id=business_id, recommendation_text=recommendation_text)
    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec


@handle_db_errors(fallback=pd.DataFrame())
def get_recommendations_dataframe(session: Session, business_id: int) -> pd.DataFrame:
    recs = (
        session.query(Recommendation)
        .filter(Recommendation.business_id == business_id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )
    data = [
        {"id": r.id, "created_at": r.created_at, "recommendation_text": r.recommendation_text}
        for r in recs
    ]
    return pd.DataFrame(data)


@handle_db_errors(fallback={"possible": False})
def get_recommendation_impact(session: Session, business_id: int, recommendation_id: int) -> dict:
    from datetime import timedelta

    rec = session.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if rec is None:
        return {"possible": False}

    rec_month_start = rec.created_at.date().replace(day=1)

    if rec_month_start.month == 1:
        before_month_start = rec_month_start.replace(year=rec_month_start.year - 1, month=12)
    else:
        before_month_start = rec_month_start.replace(month=rec_month_start.month - 1)
    before_month_end = rec_month_start - timedelta(days=1)

    if rec_month_start.month == 12:
        after_month_start = rec_month_start.replace(year=rec_month_start.year + 1, month=1)
    else:
        after_month_start = rec_month_start.replace(month=rec_month_start.month + 1)
    if after_month_start.month == 12:
        after_month_end = after_month_start.replace(year=after_month_start.year + 1, month=1) - timedelta(days=1)
    else:
        after_month_end = after_month_start.replace(month=after_month_start.month + 1) - timedelta(days=1)

    if date_type.today() < after_month_end:
        return {"possible": False, "reason": "Not enough time has passed yet to measure the 'after' month."}

    before_summary = get_cost_summary(session, business_id, start_date=before_month_start, end_date=before_month_end)
    after_summary = get_cost_summary(session, business_id, start_date=after_month_start, end_date=after_month_end)

    before_cost = before_summary["total_cost"]
    after_cost = after_summary["total_cost"]
    change = after_cost - before_cost

    return {
        "possible": True,
        "before_cost": before_cost,
        "after_cost": after_cost,
        "change": round(change, 2),
        "improved": change < 0,
    }


@handle_db_errors(fallback=None)
def log_outage(session: Session, business_id: int, outage_date, hours_down: float, notes: str | None = None):
    outage = Outage(business_id=business_id, date=outage_date, hours_down=hours_down, notes=notes)
    session.add(outage)
    session.commit()
    session.refresh(outage)
    return outage


@handle_db_errors(fallback=pd.DataFrame())
def get_outages_dataframe(session: Session, business_id: int) -> pd.DataFrame:
    outages = (
        session.query(Outage)
        .filter(Outage.business_id == business_id)
        .all()
    )
    data = [
        {"id": o.id, "date": o.date, "hours_down": o.hours_down, "notes": o.notes}
        for o in outages
    ]
    return pd.DataFrame(data)


@handle_db_errors(fallback=0.0)
def get_total_outage_hours(session: Session, business_id: int) -> float:
    outages = session.query(Outage).filter(Outage.business_id == business_id).all()
    return round(sum(o.hours_down for o in outages), 2)


@handle_db_errors(fallback=False)
def delete_business(session: Session, business_id: int) -> bool:
    business = get_business_by_id(session, business_id)
    if business is None:
        return False
    session.delete(business)
    session.commit()
    return True