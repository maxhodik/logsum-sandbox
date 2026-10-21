# Refactor Notes

## Removed / Changed by AI in the Refactor
- **Extracted row parsing into `parse_event_row()` helper function.**
  - *AI reason:* Improve readability and modularity of the main processing loop.
  - *My decision:* **Keep**. It cleans up the `main()` function without altering any normalisation or edge-case behavior (such as `UNKNOWN` level fallback).
- **Added explicit guard `if not timestamp and not service: continue` for blank lines.**
  - *AI reason:* Prevent processing malformed empty rows.
  - *My decision:* **Keep / Document**. Aligns safely with edge-case specifications.