"""One-off migration: add the 'last_generator_service' column to the businesses table.

Safe to run multiple times (checks for the column first) and works against
either SQLite or Postgres, since it uses SQLAlchemy's dialect-agnostic
inspector and a plain ALTER TABLE ... ADD COLUMN supported by both.

Run locally with the default DATABASE_URL (sqlite:///energy.db), or against
Neon/Postgres by setting DATABASE_URL to the production connection string
before running this script.
"""

from sqlalchemy import inspect, text
from database import engine


def column_exists(table_name: str, column_name: str) -> bool:
    inspector = inspect(engine)
    columns = {col["name"] for col in inspector.get_columns(table_name)}
    return column_name in columns


if column_exists("businesses", "last_generator_service"):
    print("'last_generator_service' column already exists on 'businesses' — nothing to do.")
else:
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE businesses ADD COLUMN last_generator_service DATE"))
    print("Added 'last_generator_service' column to 'businesses'.")
