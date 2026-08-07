# Field Classification Hierarchy

## Working Claim

The Field classification layer is tiered:

    Category
       |
       v
      Kind
       |
       v
      Type

These tiers perform different levels of semantic refinement.

## Category

Category identifies the broad semantic domain of a Field.

Examples:

    Temporal
    Identity
    Spatial
    Quantitative
    Physical
    Categorical
    Descriptive
    Relational

Category is the least specific classification tier.

## Kind

Kind identifies the structural or semantic form a Field takes
within its Category.

Examples:

    Temporal.Coordinate
    Temporal.Measurement

    Identity.Address
    Identity.Identifier

    Quantitative.Counter
    Quantitative.Measurement
    Quantitative.Rate

Kind is Category-qualified.

The label:

    Measurement

does not identify one globally unique Kind.

These are distinct lineages:

    Temporal.Measurement
    Quantitative.Measurement
    Physical.Measurement
    Spatial.Measurement

This is deliberate.

## Type

Type identifies the most specific semantic value domain in the
classification layer.

Examples:

    Temporal.Coordinate.Timestamp
    Temporal.Measurement.Duration

    Identity.Address.IPv4Address
    Identity.Identifier.UUID

    Quantitative.Counter.PacketCount
    Quantitative.Measurement.ByteCount

    Physical.Measurement.Temperature

## Hierarchical Validity

A Type is valid only under its registered Kind.

A Kind is valid only under its registered Category.

Therefore:

    Temporal.Measurement.Duration

is valid while:

    Temporal.Coordinate.Duration

is not.

The latter combines individually meaningful labels into an invalid
semantic lineage.

## Repeated Names

Names may recur at different hierarchy paths.

For example:

    Temporal.Measurement
    Quantitative.Measurement
    Physical.Measurement

This does not collapse the hierarchy.

A node is semantically identified by its lineage, not merely its
local label.

## Structural Consequence

Classification is therefore not:

    Field.category = arbitrary tag
    Field.kind     = arbitrary tag
    Field.type     = arbitrary tag

It is:

    Field.classification =
        Category -> Kind -> Type

The hierarchy constrains which combinations can exist.

## What Is Not In This Hierarchy

The following remain separate Field layers:

    Scale
    Unit
    Role
    Value
    Invariants

They may depend on or constrain classification, but they are not
currently modeled as descendants of Type.

## Research Question

The hierarchy survives the initial cross-domain cases if all three tiers
continue to make distinct and useful contributions to:

1. operation admission;
2. result Field derivation;
3. invariant formation;
4. semantic comparison;
5. schema interoperability.

If one tier contributes no independent computational information, the
model should be reduced rather than preserved for symmetry.
