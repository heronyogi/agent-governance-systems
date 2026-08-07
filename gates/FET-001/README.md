# FET-001 gate records

## Implementation gate

## Decision

This gate opens FET-001 for two separately reviewed, offline implementation
pull requests:

- a producer track in Agent Context Proof; and
- a consumer track in Agent Authority Benchmark.

The implementation gate became effective when its catalog change was merged.

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

Those conditions are now bound by the separate development-execution record.

## Development-execution gate

The development-execution gate authorizes one narrow class of evidence work:
offline execution of the eight frozen public development cases and ten active
mutations against the exact merged producer and consumer implementations.
The gate becomes effective only when its catalog change is merged. Until then,
it is a candidate decision record.

The record binds:

- implementation-gate PR #3, merge commit, record digest, and post-merge CI;
- producer PR #4, source and merge commits, source-manifest digest, and
  post-merge CI;
- consumer PR #2, source and merge commits, source-manifest digest, and
  post-merge CI;
- the byte-identical Context-envelope schema used by both systems;
- the frozen public cases, mutations, and report schema; and
- both implementation PR review surfaces at gate evaluation.

Both implementation PRs had zero conversation comments, submitted reviews,
review threads, unresolved threads, or change requests. Independent review is
therefore **not claimed**. The acceptance basis is the repository owner's two
merges with no publicly recorded blockers.

### Authorized execution

Execution must use isolated workspaces at the bound merge commits, remain
offline and synthetic, and exchange only the versioned JSON envelope across
the system boundary. It must run a clean preflight, execute all eight cases,
prove activation for all ten mutations, observe effects outside implementation
prose, and emit the separated frozen report format.

The producer's public export covers three representative Context states:
`FET001-DEV-001`, `FET001-DEV-003`, and `FET001-DEV-008`. Consumer evaluation
covers all eight frozen cases. That asymmetry must remain visible in the report
rather than being described as eight end-to-end producer exports.

### Still not authorized

This gate does not authorize live models, provider APIs, networked runtime
tools, production or personal data, real external effects, blind or sealed
cases, modification of the frozen packet or bound implementations, or an
experimental, safety, certification, or production claim.

Any supported result is only public development conformance within the exact
commits, cases, mutations, and confirmed observation scope. Independent
evaluation remains closed pending a separately governed blind case set,
independent review, and another gate record. Live evaluation remains closed.

## Public development result

The [v0.1 public development report](../../results/FET-001/public-development-v0.1/README.md)
records the bounded execution authorized by this gate. Its merge does not open
independent or live evaluation; those transitions still require the successor
conditions and a separate gate record.
