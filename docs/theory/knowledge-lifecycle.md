# Knowledge Lifecycle

## Distinction

Veridic distinguishes:

    ACTIVE

    STALE

    INVALID

    RETRACTED

These states answer different lifecycle questions.

---

# ACTIVE

The Knowledge item is currently eligible to participate as warranted
premise Knowledge.

---

# STALE

The Knowledge item was produced by a historically well-formed warrant,
but one or more premises are no longer current.

Staleness does not rewrite history.

A stale Derivation retains:

    Proposition
    Warrant
    Premises
    Operation
    Rule
    Lineage

It simply no longer participates as active Knowledge.

---

# INVALID

The Knowledge item itself is declared defective.

Invalidity applies to the target Knowledge item.

Its downstream Derivations become stale because those Derivations may
have been valid when their premise was active.

---

# RETRACTED

The Knowledge item has been explicitly withdrawn.

Retraction does not imply that the Knowledge item was always invalid.

Downstream Derivations become stale.

---

# Propagation

The refined propagation rule is:

    invalidate(K)
        ->
    state(K) = INVALID
        ->
    dependents(K) = STALE

and:

    retract(K)
        ->
    state(K) = RETRACTED
        ->
    dependents(K) = STALE

Revision of an Assertion in the legacy experimental KnowledgeStore also
marks its dependent Derivations stale.

---

# Historical Warrant

A stale Derivation still answers:

    What was derived?

    From which premises?

    By which operation?

    Under which rule?

Therefore:

    stale
        !=
    invalid

and:

    stale
        !=
    erased

This distinction preserves historical epistemic meaning while excluding
obsolete Derivations from current support.

---

# Support

Only ACTIVE Knowledge contributes to active epistemic Support.

STALE, INVALID, and RETRACTED Knowledge may remain available to
historical analysis.

Therefore Support can be evaluated over:

    current Knowledge

or:

    historical Knowledge

without changing the underlying warrants.

---

# Remaining Limitation

The current stores still mutate lifecycle state in place.

The distinction between ACTIVE, STALE, INVALID, and RETRACTED now has
computational force, but historical state transitions themselves are
not yet first-class immutable records.

That is a separate upgrade problem.

Phase 16 does not solve it.
