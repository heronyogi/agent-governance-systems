# Repository instructions

- Keep this catalog independent of model providers and runtime frameworks.
- Organize systems around externally testable invariants, not private ontology primitives.
- Do not publish private symbols, registries, signatures, morphologies, formulas, mappings, or correspondence.
- Treat every cross-system interface as versioned data with an explicit claim boundary.
- Never let information, confidence, or a prior decision silently become authority for another system.
- Keep proposed systems visibly distinct from registered systems.
- Before finishing a change, run `python -m pytest`, `python -m ruff check .`, and `python -m ruff format --check .` from the project environment.
