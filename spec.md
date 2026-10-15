# Specification: Log Summary CLI

## Goal
Summarise synthetic `events.csv` logs into a grouped `summary.csv` report via a command-line interface.

## Inputs
- `events.csv` containing columns: `timestamp`, `level`, `service`, `message`.

## Outputs
- `summary.csv` containing aggregated event groups.

## Normalisation Rules
- Timestamps preserved as strings.
- Log levels normalised to uppercase; missing levels default to `UNKNOWN`.
- Service names trimmed of whitespace.

## Grouping Rule
- Grouped by the exact key: `(service, level)`.

## Aggregation
- Count of events per group.
- `first_seen` timestamp and `last_seen` timestamp per group.

## Edge Cases
- **Missing level:** Default to `UNKNOWN`.
- **Empty input:** Print error message and exit with code 1.

## CLI
- Usage: `python -m src.logsum data/sample_events.csv data/summary.csv`
- Exit codes: `0` on success, `1` on error.

## Out of Scope
- Real-time log streaming.
- Database storage or web UI dashboards.

## Implementation notes
- Implemented using pure Python 3.11 standard library (`csv`, `argparse`, `collections`).
- Missing log levels default to `UNKNOWN`.

## Signed off
- **Author:** Maksym Hodik (MH)
- **Date:** 2026-10-15