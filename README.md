
# Energy Cost Tracker

A manual energy-cost tracking tool for small businesses in Lebanon, where power comes from three unreliable, differently-priced sources: the public grid, diesel generators, and increasingly solar. Built solo, end to end — schema to cloud deployment.

**Live app:** [energy-cost-app.streamlit.app](https://energy-cost-app-mtpsjnjcmg44prvyhvangj.streamlit.app)

## The Problem

Lebanon's chronic grid shortages mean small business owners juggle three power sources with wildly different, often volatile pricing. Existing tracking tools are industrial IoT systems built for large fleets — there was no simple, manual-entry tool sized for a single small business trying to understand its own costs across grid, generator, and solar at once.

## Features

**Tracking**
- Manual entry logging per source, with fields that adapt to what's relevant (diesel liters and hours for generator, kWh for grid/solar)
- Multi-business support
- Outage logging, plus recurring outage schedules for predictable rationing patterns
- CSV bulk import (with per-row validation) and CSV/PDF export

**Understanding the numbers**
- Dashboard with cost totals, cost-by-source and cost-over-time charts
- Real cost-per-kWh (grid/solar) and cost-per-hour (generator) efficiency metrics
- Grid rate compared against typical EDL subsidized-tier pricing
- Monthly budget threshold alerts
- Time-of-day tracking for grid/generator usage, to see whether usage overlaps with solar-producing hours

**AI-powered decision support**
- Natural-language querying over your own data (Claude tool-use — the AI never touches the database directly)
- Data-grounded cost-saving recommendations: battery storage and shared-generator-subscription ("ishtirak") reasoning based on real outage hours and generator costs; generator right-sizing analysis based on fuel-consumption physics — every claim only appears when the underlying numbers actually support it, never generic advice
- A closed feedback loop: every recommendation is tracked, markable as followed or not, and compared against actual before/after monthly spending
- Solar payback calculator (supports direct kWh or panel-count input) and a what-if savings simulator for hypothetical usage changes

**Sharing**
- Downloadable PDF cost reports
- Shareable, WhatsApp-friendly PNG summary cards

**Accessibility**
- Full multi-language support (English, French, Arabic)

## Tech Stack

- **Python 3.14**
- **SQLAlchemy 2.0** (modern `Mapped[]` syntax) — ORM / database layer
- **Streamlit** — multi-page frontend, `st.navigation`-based router for language-aware sidebar labels
- **Anthropic Claude API** — natural-language querying, recommendations, calculators
- **SQLite** (local development) / **PostgreSQL via Neon** (production)
- **Pillow** — summary card image generation
- **ReportLab** — PDF report generation
- **GitHub + Streamlit Community Cloud** — version control and deployment

## Setup

```bash
git clone <this-repo>
cd energy-cost-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with: