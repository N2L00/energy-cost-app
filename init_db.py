from database import engine, Base
import models  # noqa: F401 — needed so SQLAlchemy sees the model classes

Base.metadata.create_all(engine)

print("Database tables created.")