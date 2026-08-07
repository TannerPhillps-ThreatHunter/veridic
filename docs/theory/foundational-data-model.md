# Foundational Data Model Experiment

## Status

Phase 18 is an executable reduction experiment.

It does not replace the current Field runtime.

The candidate primitives are:

    Identity
    Datum
    Domain
    Relation

Derived structures include:

    Value
    RelationFact
    DataState
    Field decomposition

---

# Identity

Identity answers:

    Which particular thing is this?

Identity is distinct from identifier data.

Two equal Datum values may occur under different identities.

An Identity token in the implementation is only a runtime handle.

It is not evidence that identity itself reduces to text.

---

# Datum

Datum is represented content before complete semantic interpretation.

Equal Datum values do not imply equal identity or equal semantic value.

---

# Domain

Domain identifies a semantic possibility space.

Phase 18 deliberately keeps Domain minimal.

Its classification, scale, and unit are attached through Relations
during Field decomposition rather than embedded into Domain itself.

This creates an important unresolved question:

    Is Domain irreducible?

or can:

    Domain

ultimately reduce to:

    Identity + Relations

Phase 18 does not decide that question.

---

# Value

Value is derived:

    Value = Domain + Datum

The same Datum under different Domains yields different Values.

Therefore:

    Datum equality
        !=
    Value equality

---

# Relation

Relation is general n-ary structure:

    R(t1, ..., tn)

It can represent:

    binding
    membership
    containment
    ordering
    adjacency
    key/value association
    reference
    field/domain association

RelationFact is the derived application of a Relation to terms.

---

# Missing and Null

Missing is relational absence:

    no binding exists

Null is explicit represented content:

    binding exists
        ->
    Value(
        NullDomain,
        Datum(None)
    )

Therefore:

    missing
        !=
    null

---

# Field Reduction

The current Field can be decomposed into relational structure.

Field identity is separate from Field name.

A Field is projected through relations expressing:

    field name
    expected Domain
    Domain classification
    Domain scale
    Domain unit
    Field role
    Field invariants

The experiment proves that current Field state can round-trip through
this decomposition.

It does not yet prove that Field should be removed.

---

# Important Collision

Veridic already contains:

    veridic.relations.Relation

That existing enum represents relations preserved by measurement scale:

    equality
    order
    difference
    ratio

The foundational Relation introduced here is different.

It is a general n-ary structural relation.

These concepts must not be conflated.

A future reduction may rename the existing measurement concept to make
that distinction explicit.

---

# Current Result

Phase 18 tests the decomposition:

    Field
        ->
    Identity + Domain + Relations

and:

    FieldValue
        ->
    Field + Datum

while the deeper candidate becomes:

    Value
        =
    Domain + Datum

This is evidence that Field may be a derived operational abstraction.

It is not yet sufficient evidence to replace Field in the runtime.
