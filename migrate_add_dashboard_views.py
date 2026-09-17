"""One-off migration: create the 'dashboard_views' table.

Safe to run multiple times (checks for the table first) and works against
either SQLite or Postgres, since it uses SQLAlchemy's dialect-agnostic
inspector and table-level create(), same approach as the other migrations
in this project.

Run locally with the default DATABASE_URL (sqlite:///energy.db), or against
Neon/Postgres by setting DATABASE_URL to the production connection string
before running this script.
"""

from sqlalchemy import inspect
from database import engine
from models import DashboardView


def table_exists(table_name: str) -> bool:
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


if table_exists("dashboard_views"):
    print("'dashboard_views' table already exists — nothing to do.")
else:
    DashboardView.__table__.create(engine)
    print("Created 'dashboard_views' table.")