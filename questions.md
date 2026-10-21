# Code Questions and Citations

## Q1: Where is the grouping rule?
- **Files read:** `spec.md`, `src/logsum.py`
- **Answer:** The grouping rule dictates that events are aggregated using a composite key consisting of the service name and the log level `(service, level)`.
- **Citations:**
  - `spec.md:19` (`## Grouping Rule - Grouped by the exact key: (service, level).`)
  - `src/logsum.py:34` (`key = (service, level)`)
- **Unverifiable items:** None.

## Q2: How is missing level handled?
- **Files read:** `spec.md`, `src/logsum.py`
- **Answer:** If a log event has a missing or empty level field, it is normalized and defaulted to the string `"UNKNOWN"`.
- **Citations:**
  - `spec.md:23` (`- **Missing level:** Default to UNKNOWN.`)
  - `src/logsum.py:10` (`level = row.get("level", "").strip() or "UNKNOWN"`)
- **Unverifiable items:** None.

## Q3: How do I run tests and CI locally?
- **Files read:** `tests/test_logsum.py`, `.github/workflows/ci.yml`
- **Answer:** Local tests can be executed using `pytest -v`, and the CI workflow performs both `ruff check .` and `pytest -v` under Python 3.11.
- **Citations:**
  - `tests/test_logsum.py:1` (pytest framework usage)
  - `.github/workflows/ci.yml:25-29` (CI steps running ruff check and pytest)
- **Unverifiable items:** None.

---

## Verification
- **Q1 Verification:** Verified. `spec.md` line 19 and `src/logsum.py` line 34 match the cited composite key exactly. Verdict: **Correct**.
- **Q2 Verification:** Verified. `spec.md` line 23 and `src/logsum.py` line 10 correctly define the `UNKNOWN` fallback. Verdict: **Correct**.
- **Q3 Verification:** Verified. `.github/workflows/ci.yml` lines 25–29 explicitly invoke `ruff check .` and `pytest -v`. Verdict: **Correct**.