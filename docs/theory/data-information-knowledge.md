# Data -> Information -> Knowledge

## Foundational Spine

The current Veridic candidate architecture is:

    Data
        ->
    Information
        ->
    Knowledge

The transition from Information to Knowledge requires explicit
epistemic warrant:

    Information
        +
    Warrant
        =
    Knowledge

where:

    Warrant
        =
    Assertion
        |
    Derivation

---

# Data

The current candidate irreducible Data primitives are:

    Identity
    Datum
    Domain
    Relation

Data answers:

    What is represented?

Existing Veridic structures such as Field and FieldValue remain the
current executable representation while the deeper Data reduction is
tested independently.

---

# Information

The candidate irreducible Information primitive is:

    Proposition

An atomic Proposition has the form:

    P = R(t1, ..., tn)

A Proposition is truth-apt semantic content.

It says something.

For example:

    HAS_VALUE(
        event.duration,
        Duration(5 s)
    )

A Proposition can exist without Veridic accepting it as Knowledge.

Therefore:

    Information != Knowledge

---

# Open World

Absence of Information is not negative Information.

    absence(P)
        !=
    NOT P

If neither P nor NOT P is represented, evaluation is:

    UNKNOWN

This preserves Veridic's existing epistemic distinction:

    TRUE
    FALSE
    UNKNOWN

---

# Contradictory Information

An Information state may contain both:

    P

and:

    NOT P

The current three-valued Truth system cannot faithfully collapse that
state.

Phase 11 therefore preserves explicit contradiction by raising an
InformationConflict rather than choosing TRUE or FALSE.

This is evidence for a future adversarial investigation of whether
Truth itself requires a fourth state or whether contradiction belongs
to a separate support relation.

No change is made yet.

---

# Knowledge

Knowledge is warranted Information.

    Knowledge {
        identity
        proposition
        warrant
        state
    }

Knowledge identity is distinct from Proposition identity.

The same Proposition may possess multiple independent warrants.

For example:

    P:
        event.duration = 5 s

may be supported by:

    K1:
        Assertion from operator input

and independently by:

    K2:
        Derivation from event.start and event.end

Therefore:

    P(K1) == P(K2)

while:

    Identity(K1) != Identity(K2)

This permits independent corroboration without duplicating Information.

---

# Assertion

Assertion supplies external epistemic warrant.

    Assertion {
        provenance
    }

Observation, direct measurement, imported input, and nondeterministic
boundary input currently reduce to Assertion plus provenance.

---

# Derivation

Derivation supplies internal epistemic warrant.

    Derivation {
        premises
        operation
        rule
        governing_laws
    }

A Derivation must preserve enough lineage to answer:

    WHY?

    FROM WHAT?

    BY WHAT OPERATION?

    UNDER WHAT LAW?

---

# State is Orthogonal to Warrant

Knowledge may be:

    ACTIVE
    INVALID
    RETRACTED

These are lifecycle states.

They are not new forms of warrant.

An invalidated Assertion remains historically an Assertion.

An invalidated Derivation remains historically a Derivation.

Therefore:

    Warrant
        !=
    State

---

# Current Executable Layers

Phase 10 remains preserved as experimental lineage:

    KnownValue
        =
    FieldValue + Origin

Phase 11 introduces the stronger formulation:

    Knowledge
        =
    Proposition + Warrant

The old implementation is not deleted.

Both remain executable until comparative testing justifies promotion of
the deeper model.

---

# Current Candidate Laws

1. Every represented Value must retain semantic grounding.

2. Every Information item is propositionally structured.

3. Information may exist without Knowledge.

4. Every Knowledge item must contain explicit Warrant.

5. Warrant is currently either Assertion or Derivation.

6. Knowledge identity is distinct from Proposition identity.

7. Multiple independent warrants may support the same Proposition.

8. Knowledge lifecycle state is independent from warrant origin.

These remain candidate laws until broader adversarial testing supports
promotion.
