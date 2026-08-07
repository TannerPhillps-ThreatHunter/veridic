# Semantic Contracts

## Purpose

Veridic now contains multiple independently derived semantic systems.

The Field classification system determines:

    Category
    Kind
    Type

The measurement system determines:

    Scale

The dimensional system determines:

    Dimension

The Unit system determines:

    Unit
    Scale factor
    Offset

Independence is valuable because one system can check another.

The systems should not be collapsed merely to make contradictions
impossible to represent.

Instead, contradictions should be detectable.

---

# Semantic Contract

A Semantic Contract defines the measurement shape that is coherent with
a Field classification.

For example:

    Quantitative.Rate.DataRate

requires:

    Scale:
        Ratio

    Dimension:
        Data / Time

    Unit:
        Required

The contract does not state that the Unit must literally be:

    byte / second

Other compatible units may exist.

What must remain true is the dimensional relationship:

    Data / Time

---

# Independent Derivation

Consider:

    ByteCount / Duration

Field algebra derives:

    Quantitative.Rate.DataRate

Unit algebra derives:

    BYTE / SECOND

Dimension algebra derives:

    Data / Time

The DataRate contract independently expects:

    Ratio
    Data / Time
    Unit Required

Therefore all semantic systems agree.

This is a coherence proof.

---

# Contradiction

Suppose a faulty transfer rule derives:

    Type:
        DataRate

but also:

    Unit:
        meter / second

The Unit algebra derives:

    Length / Time

The DataRate contract expects:

    Data / Time

Therefore Veridic rejects the result.

The underlying numerical division may be perfectly executable.

The semantic result is internally contradictory.

---

# Three Contract Outcomes

Contract evaluation uses Veridic's native three-valued Truth system.

## TRUE

A contract exists and the Field satisfies it.

## FALSE

A contract exists and the Field contradicts it.

## UNKNOWN

No contract has yet been defined for that classification.

This distinction is deliberate.

Absence of semantic knowledge is not evidence of invalidity.

Therefore:

    UNKNOWN != FALSE

and:

    UNKNOWN != TRUE

---

# Runtime Integration

The Semantic Runtime now performs:

    Resolve
        ->
    Verify Input Contracts
        ->
    Admit Operation
        ->
    Transfer Semantics
        ->
    Verify Output Contract

Only after these static semantic stages should Value execution occur.

This creates a stronger execution model:

    Coherent Inputs
        ->
    Meaningful Operation
        ->
    Coherent Result
        ->
    Execute Values
        ->
    Verify Contextual Invariants

---

# Layered Validity

Veridic can now distinguish:

    Representational Validity

    Semantic Operation Validity

    Internal Semantic Coherence

    Value Execution

    Contextual Validity

These are not synonyms.

A computation may pass one layer and fail another.

---

# Current Contract Dimensions

The initial contracts relate:

    Type
    Scale
    Dimension
    Unit presence

Future contracts may also relate:

    Kind
    Role
    affine versus linear Unit behavior
    admissible transformations
    invariant families
    canonical expression forms

The contract system should expand only where independent semantic laws
justify the relationship.
