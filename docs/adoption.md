# System adoption guide

## 1. Establish the boundary

Write one governing question and one primary invariant. The invariant must be
evaluated from declared evidence without requiring access to private derivation
machinery.

List in-scope behavior and explicit non-claims. If two proposed components can
fail, version, or produce evidence only as one unit, they are probably one
system. If they own different invariants and can fail independently, they may
be separate systems.

## 2. Start with one root repository

Add these files to the system root:

- `SYSTEM.md` for the human-readable boundary;
- `CONTRACTS.md` for provided and consumed interfaces;
- `system.manifest.json` for the machine-readable declaration; and
- a test that preserves the system identifier, dependency boundary, non-claims,
  and public IP exclusions.

Use the canonical manifest schema URL. Keep runtime and evaluation dependency
lists empty unless the dependency is real, required, and testable.

## 3. Register a candidate

Copy the source manifest into `manifests/`, add a matching registry entry with
adoption state `candidate`, and run the offline catalog validator. Catalog and
source copies must remain identical during adoption review.

Candidate status means structural conformance only. It does not certify the
implementation or validate the system's external authority.

## 4. Activate adoption

After the source manifest is present on the system repository's default branch:

1. verify the source and catalog manifest contents match;
2. verify the repository's required checks pass;
3. change catalog adoption to `active`; and
4. record the exact source and catalog commits in the activation pull request.

## 5. Split only at a real boundary

Create a cluster repository when a component has its own release cadence,
security or access boundary, contributor audience, reuse contract, or evidence
policy. Preserve the same `system_id` and choose a specific `repository_role`.

Cross-repository source sharing does not by itself justify a cluster split.

## 6. Change without rewriting history

Version incompatible interface or schema changes. Mark deprecated and retired
systems explicitly. Preserve historical manifests and evidence needed to
interpret earlier conformance claims.
