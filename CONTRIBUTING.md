# Contributing

Contributions should make a system boundary more explicit, falsifiable, and
independently testable.

## Registering a system

Before proposing registration, read the [charter](CHARTER.md) and
[adoption guide](docs/adoption.md). A proposal must include a strict manifest,
one governing question, one primary invariant, explicit non-claims, named
interfaces, dependency declarations, and an intellectual-property boundary.

Add or change tests whenever a proposal changes validation behavior. Candidate
future systems in the system map are not preapproved registrations.

## Pull requests

Keep each pull request bounded to one system registration, lifecycle change,
schema revision, or validation rule. Explain:

- what changed;
- which invariant or ambiguity motivated it;
- whether any interface or dependency changed;
- how compatibility was evaluated; and
- which checks were run.

Do not include production credentials, personal data, private correspondence,
sealed cases, or private derivation machinery.

## Validation

Run:

```bash
python scripts/validate_catalog.py
python -m pytest
python -m ruff check .
python -m ruff format --check .
```
