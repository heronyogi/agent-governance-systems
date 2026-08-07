# System map

## Current systems

### Context integrity

Agent Context Proof evaluates whether a repository decision is supported by
governed evidence and contracts inside a declared trust boundary. Its result is
epistemic and procedural: it does not grant permission for another system to
retain, disclose, rank, recommend, or act.

### Authority integrity

Agent Authority Benchmark evaluates whether observed consequential effects
remained inside a declared authority and observation boundary. Its result does
not establish that an upstream interpretation was true or that real-world
authority was legitimate.

### Relationship

The systems are siblings with no runtime dependency. A future adapter could
present a context-integrity artifact to an authority-integrity implementation,
but the latter would still need its own purpose-specific permission and effect
rules.

## Candidate future boundaries

These entries are architectural hypotheses, not registered systems or public
claims.

| Candidate | Governing question | Boundary risk |
|---|---|---|
| Memory governance | What may persist, change, be disputed, or be withdrawn? | Collapsing record, interpretation, permission, and current reliance |
| Propagation governance | What may cross between people, agents, tools, and audiences? | Treating local permission as transferable authority |
| Consequence evidence | What occurred, where did it propagate, and does the receipt match reality? | Confusing observability or remediation with prevention |

A candidate becomes a registered system only after its invariant, evidence
discipline, interfaces, and non-claims are independently specified.

## Cluster growth

Keep a system in one repository until at least one component requires a distinct
release cadence, access boundary, security posture, contributor audience, or
reuse contract. When a split occurs, every repository keeps the same
`system_id` and declares a different `repository_role`.
