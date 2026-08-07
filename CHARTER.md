# Federated Systems Charter

## Purpose

The federation organizes public agent research as a set of bounded systems
rather than a single expanding framework. Each system must make a narrow claim
that can be independently implemented, challenged, versioned, and retired.

The catalog records how systems relate. It does not centralize their runtime,
evidence, release authority, or truth.

## Unit of organization

A system qualifies for registration when it declares:

- one governing question;
- one primary invariant;
- an exact scope and explicit non-claims;
- the evidence required to evaluate the invariant;
- versioned interfaces, if it exchanges artifacts;
- independent runtime and evaluation dependencies; and
- a public intellectual-property boundary.

A topic, metaphor, symbol, library, or implementation technique is not by
itself a system boundary.

## Independence

Every registered system must be able to:

1. publish and version its protocol independently;
2. fail without forcing another system to misreport its own result;
3. distinguish its evidence from upstream assertions;
4. reject an incompatible or insufficient input envelope;
5. name every runtime-system dependency; and
6. preserve unknown results when its observation boundary is inadequate.

An optional relationship is not a hidden dependency. A runtime dependency must
be present in both the producer and consumer manifests before a composite claim
is made.

## No implicit promotion

The federation forbids silent transfers of authority. In particular:

- retrieved information is not trusted context;
- trusted context is not a factual guarantee;
- a supported interpretation is not permission to retain it;
- permission to retain is not permission to disclose or act;
- a recommendation is not authorization for an external effect; and
- an accurate receipt cannot authorize an effect retroactively.

Every promotion requires a consumer-owned rule, declared purpose, sufficient
authority, and evidence appropriate to the new consequence.

## Claims and evidence

A system owns only its declared output claim. Consumers must preserve the
producer's version, purpose, scope, limitations, evidence references, and
expiry when present. Consumers remain responsible for their own decisions.

The catalog's validation proves structural conformance only. It does not prove
that a system's authority is legitimate, its evidence is true, its observation
boundary is complete, or its implementation is safe in production.

## Repository clusters

A system begins as one repository. It may split into a cluster when a component
has an independent release cadence, security boundary, contributor audience,
reuse boundary, or evidence-access policy. Typical cluster roles are:

- protocol;
- reference implementation;
- adapters;
- public development cases;
- sealed evaluation cases; and
- result registry.

Splitting a repository does not create a new system. Every cluster repository
must point to the same system identifier and declare its role.

## Lifecycle

Catalog states are `candidate`, `active`, `deprecated`, and `retired`.

- A candidate satisfies the manifest schema but has not completed adoption.
- An active system has adopted the federation contract on its default branch.
- A deprecated system remains readable but should not receive new consumers.
- A retired system remains in the historical registry with a final explanation.

Lifecycle changes require a catalog change and cannot rewrite prior evidence.

## Publication boundary

Public manifests describe observable behavior and system interfaces. They must
not disclose private derivation rules, symbolic registries, composition laws,
unpublished cases, private correspondence, production credentials, or personal
data.
