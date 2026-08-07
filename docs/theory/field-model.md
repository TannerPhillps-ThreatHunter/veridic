# Field Model

## Working Hypothesis

A Field is a layered and tiered semantic structure associated with data.

Current candidate dimensions:

    Field
    |
    +-- Category
    +-- Kind
    +-- Type
    +-- Scale
    +-- Value
    +-- Role
    +-- Unit
    +-- Invariants

Classification refinement:

    Category -> Kind -> Type

This is a working research model, not yet a fixed ontology.

## Field Definition vs Field Instance

A column can efficiently be modeled as:

    Column = <FieldDefinition, Values>

where FieldDefinition carries shared semantics and Values contains the
vector of Field instances.

## Computational Hypothesis

An operation transforms both values and semantics:

    o(V1, V2) -> V3

and

    o(F1, F2) -> F3

Therefore an operator is a partial semantic function:

    o : F1 x F2 -> Fout

The operation is undefined where no semantically valid transformation
exists.
