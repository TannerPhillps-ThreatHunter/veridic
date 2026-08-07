# Veridic

**A field-aware semantic DataFrame runtime.**

Veridic is a research and engineering project exploring a layered and
tiered model of data fields and the computational consequences of making
field semantics explicit.

The working Field model considers:

- Field Category
- Field Kind
- Field Type
- Field Scale
- Field Value
- Field Role
- Field Unit
- Field Invariants

The central research hypothesis is that DataFrame operations should operate
over both values and their field semantics.

A Veridic operation should be able to determine:

1. whether an operation is representationally executable;
2. whether the operation is semantically meaningful;
3. what Field semantics the result acquires; and
4. whether contextual invariants remain satisfied.

The initial computational model is:

    Admit -> Execute -> Transfer -> Verify

Veridic is currently experimental research. The field hierarchy,
operation algebra, and runtime semantics are not yet considered stable.

## Current Runtime

Veridic now includes an experimental `SemanticDataFrame` backed by
Polars.

```text
SemanticDataFrame
    |
    +-- SemanticSchema
    |       |
    |       +-- Field
    |
    +-- SemanticRuntime
    |
    +-- Invariant Validation
    |
    +-- Polars```
A derived column transforms both semantics and values:

FieldA x FieldB -> FieldOut
ValueA x ValueB -> ValueOut

Veridic distinguishes:

Representational Validity
    ->
Semantic Validity
    ->
Contextual Validity

See docs/theory/semantic-dataframe.md.

## Native Dimensions and Units

Veridic implements its own dependency-free dimensional and unit algebra.

```text
Dimension
    |
    +-- Time
    +-- Length
    +-- Mass
    +-- Temperature
    +-- Data
    +-- Count
    +-- Angle

Unit
    |
    +-- Dimension
    +-- Scale
    +-- Offset```
Compound units are derived algebraically:

byte / second
    ->
Data / Time

Affine units such as absolute Celsius are explicitly distinguished from
linear difference units.

## Semantic Coherence

Veridic independently derives and cross-checks semantic properties.

```text
Field Algebra
    ->
Type

Unit Algebra
    ->
Unit

Dimension Algebra
    ->
Dimension

Measurement Semantics
    ->
Scale

        |
        v

Semantic Contract

        |
        v

TRUE | FALSE | UNKNOWN```
A Field claiming DataRate with dimension Length / Time is rejected
even if its underlying values are numerically computable.

## Assertion and Derivation

Veridic distinguishes knowledge introduced into a computation from
knowledge established by computation.

```text
Assertion
    |
    v
KnownValue
    |
    v
Semantic Operation
    |
    v
Derivation```
An asserted and derived value may have identical Field semantics and
datum while remaining epistemically distinct.

Derived values retain their dependencies and governing semantic rule,
allowing Veridic to explain why they exist and invalidate them when
their premises change.

## Data -> Information -> Knowledge

Veridic now distinguishes three semantic layers:

```text
Data
    |
    v
Information
    |
    +-- Assertion
    |
    +-- Derivation
    |
    v
Knowledge```
More precisely:

Knowledge = Information + Warrant

Warrant = Assertion | Derivation

A Proposition may exist without being accepted as Knowledge, and the
same Proposition may possess multiple independent warrants.

## Truth and Epistemic Support

Veridic does not treat contradictory warrants as a fourth truth value.

```text
Truth
    TRUE
    FALSE
    UNKNOWN

Support
    NEITHER
    FOR
    AGAINST
    BOTH```
BOTH means that active warranted Knowledge exists for both a
Proposition and its negation. It represents epistemic contest, not a
declaration that the Proposition is objectively both true and false.

## Warrant Lineage

Veridic distinguishes the number of warrants from the number of
assertion-lineage groups supporting a Proposition.

```text
K1 = ASSERT P
K2 = DERIVE P FROM K1
K3 = DERIVE P FROM K1

warrant count  = 3
lineage count  = 1```
Derivation can create additional warranted Knowledge without creating a
new epistemic root.

Lineage independence is intentionally narrower than source or causal
independence.

## Representation, Warrant, and Truth

Veridic distinguishes three independent questions:

    represented(P)?
    warranted(P)?
    true(P under Interpretation)?

Representation belongs to Information.

Warrant belongs to Knowledge.

Truth is produced only by evaluating a Proposition under an
Interpretation.

    Proposition + Interpretation -> Truth

Neither represented Information nor epistemic Support is silently
promoted to Truth.

## Reduced Value Information

The Information layer no longer duplicates Field semantics inside a
second SemanticValue object.

    HAS_VALUE(Field, Datum)

Field carries semantic position and Datum carries represented content.

This is an executable reduction, not yet the final Domain-based Value
model.

## Knowledge Lifecycle

Veridic distinguishes currentness from invalidity.

    ACTIVE
    STALE
    INVALID
    RETRACTED

If a premise is invalidated or retracted, downstream Derivations become
STALE rather than INVALID. Their historical warrants remain intact, but
they no longer contribute active epistemic Support.

## Immutable Knowledge Lifecycle

Canonical Knowledge no longer stores mutable lifecycle state.

    Knowledge = Proposition + Warrant

Lifecycle is append-only:

    ACTIVE -> STALE
    ACTIVE -> INVALID
    ACTIVE -> RETRACTED

Current state is derived from immutable KnowledgeTransition history.

## Foundational Data Model Experiment

Veridic is experimentally reducing its Field-centric substrate toward:

    Identity
    Datum
    Domain
    Relation

Current Fields can be decomposed into relational structure and
reconstructed without changing the operational runtime.

The experiment is intentionally non-destructive. Field remains the
current executable semantic abstraction until the reduction survives
further adversarial testing.

## Operational CLI

Veridic now exposes its semantic runtime as a command-line tool.

    ./bin/veridic fields

    ./bin/veridic show event.duration

    ./bin/veridic resolve sub event.end event.start

    ./bin/veridic compute sub event.end=15.0 event.start=10.0

The CLI distinguishes semantic rejection from contextual invariant
failure and supports JSON output for programmatic use.
