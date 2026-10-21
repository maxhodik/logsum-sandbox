# K 5.W.9 - By-hand vs by-agent comparison

## What both produced
- A fully functional Python CLI tool (`src/logsum.py`) for summarising event logs.
- A comprehensive specification (`spec.md`) and a robust test suite (`tests/test_logsum.py`).
- Server-side CI configuration via GitHub Actions (`.github/workflows/ci.yml`).
- Supporting documentation, including project context rules (`CLAUDE.md`), provenance notes, test notes, refactor notes, and code Q&A with citations.

## Where the agent saved time
- Generating boilerplate code structures, standard CSV reading logic, and initial test templates in a single batch pass.
- Quickly drafting standard GitHub Actions workflow syntax without manual YAML lookups.

## Where the agent went wrong or shorter
- **Blind spots in edge cases:** An async agent pass often misses nuanced requirements (such as specific normalisation rules or missing-level fallbacks) unless constrained by strict step-by-step gates.
- **Linter and style enforcement:** The agent-generated code initially triggered `ruff` linting errors (like import sorting and missing explicit `check=` arguments in `subprocess.run`), requiring iterative manual fixes.

## What the agent did better
- Provided rapid end-to-end scaffolding and boilerplate generation, reducing the friction of starting a project from scratch.

## What I learned about supervised vs async
- **Supervised step-by-step work** ensures high fidelity to specifications, rigorous edge-case handling, and immediate visibility into technical debt or contract violations.
- **Async/agent delegation** is efficient for scaffolding and bulk code generation, but dangerous without rigorous automated gates (CI, linter, tests) and explicit provenance tracking.

## What I would do differently next time
- Establish automated linter and test gates *before* delegating larger blocks of code to an agent.
- Enforce strict micro-step planning and incremental provenance logging to catch deviations before they compound into larger technical debt.