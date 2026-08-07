# FieldFrame Agent Instructions

## Project Purpose

FieldFrame investigates whether explicit field semantics can provide a
general computational layer above conventional DataFrame datatypes.

Do not reduce the project to:
- richer dtype metadata;
- schema validation;
- unit-aware arithmetic;
- a Pandas wrapper; or
- a fixed taxonomy.

The research problem is semantic validity of computation.

## Working Field Model

The current candidate Field anatomy is:

- Category
- Kind
- Type
- Scale
- Value
- Role
- Unit
- Invariants

This structure is layered and tiered.

Classification refinement currently begins:

    Category -> Kind -> Type

Other properties occupy different semantic responsibilities and MUST NOT
be forced into a single inheritance hierarchy without justification.

## Core Runtime Hypothesis

For an operation o over Fields F1 ... Fn:

    Admit(o, F1, ... Fn)
        -> Execute(o, V1, ... Vn)
        -> Transfer(o, F1, ... Fn)
        -> Verify(Invariants)

The runtime must distinguish:

    Can Compute
    May Meaningfully Compute
    May Remain Contextually Valid

## Engineering Doctrine

1. Theory before architecture.
2. Architecture before optimization.
3. Preserve distinctions between representation and semantics.
4. Do not treat storage dtype as semantic type.
5. Do not treat NOIR as exhaustive measurement theory.
6. Invariants are semantic obligations, not merely validators.
7. Every derived column must have derivable or explicitly declared Field
   semantics.
8. Failed semantic inference must remain explicit rather than silently
   degrading to an untyped field.
9. Prefer composition over inheritance.
10. Test the model against non-security datasets as well as network
    telemetry.

## Initial Substrate

Preferred initial stack:

- Python
- Polars
- Apache Arrow
- Pint where appropriate

Do not subclass pandas.DataFrame as the foundational architecture.

## Current Research Frontier

Before implementing a broad runtime, derive and test the Field operation
algebra for:

- equality
- comparison
- addition
- subtraction
- multiplication
- division
- count
- sum
- mean
- min/max
- grouping
- joins
- casting
- unit conversion

The objective is to discover the smallest semantic model necessary to
determine valid operations and result semantics.
