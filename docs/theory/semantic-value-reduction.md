# SemanticValue Reduction

## Problem

Phase 11 introduced an executable SemanticValue containing:

    classification_path
    scale
    unit
    datum

A HAS_VALUE Proposition therefore contained:

    Field
        +
    SemanticValue

But Field already carried:

    classification
    scale
    unit

The same semantic claims were represented twice.

---

# Computational Force Test

The duplicated SemanticValue properties were used only to compare the
copied semantic signature back against the Field that originally
produced them.

Therefore the structure did not contribute independent meaning.

It provided verification by duplication.

Veridic already has an independent semantic-coherence mechanism through
Field contracts.

The Information Model does not need to duplicate those claims.

---

# Reduction

Phase 15 reduces:

    HAS_VALUE(
        Field,
        SemanticValue(
            classification,
            scale,
            unit,
            datum
        )
    )

to:

    HAS_VALUE(
        Field,
        Datum
    )

The Field carries semantic position.

The Datum carries represented content.

---

# Important Limit

This reduction does not define the final Veridic Value model.

The deeper Data hypothesis remains:

    Value
        =
    Domain + Datum

That model has not yet been promoted to executable architecture.

Phase 15 only removes an unnecessary Information-layer duplication.

---

# Consequence

The same Datum may occur under different Fields:

    HAS_VALUE(
        event.duration,
        5
    )

    HAS_VALUE(
        network.bytes,
        5
    )

The represented Datum is equal.

The Information is not equal because the Fields are semantically
different.

Thus:

    Datum equality
        !=
    Proposition equality

No duplicated SemanticValue signature is required to preserve that
distinction.

---

# Current Finding

SemanticValue was a useful transitional adapter.

It is not an irreducible Information construct.

Its removal makes the executable system better match the reduced
architecture:

    Data
        ->
    Information
        ->
    Knowledge

without prematurely implementing the deeper Domain-based Value model.
