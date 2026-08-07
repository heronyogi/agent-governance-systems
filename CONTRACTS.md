# Cross-system contract rules

## Current contract surface

Version 0.1 registers relationships and public artifact types. It does not
define a live runtime bus. Both current systems have empty runtime-system
dependency lists.

## Required envelope semantics

Any future artifact exchanged between systems must carry, directly or through
a content-addressed manifest:

- producer system identifier and version;
- artifact type and interface version;
- purpose and subject boundary;
- evidence and authority references;
- observation scope;
- limitations, disputes, and unknowns;
- creation time and expiry when applicable; and
- a stable content digest.

The consumer must reject an artifact when a required field is missing, an
interface version is incompatible, integrity cannot be checked, or the
artifact's purpose does not cover the proposed use.

## Consumer responsibility

Accepting an artifact means only that its structure and declared provenance
meet the consumer's input rules. It does not establish that:

- the producer's evidence was true;
- the producer's authority was legitimate;
- the artifact grants permission for a new action;
- the consumer may widen its purpose or audience; or
- the consumer may suppress limitations or disagreement.

The consuming system owns every downstream promotion and consequence.

## Failure behavior

Interface failure must be visible in the consumer's result. When the consumer
cannot determine compatibility, authority, freshness, or scope, it must not
report successful cross-system conformance.

This rule does not require universal refusal. A consumer may continue using an
independent path whose authority and evidence do not depend on the failed
artifact.

## Composite claims

A composite claim must report each participating system's result separately,
then name the rule used to combine them. No aggregate score may erase a hard
failure in a constituent invariant.
