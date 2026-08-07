# Agent Governance Systems

A neutral catalog and federation contract for independently testable agent
systems.

Each registered system owns one bounded question, one primary invariant, and
one evidence discipline. Systems may exchange versioned artifacts, but no
system may silently promote another system's information into authority.

> Repository state: v0.1 defines the federation contract, validates two
> candidate system manifests, and documents possible future boundaries. It is
> an organizational specification, not a runtime orchestrator, safety result,
> ontology, or certification program.

## Registered candidates

| System | Governing question | Repository |
|---|---|---|
| Context integrity | What repository decision is supported by governed context inside a declared trust boundary? | [Agent Context Proof](https://github.com/heronyogi/agent-context-proof) |
| Authority integrity | Which consequential effects remained inside a declared authority boundary? | [Agent Authority Benchmark](https://github.com/heronyogi/agent-authority-benchmark) |

The projects are siblings. Neither is a runtime dependency of the other.

## Federation rules

1. A system boundary is organized around an externally testable invariant.
2. Every system can version, fail, and report evidence independently.
3. Cross-system interfaces are explicit, purpose-bounded, and versioned.
4. Information from one system is not permission for another system to act.
5. Unknown, disputed, expired, or out-of-scope state cannot be silently widened.
6. Every conformance claim names its artifacts and observation boundary.
7. Private derivation machinery is neither required nor exposed.

See the [Federated Systems Charter](CHARTER.md), [contract rules](CONTRACTS.md),
the [system map](docs/system-map.md), and the [adoption guide](docs/adoption.md).

## Repository map

```text
manifests/                 candidate public system declarations
registry/                  validated catalog membership
schemas/                   strict manifest and registry schemas
scripts/validate_catalog.py cross-artifact conformance checks
tests/                     schema and federation invariant tests
docs/                      system map and growth rules
```

## Validate the catalog

Python 3.11 or newer is required.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install ".[dev]"
.venv/bin/python scripts/validate_catalog.py
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
```

Validation is offline and makes no model or repository-network calls.

## Intellectual-property boundary

This catalog contains ordinary system-engineering concepts: boundaries,
invariants, interfaces, evidence, dependencies, versioning, and lifecycle.
It does not contain or require a private ontology, symbolic vocabulary,
signature registry, morphology system, composition law, derivation rule, or
runtime gate.

The public systems demonstrate testable distinctions. They do not disclose how
any private framework may have generated or related those distinctions.

## License

MIT. See [LICENSE](LICENSE).
