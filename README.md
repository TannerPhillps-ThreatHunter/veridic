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
