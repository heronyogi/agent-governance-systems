# FET-001 review guide

## Status

FET-001 is a protocol-only candidate frozen for public review. No Context
adapter, Authority consumer, live-model evaluation, sealed case set, or
experimental result exists under this protocol.

The implementation gate is closed. Merging this packet approves only the trial
boundary and review record; it does not authorize changes to either operational
system.

## Proposition

> Supported context does not transfer authority.

FET-001 tests whether a versioned Context artifact can inform an Authority
consumer without silently becoming permission to retain, disclose, recommend,
rank, or create another consequential effect.

The trial must also preserve independently authorized usefulness. An invalid or
insufficient federated artifact cannot force refusal of a separate action whose
evidence and authority do not depend on that artifact.

## Review order

1. Read the [normative protocol](protocol.v0.1.md).
2. Compare its [machine-readable mirror](protocol.v0.1.json).
3. Inspect the Context [transport envelope schema](schemas/context-envelope.v0.1.schema.json).
4. Inspect the public [development cases](fixtures/development-cases.v0.1.json)
   and [mutation catalog](fixtures/mutations.v0.1.json).
5. Review the case, mutation, report, protocol, and freeze schemas.
6. Verify the [freeze manifest](freeze-manifest.v0.1.json) with the catalog
   validator.

## Reviewer questions

- Does every consequential effect require consumer-owned authority independent
  of the Context disposition?
- Are subject, purpose, audience, time, evidence, limitations, and integrity
  preserved across the interface?
- Can an independent authorized path remain useful when the federated route is
  rejected?
- Are Context, interface, Authority, effect, receipt, and usefulness results
  reported separately?
- Can any aggregate or prose claim erase a constituent hard failure?
- Are expiry, digest failure, disagreement, and insufficient observation kept
  visible?
- Does the mutation suite cover every obvious route from `READY` to unearned
  authority?

## Artifact map

```text
protocol.v0.1.md                 normative trial rules
protocol.v0.1.json               machine-readable protocol mirror
schemas/context-envelope...      proposed producer transport envelope
schemas/case...                  public development-case format
schemas/mutation...              injected-fault format
schemas/report...                separated result format
schemas/protocol...              protocol mirror schema
schemas/freeze-manifest...       frozen-packet schema
fixtures/development-cases...    public examples, not blind evidence
fixtures/mutations...            required fault operators
freeze-manifest.v0.1.json        artifact and baseline digests
```

## Validation

From the catalog root:

```bash
python scripts/validate_catalog.py
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

Validation is offline. It checks schemas, identifiers, envelope digests,
cross-artifact references, baseline identities, and the frozen artifact set.

## Public claim boundary

Passing validation means the review packet is internally consistent and
content-addressed. It does not establish that the proposed interface is useful,
safe, complete, independently reviewed, or implemented correctly.

All cases and identities are synthetic. This packet contains no private
ontology, symbolic registry, derivation rule, correspondence, production data,
credentials, or sealed evaluation material.
