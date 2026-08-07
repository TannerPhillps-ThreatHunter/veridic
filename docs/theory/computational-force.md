# Computational Force of Field Semantics

## Question

The Field model distinguishes:

    Category -> Kind -> Type

as three classification tiers.

A hierarchy is not justified merely because its labels are intuitive.

Each tier should either contribute independently to computation or be
recognized as descriptive metadata.

## Definition

Let:

    F

and:

    F'

be two Fields that are equivalent in every tested semantic dimension
except dimension `d`.

Write:

    F ≡d F'

to mean:

> F and F' differ only in semantic dimension d.

A dimension has **computational force** for operation `o` when:

    Result(o, F) != Result(o, F')

where the difference may occur in:

1. operation admission;
2. selected operator rule;
3. derived output classification;
4. derived Scale;
5. derived Unit;
6. resulting Role;
7. resulting Invariants.

This is a counterfactual test.

Change one semantic dimension.

Hold the others constant.

Observe whether computation changes.

## Category Experiment

Inputs:

    Temporal.Coordinate.Scalar
    Spatial.Coordinate.Scalar

All tested dimensions except Category are held constant.

For subtraction:

    Temporal.Coordinate.Scalar
        -
    Temporal.Coordinate.Scalar

derives:

    Temporal.Measurement.Difference

while:

    Spatial.Coordinate.Scalar
        -
    Spatial.Coordinate.Scalar

derives:

    Spatial.Measurement.Displacement

Therefore Category affects result semantics in the experimental algebra.

## Kind Experiment

Inputs:

    Quantitative.Counter.Scalar
    Quantitative.Measurement.Scalar

Category, Type, Scale, Unit, and Role are held constant.

For subtraction:

    Counter - Counter

derives:

    Quantitative.Measurement.CountDelta
    Scale: Interval

while:

    Measurement - Measurement

derives:

    Quantitative.Measurement.Difference
    Scale: Ratio

Therefore Kind affects result semantics in the experimental algebra.

## Type Experiment

Inputs:

    Identity.Address.IPv4Address
    Identity.Address.MACAddress

Category, Kind, Scale, Unit, and Role are held constant.

Equality is admitted for:

    IPv4Address == IPv4Address

but not for:

    IPv4Address == MACAddress

under the current exact-type equality rule.

Therefore Type affects operation admission.

## Current Result

The experiments demonstrate that a three-tier classification model
*can* possess computational force.

They do NOT yet prove that the selected Categories, Kinds, or Types form
the correct universal ontology.

The distinction is important:

    structural validity != ontological validity

Phase 3 tests the former.

The taxonomy remains provisional.

## Stronger Criterion

Eventually, Veridic should not rely on hand-authored rules merely to
make each tier appear useful.

The stronger question is:

> Do naturally occurring operations across independent domains require
> Category, Kind, and Type distinctions?

The next research phases should therefore test the hierarchy against:

- time;
- spatial coordinates;
- physical measurement;
- identity;
- networking;
- finance;
- categorical analysis;
- circular quantities;
- logarithmic quantities.

If a tier repeatedly contributes no independent semantic information in
real domains, it should be reduced or converted into a facet.
