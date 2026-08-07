# Knowledge Transition History

## Upgrade

Knowledge content and lifecycle state are orthogonal.

Phase 17 removes lifecycle state from the canonical Knowledge object.

    Knowledge {
        identity
        proposition
        warrant
    }

Knowledge therefore remains unchanged when its current usability changes.

---

# Transition

Lifecycle change is represented by:

    KnowledgeTransition {
        sequence
        knowledge
        from_state
        to_state
        reason
        cause
    }

Transitions are immutable.

They are appended rather than replacing prior lifecycle information.

---

# Current State

Current state is derived:

    state(K)
        =
    last(history(K)).to_state

The current state is therefore a projection of history.

It is not stored epistemic content.

---

# Why History Has Computational Force

Two Knowledge items may both currently be STALE while having different
histories.

Example A:

    ACTIVE
        ->
    STALE
        because premise was INVALIDATED

Example B:

    ACTIVE
        ->
    STALE
        because premise was RETRACTED

The final state alone cannot distinguish those cases.

The transition history can.

Therefore lifecycle history cannot be reduced to current state without
information loss.

---

# Sequence Is Not Time

Phase 17 records deterministic append order with a monotonic sequence.

It does not introduce:

    wall-clock time
    valid time
    transaction time
    event time

Those are separate temporal questions.

Sequence establishes ordering only.

---

# Causality

A transition may identify the Knowledge item that caused another item to
become stale.

For example:

    K:end
        RETRACTED

causes:

    K:duration
        ACTIVE -> STALE

The transition records:

    reason = premise-retracted
    cause  = K:end

This is lifecycle causation inside the Knowledge graph.

It is not a claim about real-world causality.

---

# Reduced Model

The canonical Knowledge model becomes:

    Knowledge
        =
    Proposition + Warrant

with orthogonal lifecycle:

    Lifecycle(K)
        =
    ordered immutable transitions

Thus:

    Knowledge
        !=
    KnowledgeState

and:

    current state
        =
    projection(history)
