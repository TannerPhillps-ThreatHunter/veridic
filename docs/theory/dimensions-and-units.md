# Dimensions and Units

## Purpose

Veridic distinguishes a Field's semantic Type from its physical or
measurement Unit.

A Unit is not represented as an arbitrary string.

A Unit has dimensional structure.

For example:

    byte

has dimension:

    Data

while:

    second

has dimension:

    Time

and:

    byte / second

has dimension:

    Data * Time^-1

This structure can be derived mechanically.

---

# Dimension

A Dimension is an algebraic signature composed from named base
dimensions and rational exponents.

Examples:

    Time

    Length

    Data

    Length / Time

    Data / Time

    Length^2

Dimension algebra supports:

    multiplication
    division
    exponentiation
    cancellation

Therefore:

    Time / Time

reduces to:

    Dimensionless

and:

    Length * Time / Time

reduces to:

    Length

---

# Unit

A Unit binds:

    Name
    Symbol
    Dimension
    Scale
    Offset

to a canonical coordinate system.

Linear conversion is:

    canonical = value * scale

Affine conversion is:

    canonical = value * scale + offset

This distinction is necessary for quantities such as absolute
temperature.

---

# Absolute and Differential Temperature

Absolute Celsius temperature is affine.

    0 degC
        =
    273.15 K

A Celsius temperature difference is not affine.

    10 delta_degC
        =
    10 K difference

Therefore Veridic explicitly distinguishes:

    degree Celsius

from:

    delta degree Celsius

This aligns with the existing Field distinction:

    Temperature

versus:

    TemperatureDifference

---

# Affine Unit Restriction

Affine units cannot participate directly in multiplicative unit algebra.

For example:

    degree Celsius * second

is rejected by the Unit system.

This is not because Python cannot multiply the represented numbers.

It is because multiplying an affine coordinate scale as though it were
a linear quantity is semantically malformed.

This is another instance of:

    Can Compute
        !=
    May Meaningfully Compute

---

# Unit Derivation

Units compose algebraically.

    byte / second

derives:

    Dimension:
        Data / Time

The unit need not be registered in advance for its dimensional meaning
to exist.

This prepares Veridic for semantic transfer rules such as:

    ByteCount / Duration
        ->
    DataRate

where:

    Field classification

and:

    Unit dimensionality

are independently derived and then checked for agreement.

---

# Architectural Boundary

Dimensions and Units do not define what a Field means.

For example:

    ByteCount
    PacketCount

may both participate in ratio arithmetic, but their Field Types remain
different.

The responsibility boundary is:

    Field
        semantic meaning

    Dimension
        algebraic quantity structure

    Unit
        representation of quantity magnitude

These layers cooperate without collapsing into one another.

---

# Next Integration

The current Field model still stores:

    unit: str | None

That is deliberate.

The native Unit system is being proven independently first.

The next phase should replace unit strings with native Unit objects and
make semantic transfer rules derive Units through algebra instead of
hard-coded strings such as:

    "byte/second"

---

# Phase 8 — Field Integration

Native Units are now part of Field semantics.

The previous representation:

    Field.unit: str | None

has been removed.

The Field now requires:

    Field.unit: Unit | None

A textual unit such as:

    "second"

is rejected.

The corresponding semantic object is:

    SECOND

with:

    Name:
        second

    Symbol:
        s

    Dimension:
        Time

---

# Derived Unit Semantics

Operator transfer rules no longer hard-code compound unit strings.

Previously:

    ByteCount / Duration
        ->
    unit = "byte/second"

Now:

    ByteCount.unit / Duration.unit
        ->
    BYTE / SECOND

The compound Unit is derived by native unit algebra.

Its Dimension is independently derived:

    Data / Time

Therefore the result:

    Quantitative.Rate.DataRate

and:

    Data / Time

are produced by two distinct semantic systems.

The classification algebra answers:

    What does this result mean?

The dimensional algebra answers:

    What quantity structure does it possess?

Agreement between those systems is now testable.

---

# Field Dimensional Projection

A Field with a Unit exposes:

    Field.dimension

as the dimensional signature of that Unit.

This does not collapse Dimension into Field Type.

For example:

    ByteCount
        Type: ByteCount
        Dimension: Data

and another future Field may also possess:

    Dimension: Data

without becoming semantically identical to ByteCount.

Dimension is therefore a projection of Unit semantics rather than a
replacement for Field classification.

---

# Native Unit Enforcement

Field construction now rejects arbitrary unit strings.

This closes an important semantic escape hatch.

A Field can no longer claim:

    unit = "whatever"

without that Unit existing as a structured Veridic semantic object.

The Unit must possess:

    identity
    dimensionality
    scale
    offset

and participate in the native Unit algebra.
