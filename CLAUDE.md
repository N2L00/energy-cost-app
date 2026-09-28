
## Hard rules
- Every schema change needs a migration on BOTH databases:
  SQLite (local) and Neon PostgreSQL (production).
- Verify behavior in Terminal before touching the UI.
- Never print, log, or echo secrets (DATABASE_URL, API keys).
  Never read or edit .env.
- Test adversarially: try to break a feature before calling
  it done.
- AI features: the model interprets, Python does the math.
