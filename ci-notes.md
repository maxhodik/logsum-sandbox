# CI Notes

- **Workflow File:** `.github/workflows/ci.yml`
- **Triggers:** Push and Pull Request on all branches.
- **Environment:** Ubuntu-latest, Python 3.11.
- **Pipeline Steps:**
  1. Checkout repository code.
  2. Set up Python 3.11 environment.
  3. Install `ruff` and `pytest`.
  4. Run linter: `ruff check .`
  5. Run test suite: `pytest -v` (All 5 tests passed successfully).
- **Red-to-Green Recovery Check:** Verified locally and via workflow structure that server-side gates enforce the exact same standard as local preflight checks.