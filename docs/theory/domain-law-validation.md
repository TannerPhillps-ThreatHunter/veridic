# Domain-Law Validation

## Purpose

Phase 3 demonstrated that Category, Kind, and Type *can* affect
computation.

That result was internally consistent but partially circular:

> the experimental rules were deliberately written to depend on the
> hierarchy being tested.

Phase 4 uses a stronger method.

We begin with independently motivated semantic behavior from ordinary
domains and then ask which Field dimensions are required to express
that behavior.

---

# Method

For each domain:

1. state a natural semantic law;
2. construct representative Fields;
3. express the law as an operator admission rule;
4. derive the semantic Field of the result;
5. record which Field dimensions the law requires;
6. test nearby operations that should fail.

The current domains are:

- temporal coordinates;
- physical temperature;
- projected spatial coordinates;
- identity/address semantics;
- network quantities.

---

# Temporal law

Natural-domain statement:

    timestamp - timestamp -> duration

This requires distinguishing:

    Temporal
        Coordinate
            Timestamp

from the output:

    Temporal
        Measurement
            Duration

The output also changes:

    Scale:
        Interval -> Ratio

while retaining a compatible temporal Unit.

This supports independent computational use of:

    Category
    Kind
    Type
    Scale
    Unit

---

# Temperature law

Absolute Celsius temperature is not semantically identical to a
temperature difference.

Natural-domain statement:

    absolute temperature
        -
    absolute temperature

        -> temperature difference

Input:

    Physical.Measurement.Temperature
    Scale: Interval
    Unit: degree_Celsius

Output:

    Physical.Measurement.TemperatureDifference
    Scale: Ratio
    Unit: delta_degree_Celsius

This case is important because a naïve system may represent both
inputs and output as floating-point numbers.

Representation does not preserve the distinction.

Field semantics do.

It also demonstrates that:

    Type
    Scale
    Unit

may all transform during one mathematically ordinary operation.

---

# Spatial law

Projected coordinates provide a natural test of Role.

Consider:

    position_a.x
    position_b.x
    position_a.y

All may share:

    Category: Spatial
    Kind: Coordinate
    Type: ProjectedCoordinate
    Scale: Interval
    Unit: meter

But:

    X - X

has a straightforward same-axis displacement interpretation while:

    X - Y

does not represent displacement along one common coordinate axis.

The discriminating dimension is:

    Role

Therefore Role is not merely descriptive metadata.

It can have direct computational force even when:

    Category
    Kind
    Type
    Scale
    Unit

are identical.

---

# Identity law

IPv4 addresses support identity comparison.

They do not acquire arithmetic meaning merely because their physical
representations can be encoded numerically.

Therefore:

    IPv4Address == IPv4Address

is admitted while:

    IPv4Address + IPv4Address

remains undefined.

This supports the distinction:

    representational capability
        !=
    semantic permission

---

# Network quantity law

Natural-domain statement:

    byte quantity / duration -> data rate

Input:

    Quantitative.Measurement.ByteCount
        /
    Temporal.Measurement.Duration

Output:

    Quantitative.Rate.DataRate

with:

    Scale: Ratio
    Unit: byte/second

The output Category, Kind, Type, Scale, and Unit are derived from the
semantics of the operation.

---

# Current Evidence

The domain-law experiments independently exercise:

    Category
    Kind
    Type
    Scale
    Unit
    Role

Value and Invariants are not yet required for *static admission* of
these operations.

That is not evidence that they are unnecessary.

It indicates that they occupy a different phase.

The likely emerging division is:

## Static semantic signature

    Category
    Kind
    Type
    Scale
    Unit
    Role

These dimensions influence whether an operation is meaningful and what
Field it produces.

## Dynamic semantic state

    Value
    Invariants

These dimensions become necessary when determining whether a specific
execution and resulting DataFrame remain valid.

This is a stronger layered interpretation than treating all eight
properties as peers.

---

# Current Working Architecture

    FIELD

    STATIC SEMANTICS
    |
    +-- Classification
    |   |
    |   +-- Category
    |   +-- Kind
    |   +-- Type
    |
    +-- Measurement
    |   |
    |   +-- Scale
    |   +-- Unit
    |
    +-- Context
        |
        +-- Role

    DYNAMIC SEMANTICS
    |
    +-- Value

    VALIDITY
    |
    +-- Invariants

This architecture is provisional.

Its justification must come from computational necessity rather than
symmetry.

---

# Important Result

The strongest Phase 4 result is not merely that the classification
hierarchy survived.

It is that a real spatial case establishes:

    same Category
    same Kind
    same Type
    same Scale
    same Unit
    different Role

and produces different operation validity.

Therefore:

    Role

has independent computational significance.

---

# Next Question

Static semantic admission is now reasonably well motivated.

The next unresolved layer is dynamic validity.

Example:

    duration * 2

may be semantically valid as arithmetic over Duration.

But if the Field carries the invariant:

    duration = end - start

then replacing the original connection duration with twice its value
makes the DataFrame contextually false.

The next phase should therefore make Invariants executable as
post-operation proof obligations.

That will test the distinction:

    Semantically Valid Operation

versus:

    Contextually Valid Transformation
