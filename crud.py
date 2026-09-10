import pandas as pd
from datetime import date as date_type
from sqlalchemy.orm import Session

from models import Business, EnergyEntry, EnergySource


def get_or_create_default_business(session: Session) -> Business:
    business = session.query(Business).first()
    if business is None:
        business = Business(name="My Business")
        session.add(business)
        session.commit()
        session.refresh(business)
    return business


def create_energy_entry(
    session: Session,
    business_id: int,
    entry_date,
    source: EnergySource,
    cost: float,
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
        units_kwh=units_kwh,
        diesel_liters=diesel_liters,
        hours_run=hours_run,
        notes=notes,
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry



def get_entries_dataframe(session: Session, business_id: int) -> pd.DataFrame:
    entries = (
        session.query(EnergyEntry)
        .filter(EnergyEntry.business_id == business_id)
        .all()
    )
    data = [
        {
            "date": e.date,
            "source": e.source.value,
            "cost": e.cost,
            "units_kwh": e.units_kwh,
            "diesel_liters": e.diesel_liters,
            "hours_run": e.hours_run,
            "notes": e.notes,
        }
        for e in entries
    ]
    return pd.DataFrame(data)

def get_cost_summary(
    session: Session,
    business_id: int,
    source: str | None = None,
    start_date: date_type | None = None,
    end_date: date_type | None = None,
) -> dict:
    query = session.query(EnergyEntry).filter(EnergyEntry.business_id == business_id)

    if source is not None:
        query = query.filter(EnergyEntry.source == EnergySource(source))
    if start_date is not None:
        query = query.filter(EnergyEntry.date >= start_date)
    if end_date is not None:
        query = query.filter(EnergyEntry.date <= end_date)

    entries = query.all()

    total_cost = sum(e.cost for e in entries)
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
def create_business(session: Session, name: str) -> Business:
    business = Business(name=name)
    session.add(business)
    session.commit()
    session.refresh(business)
    return business


def get_all_businesses(session: Session) -> list[Business]:
    return session.query(Business).all()