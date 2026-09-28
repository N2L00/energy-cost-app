# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Hard rules
- Every schema change needs a migration on BOTH databases:
  SQLite (local) and Neon PostgreSQL (production).
- Verify behavior in Terminal before touching the UI.
- Never print, log, or echo secrets (DATABASE_URL, API keys).
  Never read or edit .env.
- Test adversarially: try to break a feature before calling
  it done.
- AI features: the model interprets, Python does the math.
- Every new UI string goes into translations.py in all three languages (en, fr, ar).

## Commands

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# First-time DB init (creates tables from models.py)
python init_db.py

# Run the app
streamlit run app.py
```

There is no test suite, linter, or build step configured in this repo. There is also no
`.env.example` — a `.env` must be created manually with `ANTHROPIC_API_KEY` set, and
`DATABASE_URL` left commented out locally (defaults to `sqlite:///energy.db`) or set to a
Neon/Postgres connection string in production. When testing, use an isolated in-memory
SQLite database, never energy.db or Neon.

## Architecture

**Multi-page Streamlit app**, wired up in `app.py` via `st.navigation` — pages are files
under `pages/`, numbered by sidebar order (`1_Log_Entry.py` ... `7_What_If_Simulator.py`),
plus `home.py` as the default page. Page titles/icons are resolved per-request through
`t(...)` so the sidebar itself is language-aware. `app.py` also establishes
`st.session_state.active_business_id` once per session (via
`get_or_create_default_business`), which every other page reads to scope its data.

**Layers, strictly separated:**
- `models.py` — SQLAlchemy `Mapped[]`-style ORM models (`Business`, `EnergyEntry`,
  `Outage`, `OutageSchedule`, `Recommendation`, `DashboardView`). Everything is scoped to a
  `business_id` to support the multi-business switcher.
- `crud.py` — the only module that touches the database. All read/write logic for every
  page lives here as flat functions taking `(session, business_id, ...)`. Pages and
  `ai_query.py` call into `crud.py`; they never issue queries directly. Every function that
  hits the DB is wrapped in `@handle_db_errors(fallback=...)`, which catches
  `SQLAlchemyError` only — a `ValueError` (e.g. business-rule validation) is intentionally
  left to propagate rather than being swallowed into the fallback.
- `ai_query.py` — all Anthropic API calls. Ask-AI uses Claude tool-use, where the "tools"
  are `crud.py` functions (e.g. `get_cost_summary`) — Claude decides what data to pull and
  narrates it, but never queries the database itself. Recommendations, the solar payback
  narrative, and the what-if simulator follow the same split: `crud.py` computes the real
  numbers first, and the prompt to Claude is built by interpolating those numbers in, so the
  model is reasoning over ground-truth figures rather than inventing them.
- `reports.py` / `summary_card.py` — output formatting only (ReportLab PDF, Pillow PNG
  summary card for WhatsApp sharing). These consume already-computed data (e.g. a DataFrame
  from `crud.py`), not raw models.
- `translations.py` — all static UI chrome strings (labels, buttons, captions) for en/fr/ar,
  looked up via `t(key, language, **kwargs)`. AI-generated text (recommendations, Ask-AI
  answers) deliberately does *not* go through this module — it stays in whatever language
  the model responded in. Streamlit has no native RTL layout support, so Arabic text itself
  renders correctly but page layout direction does not flip.

**Migrations** are one-off scripts at the repo root (`migrate_add_*.py`), not a migration
framework. Each one is idempotent (checks `inspect(engine)` for the column/table before
altering) and dialect-agnostic (plain `ALTER TABLE`, works against both SQLite and
Postgres) — follow that pattern for new ones. Run new migrations against local SQLite only.
For Neon, give me the exact SQL statement to run in the Neon SQL Editor, and never push a
schema change until I confirm the Neon migration is done.

**Currency**: entries are stored in their original currency (USD or LBP) plus the
business's `exchange_rate`; `crud.to_usd()` is the single conversion point used whenever
costs need to be compared or summed across currencies.

## Deployment

Pushing to `main` auto-deploys to Streamlit Community Cloud, which is production with real
users. Production secrets live in Streamlit Cloud secrets, never in this repo.
