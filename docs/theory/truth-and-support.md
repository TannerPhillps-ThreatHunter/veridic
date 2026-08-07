# Truth and Support

## Problem

Veridic permits the same Proposition to possess multiple independent
epistemic warrants.

Therefore it is possible to warrant:

    P

and independently warrant:

    NOT P

The initial temptation is to extend:

    TRUE
    FALSE
    UNKNOWN

with:

    BOTH

This phase rejects that move.

The reason is that Truth and Support answer different questions.

---

# Truth

Truth concerns the Proposition itself:

    Is P true?

Veridic currently preserves:

    TRUE
    FALSE
    UNKNOWN

No fourth Truth value is introduced.

---

# Support

Support concerns Knowledge:

    What active warranted Knowledge supports P?

and:

    What active warranted Knowledge supports NOT P?

These dimensions are independent.

Represent them as:

    S(P) = <support_for_P, support_for_NOT_P>

Each component is Boolean with respect to existence of active warrant.

Therefore four support states emerge naturally.

---

# Support States

## NEITHER

    <0, 0>

No active Knowledge warrants either P or NOT P.

This is absence of current epistemic support.

---

## FOR

    <1, 0>

At least one active Knowledge item warrants P.

No active Knowledge item warrants NOT P.

---

## AGAINST

    <0, 1>

At least one active Knowledge item warrants NOT P.

No active Knowledge item warrants P.

---

## BOTH

    <1, 1>

At least one active Knowledge item warrants P.

At least one active Knowledge item warrants NOT P.

This is epistemic contest.

It does not mean that Veridic has concluded that P is objectively both
true and false.

---

# Why BOTH Is Not Truth

Consider:

    K1:
        P
        Assertion(source=A)

    K2:
        NOT P
        Assertion(source=B)

What Veridic knows with certainty is:

    source A warrants P

and:

    source B warrants NOT P

That is a fact about the Knowledge state.

It does not by itself resolve the truth of P.

Therefore:

    support(P) = BOTH

may coexist with:

    truth(P) = UNKNOWN

without contradiction between the models.

---

# No Explosion

Opposing warrants must not cause arbitrary propositions to become
Knowledge.

From:

    warranted(P)

and:

    warranted(NOT P)

Veridic must not infer:

    warranted(Q)

for unrelated Q.

Therefore contradiction is preserved locally.

This gives Veridic a paraconsistent property at the Knowledge layer
without requiring the entire semantic runtime to adopt a new logic.

---

# Lifecycle

Only active Knowledge contributes to active Support.

Invalidated and retracted Knowledge remains historical lineage but no
longer contributes current epistemic support.

Thus:

    Warrant
        explains why Knowledge existed

    State
        determines whether that warrant is currently active

    Support
        aggregates currently active warrant around a Proposition

These concepts remain orthogonal.

---

# Multiplicity

Support is not merely Boolean internally.

Veridic retains every Knowledge identity contributing to each polarity.

Example:

    support_for:
        K1
        K2
        K3

    support_against:
        K4

The derived state is:

    BOTH

but the underlying provenance remains available for later reasoning.

This matters for:

    corroboration
    source independence
    provenance analysis
    confidence
    conflict resolution

No aggregation rule is introduced yet.

---

# Current Model

The epistemic stack is now:

    Proposition
        |
        v
    Knowledge
        |
        +-- Warrant
        |
        +-- State
        |
        v
    EpistemicSupport
        |
        +-- for
        +-- against
        |
        v
    NEITHER | FOR | AGAINST | BOTH

Truth remains separate:

    TRUE | FALSE | UNKNOWN

---

# Current Finding

The contradiction test does not justify a fourth Truth value.

It justifies an independent Support calculus.

Therefore the stronger current model is:

    Data
        ->
    Information
        ->
    Knowledge
        ->
    Support

with:

    Knowledge
        =
    Information + Warrant

and:

    Support
        =
    active warranted polarity around Information
