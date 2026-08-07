# SemanticDataFrame

## Phase 6

FieldFrame now has its first DataFrame abstraction.

The implementation deliberately uses composition:

    SemanticDataFrame
        |
        +-- SemanticSchema
        |
        +-- SemanticRuntime
        |
        +-- Invariant Validation
        |
        +-- Polars DataFrame

Polars is the physical execution engine.

FieldFrame is the semantic execution layer.

---

# SemanticColumn

A conventional column is approximately:

    Column =
        <Name, DType, Values>

FieldFrame models:

    SemanticColumn =
        <FieldDefinition, Vector[Value]>

The Field definition is stored once.

The Values remain vectorized.

This avoids constructing one Field object per cell.

---

# SemanticSchema

The schema is not merely:

    name -> dtype

It is:

    name -> Field

where each Field carries:

    Category
    Kind
    Type
    Scale
    Unit
    Role
    Invariants

Value remains a column instance property rather than duplicated in the
schema.

---

# Execution Separation

A derived column requires two parallel transformations.

## Semantic

    operation(
        FieldA,
        FieldB
    )
        ->
    FieldOut

## Physical

    operation(
        ValuesA,
        ValuesB
    )
        ->
    ValuesOut

These are intentionally separate.

Polars performs the physical operation.

FieldFrame must first establish that the semantic operation exists.

---

# Example

Input:

    network.bytes

        Quantitative
            Measurement
                ByteCount

        Scale: Ratio
        Unit: byte

and:

    event.duration

        Temporal
            Measurement
                Duration

        Scale: Ratio
        Unit: second

Operation:

    network.bytes
        /
    event.duration

Semantic transfer:

    Quantitative
        Rate
            DataRate

    Scale: Ratio
    Unit: byte/second

Physical execution occurs only after semantic admission.

---

# Semantic Derivation Versus Assignment

FieldFrame now distinguishes:

    derive()

from:

    assign_values()

This distinction is foundational.

## derive()

Creates a new Field from an admitted semantic operation.

Example:

    event.duration * scalar

        ->
    scaled.duration

The resulting Field is:

    Temporal.Measurement.Duration

This is meaningful.

## assign_values()

Attempts to place Values into an existing Field definition and Role.

Example:

    scaled.duration
        ->
    event.duration

The Value may have the correct Type.

It may have the correct Scale.

It may have the correct Unit.

But the target Field carries:

    Role:
        Event.Duration

and invariant:

    event.duration
        =
    event.end - event.start

Therefore assignment requires contextual verification.

A semantically valid derived value can be rejected as an invalid
assignment.

---

# Three Validity Layers

The DataFrame implementation now makes the validity hierarchy concrete.

## Representational

Can Polars execute the physical operation?

## Semantic

Does FieldFrame admit the operation over the Field definitions?

## Contextual

Can the resulting Values truthfully inhabit the intended target Fields
while preserving their Invariants?

Thus:

    Polars execution success

does not imply:

    FieldFrame semantic validity

and:

    FieldFrame semantic validity

does not imply:

    contextual assignment validity

---

# Physical Versus Semantic Schema

A Polars column may report:

    Int64

while FieldFrame reports:

    Identity
        Identifier
            EmployeeIdentifier

    Scale:
        Nominal

The physical datatype answers:

    How is this represented?

The Field answers:

    What is this?

and:

    What operations preserve its meaning?

Neither replaces the other.

---

# Current Architecture

    VALUES
      |
      v
    Polars
      ^
      |
      | execute
      |
    FieldFrame Runtime
      ^
      |
      | admit / transfer
      |
    SemanticSchema
      |
      +-- Category
      +-- Kind
      +-- Type
      +-- Scale
      +-- Unit
      +-- Role
      +-- Invariants

Contextual verification evaluates instantiated Values against the
semantic obligations carried by the schema.

---

# Current Limitation

Invariant validation is row-wise and correctness-first.

This is deliberate.

The current objective is to prove the semantics.

Vectorized compilation of Invariants into Polars expressions is an
optimization and should not be attempted until the invariant semantics
are stable.

Likewise, SemanticDataFrame currently implements only enough operator
surface to test:

    derivation
    assignment
    selection
    contextual validation

It is not intended to imitate the entire Polars API.

---

# Research Result

Phase 6 establishes the first complete end-to-end path:

    Field Definition
        ->
    Semantic Admission
        ->
    Vectorized Execution
        ->
    Field Derivation
        ->
    Contextual Assignment
        ->
    Invariant Verification

This is the first point at which FieldFrame behaves as a semantic
DataFrame rather than solely as a theory runtime.
