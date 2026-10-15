# Project Context
- Tiny Java CLI tool that summarises synthetic events.csv logs.

# Conventions
- Code in `src/main/java/`, tests in `src/test/java/`, data in `data/`.
- Build tool: Maven (`pom.xml`).

# Utilities to Prefer
- Java 21 standard library (records, NIO).
- JUnit 5 for testing.
- Pure Java standard library (no external dependencies).

# Escalation Gates
- Stop before adding new external dependencies to `pom.xml`.
- Use synthetic data only; never commit real PII.
- Never overwrite `spec.md` after sign-off without asking.