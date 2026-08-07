# Contextual Validity

## Phase 5 Result

Veridic now distinguishes three different questions.

# 1. Representational Validity

Can the underlying runtime execute an operation over the physical
Values?

Example:

    4.0 * 2.0

Python can execute this.

This establishes only computational capability.

---

# 2. Semantic Validity

Does the operation have a meaningful interpretation over the Fields?

Example:

    Temporal.Measurement.Duration
        *
    Quantitative.Measurement.Scalar

derives:

    Temporal.Measurement.Duration

Therefore:

    4 seconds * 2 = 8 seconds

is semantically coherent.

Compare:

    IPv4Address + IPv4Address

which remains undefined despite possible integer encodings.

---

# 3. Contextual Validity

May the resulting Value truthfully occupy a particular Field Role
inside its surrounding information structure?

Suppose:

    event.start    = 10
    event.end      = 14
    event.duration = 4

with invariant:

    event.duration = event.end - event.start

The original record satisfies:

    4 = 14 - 10

Now compute:

    4 seconds * 2 = 8 seconds

The operation itself is semantically valid.

The derived value:

    8 seconds

is a valid Duration.

But assigning it back to:

    Event.Duration

without changing the event boundaries produces:

    8 != 14 - 10

The operation remains meaningful.

The transformation becomes contextually invalid.

Therefore:

    Semantic Validity
        !=
    Contextual Validity

---

# Executable Invariants

An Invariant is treated as a semantic obligation.

An invariant may evaluate to:

    True
        obligation satisfied;

    False
        obligation violated;

    None
        insufficient context or no executable predicate.

This preserves an important distinction:

    Unknown
        !=
    True

An unresolved invariant cannot be counted as verified.

---

# Veridic Validation States

A ValidationReport currently distinguishes:

    Valid
        no evaluated invariant is violated;

    Invalid
        at least one invariant is violated;

    Fully Verified
        every invariant is executable and satisfied;

    Unresolved
        one or more invariants cannot currently be evaluated.

Thus:

    is_valid

means:

    no known contradiction

while:

    is_fully_verified

means:

    all declared obligations have been established

These are intentionally different epistemic claims.

---

# Static and Dynamic Semantics

Phase 4 identified a plausible static semantic signature:

    Category
    Kind
    Type
    Scale
    Unit
    Role

Phase 5 gives Value a different computational position.

Static operation admission can generally occur without knowing the
actual Value.

Execution cannot.

Thus:

    STATIC SEMANTICS

        Category
        Kind
        Type
        Scale
        Unit
        Role

    DYNAMIC INSTANCE

        Value

    VALIDITY OBLIGATIONS

        Invariants

This is a layered model rather than an eight-property tuple.

---

# Transformation Model

The original execution pipeline was:

    Resolve
        ->
    Admit
        ->
    Execute
        ->
    Transfer
        ->
    Verify

Phase 5 gives those terms stronger meanings.

## Resolve

Recover Field semantics.

## Admit

Determine whether the operation has a valid semantic interpretation.

## Execute

Apply the operation to concrete Values.

## Transfer

Derive the semantic Field of the result.

## Verify

Evaluate the result in its intended contextual role against applicable
Invariants.

Formally:

    o(F1, ..., Fn)
        -> Fout

and:

    o(v1, ..., vn)
        -> vout

do not yet establish:

    Ftarget(vout)

as contextually valid.

That final claim requires:

    Invariants(Ftarget, Context, vout)

to hold.

---

# Central Finding

Veridic can now represent a distinction that ordinary dtype checking
alone cannot express cleanly:

    operation is meaningful

while:

    assignment of its result here is false

That suggests Invariants are not merely validation metadata.

They participate in the semantics of transformation.

The next phase should move this from isolated records to columns and
DataFrames.
