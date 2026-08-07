# FET-001 implementation gate

## Decision

This gate opens FET-001 for two separately reviewed, offline implementation
pull requests:

- a producer track in Agent Context Proof; and
- a consumer track in Agent Authority Benchmark.

The gate becomes effective only when its catalog change is merged. Until then,
it is a candidate decision record.

## Evidence

The decision binds:

- protocol source commit `ec522b8a190d51e33309e08dbc74bbc2c4e22051`;
- protocol merge commit `83ef57c750eee4da56f6c358c85e9effa45d21b7`;
- freeze-manifest SHA-256
  `1636497fa8b67bf3452f673d7b233bee428e257715722b56f6d1b237c008b4a2`;
- successful post-merge CI run
  `https://github.com/heronyogi/agent-governance-systems/actions/runs/31220113497`;
  and
- the public PR review surface at gate evaluation.

PR #2 had zero conversation comments, zero submitted reviews, zero review
threads, zero unresolved threads, and zero change requests. Independent review
is therefore **not claimed**. The acceptance basis is the repository owner's
merge with no publicly recorded blockers.

## Authorized work

The producer may implement the deterministic transport envelope and synthetic
fixtures. The consumer may implement validation, independent Authority
resolution, side-effect observation, receipts, development cases, and mutation
operators.

Each system remains responsible for its own invariant. The tracks must use
separate pull requests and preserve the frozen interface boundary.

## Not authorized

This gate does not authorize:

- a live model or provider API call;
- production or personal data;
- real external effects;
- sealed-case publication;
- a FET-001 result or safety claim;
- modification of the frozen protocol; or
- development-trial execution.

The next gate remains closed until both implementations are merged, compatible,
fully tested against the public cases and mutations, and bound by a new catalog
decision record.
