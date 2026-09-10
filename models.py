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


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    entries: Mapped[list["EnergyEntry"]] = relationship(back_populates="business")


class EnergyEntry(Base):
    __tablename__ = "energy_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"))
    date: Mapped[date]
    source: Mapped[EnergySource] = mapped_column(Enum(EnergySource))
    cost: Mapped[float]
    units_kwh: Mapped[Optional[float]] = mapped_column(default=None)
    diesel_liters: Mapped[Optional[float]] = mapped_column(default=None)
    hours_run: Mapped[Optional[float]] = mapped_column(default=None)
    notes: Mapped[Optional[str]] = mapped_column(default=None)

    business: Mapped["Business"] = relationship(back_populates="entries")