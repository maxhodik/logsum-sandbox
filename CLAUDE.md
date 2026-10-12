\# CLAUDE.md



\## Project Context

A tiny CLI that summarizes synthetic `events.csv` logs. The project operates entirely in a sandbox environment with no real data.



\## Conventions

\- Code is stored in the `src/` directory.  

\- Tests are stored in the `tests/` directory.  

\- Synthetic data is stored in the `data/` directory.  



\## Utilities to Prefer

\- Use Python 3.11 standard library.  

\- Prefer `ruff` for linting.  

\- Use `pytest` for testing.  



\## Escalation Gates

\- Stop before adding external dependencies.  

\- Operate only on synthetic data; do not introduce real data.  

\- Never overwrite `spec.md` after sign-off without explicit confirmation.  

