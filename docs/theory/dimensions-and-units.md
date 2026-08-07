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
