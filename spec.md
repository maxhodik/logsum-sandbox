\# Specification: Log Summary CLI



\## Goal

Summarise synthetic `events.csv` logs into a grouped `summary.csv` report via a command-line interface.



\## Inputs

\- `events.csv` containing columns: `timestamp`, `level`, `service`, `message`.



\## Outputs

\- `summary.csv` containing aggregated event groups.



\## Normalisation Rules

\- Timestamps normalised to ISO-8601 format.

\- Log levels normalised to uppercase (e.g., INFO, ERROR, WARN).

\- Service names trimmed of whitespace.



\## Grouping Rule

\- Grouped by the exact key: `(service, level)`.



\## Aggregation

\- Count of events per group.

\- `first\_seen` timestamp and `last\_seen` timestamp per group.



\## Edge Cases

\- \*\*Missing level:\*\* Default to `UNKNOWN`.

\- \*\*Malformed timestamp:\*\* Skip the row or log a warning and treat timestamp as invalid/epoch.

\- \*\*Empty input:\*\* Output an empty `summary.csv` with headers and exit with code 0.



\## CLI

\- Usage: `python -m src.cli --input data/events.csv --output data/summary.csv`

\- Exit codes: `0` on success, `1` on error (e.g., file not found).



\## Out of Scope

\- Real-time log tailing or streaming.

\- Database storage or web UI dashboards.

\- Complex regex pattern matching for messages.



\## Signed off

\- \*\*Author:\*\* Maksym Hodik (MH)

\- \*\*Date:\*\* 2026-10-15

