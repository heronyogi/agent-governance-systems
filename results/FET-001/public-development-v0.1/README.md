# FET-001 public development conformance v0.1

## Result

The bound producer and consumer implementations preserved the declared
FET-001 Authority boundary within the confirmed offline observation scope
across the eight frozen public development cases and ten active mutations.

This is a public development-conformance result. It is not independent, blind,
live, experimental, or production evidence, and it does not validate an
ontology or establish safety outside the exact commits and observation scope.
The result becomes part of the catalog only when its pull request is merged.

## Bound execution

Execution occurred on 2026-08-07 in three isolated, initially clean worktrees:

- producer `agent-context-integrity` at merge commit
  `eb5dfe0bcb998a12ed1b1a6bd1e76f492808b55c`;
- consumer `agent-authority-integrity` at merge commit
  `36464fa9980aae91288739e5fa403d5841c92e1c`; and
- execution gate `agent-governance-systems` at merge commit
  `74297d91915b88b581385905cc8d8dbd76ec2602`.

Preflight confirmed clean worktrees, exact commits, the merged gate decision,
all content-addressed inputs, and one byte-identical Context-envelope schema
across the producer, consumer, and catalog.

The producer and consumer ran as separate Python processes. The producer sent
canonical JSON through standard output and the consumer accepted it through
standard input. All three producer exports—`FET001-DEV-001`,
`FET001-DEV-003`, and `FET001-DEV-008`—were schema-valid, digest-valid, and
identical under the frozen canonical serialization to the corresponding
consumer fixtures.

The consumer then executed all eight public cases and all ten mutations from
the frozen content-addressed fixtures. A separate process validated the final
report against the frozen Draft 2020-12 report schema before publication.

Implementation identity fields ending in `_merge_commit_utf8` are SHA-256
digests of the lowercase 40-character Git commit identifier with no trailing
newline. Module identities are SHA-256 digests of the exact file bytes at the
bound merge commit.

## Observed outcomes

- all eight clean cases passed Context, interface, Authority, receipt,
  side-effect-evidence, usefulness, and false-refusal checks;
- the clean runs recorded no unauthorized committed effect;
- the rejected stale Context retained the independently authorized review path;
- the matching permission permitted the bounded synthetic publish effect;
- all ten mutations proved activation and were killed; and
- no aggregate score or constituent-failure cancellation was emitted.

Six deliberately faulted mutation variants produced a synthetic effect before
the harness detected the fault. Their `effect_occurred: true` values are
preserved in the report. Mutation detection is therefore reported as
observability success for those faulty variants, not as prevention. The clean
implementation results are reported separately.

## Observation limits

The producer exported three representative Context cases, while consumer
evaluation covered all eight frozen cases. This result does not describe all
eight as end-to-end producer exports.

All cases and expected outcomes were public authored development fixtures. No
independent reviewer, hidden oracle, blind case, live model, provider API,
production system, human recipient, or external network propagation was part
of the observation boundary.

A non-normative local `ruff format --check` used Ruff 0.16.2 against the bound
producer checkout and reported pre-existing formatting differences in files
outside the FET implementation. It made no changes. The producer's required
test suite and lint check passed, as did its bound post-merge CI; the formatting
drift is not treated as FET conformance evidence.

Independent evaluation and live evaluation remain closed.
