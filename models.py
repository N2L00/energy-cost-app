from datetime import date, datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class EnergySource(PyEnum):
    GRID = "grid"
    GENERATOR = "generator"
    SOLAR = "solar"


class Currency(PyEnum):
    USD = "USD"
    LBP = "LBP"


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    exchange_rate: Mapped[float] = mapped_column(default=89000.0)
    budget_threshold: Mapped[Optional[float]] = mapped_column(default=None)
    language: Mapped[Optional[str]] = mapped_column(default="en")
    generator_capacity_kva: Mapped[Optional[float]] = mapped_column(default=None)

    entries: Mapped[list["EnergyEntry"]] = relationship(back_populates="business", cascade="all, delete-orphan")
    outages: Mapped[list["Outage"]] = relationship(cascade="all, delete-orphan")
    recommendations: Mapped[list["Recommendation"]] = relationship(cascade="all, delete-orphan")
    outage_schedules: Mapped[list["OutageSchedule"]] = relationship(cascade="all, delete-orphan")
    dashboard_views: Mapped[list["DashboardView"]] = relationship(cascade="all, delete-orphan")


class EnergyEntry(Base):
    __tablename__ = "energy_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"))
    date: Mapped[date]
    source: Mapped[EnergySource] = mapped_column(Enum(EnergySource))
    currency: Mapped[Currency] = mapped_column(Enum(Currency), default=Currency.USD)
    cost: Mapped[float]
    units_kwh: Mapped[Optional[float]] = mapped_column(default=None)
    diesel_liters: Mapped[Optional[float]] = mapped_column(default=None)
    hours_run: Mapped[Optional[float]] = mapped_column(default=None)
    notes: Mapped[Optional[str]] = mapped_column(default=None)
    time_of_day: Mapped[Optional[str]] = mapped_column(default=None)

    business: Mapped["Business"] = relationship(back_populates="entries")


class Outage(Base):
    __tablename__ = "outages"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"))
    date: Mapped[date]
    hours_down: Mapped[float]
    notes: Mapped[Optional[str]] = mapped_column(default=None)

    business: Mapped["Business"] = relationship(overlaps="outages")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    recommendation_text: Mapped[str]
    followed: Mapped[Optional[bool]] = mapped_column(default=None)

    business: Mapped["Business"] = relationship(overlaps="recommendations")

class OutageSchedule(Base):
    __tablename__ = "outage_schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"))
    hours_per_day: Mapped[float]
    active: Mapped[bool] = mapped_column(default=True)

    business: Mapped["Business"] = relationship(overlaps="outage_schedules")


class DashboardView(Base):
    __tablename__ = "dashboard_views"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"))
    viewed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    business: Mapped["Business"] = relationship(overlaps="dashboard_views")