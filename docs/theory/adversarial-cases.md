# Adversarial Field Cases

The Field model must survive these cases before the hierarchy is considered
stable.

## Classification

Determine whether Category, Kind, and Type remain independently useful for:

| Field | Candidate Category | Candidate Kind | Candidate Type |
|---|---|---|---|
| source.ip | Identity | Address | IPv4Address |
| event.start | Temporal | Coordinate | Timestamp |
| event.duration | Temporal | Measurement | Duration |
| packet.count | Quantitative | Counter | PacketCount |
| severity | Categorical | Classification | Severity |
| employee.id | Identity | Identifier | EmployeeIdentifier |
| temperature | Physical | Measurement | Temperature |
| latitude | Spatial | Coordinate | Latitude |
| free_text | Descriptive | Text | String |
| tags | Categorical | Collection | TagSet |
| graph.edge | Relational | Relationship | Edge |

Questions:

1. Can Category always be distinguished from Kind?
2. Can Kind always be distinguished from Type?
3. Is Kind actually a structural semantic tier, or merely a second Type tier?
4. Can one Type participate in multiple Categories?
5. Can one Field legitimately possess multiple Kinds?
6. Do the answers require hierarchy, facets, or both?

## Operation Counterexamples

The runtime must eventually explain, not merely classify:

    Timestamp - Timestamp       -> Duration
    Duration + Duration         -> Duration
    Timestamp + Duration        -> Timestamp
    ByteCount / Duration        -> DataRate
    PacketCount / Duration      -> PacketRate

while rejecting or explicitly defining:

    IPv4Address + IPv4Address
    EmployeeIdentifier * 2
    MEAN(EmployeeIdentifier)
    Severity / Severity

## Harder Cases

Research before implementing rules for:

- longitude averages near the antimeridian;
- circular quantities such as heading;
- temperature differences versus absolute temperature;
- logarithmic quantities such as decibels;
- percentages and proportions;
- probability values;
- ranks;
- scores with arbitrary zero points;
- timestamps across different calendars/time zones;
- money across currencies and valuation times;
- geographic coordinates in different CRS systems;
- null / unknown / absent values;
- probabilistic or interval-valued Fields;
- vectors and tensors;
- sets and collections;
- identifiers with meaningful lexical structure.

These cases exist specifically to break simplistic NOIR and datatype rules.

---

# Phase 2 — Explicit Hierarchy Tests

The implementation now enforces:

    Category -> Kind -> Type

as a strict three-tier classification path.

Important result:

    Temporal.Measurement
    Quantitative.Measurement
    Physical.Measurement

are distinct Kinds despite sharing the local label "Measurement".

This means classification identity is lineage-sensitive.

The next adversarial question is computational:

> Does each tier independently change operation admission or output
> semantics?

If Category, Kind, or Type never independently affects computation,
that tier may be descriptive rather than computational.

---

# Phase 3 — Computational Force

A semantic dimension is considered computationally relevant when a
controlled change to that dimension changes:

- admission;
- rule selection; or
- output Field semantics.

Controlled experiments now test Category, Kind, and Type independently.

This is evidence that the hierarchy CAN affect computation.

It is not yet evidence that the current taxonomy SHOULD be universal.

Major threat to validity:

    The rules were authored using the hierarchy.

Therefore the experiment can establish internal consistency but cannot
by itself establish that the hierarchy is necessary.

The stronger validation must come from independently derived domain
semantics.

---

# Phase 4 — Independent Domain Laws

Synthetic tier experiments are no longer the primary evidence.

Real-domain operation laws now cover:

    Temporal
    Physical
    Spatial
    Identity
    Network quantities

Current independent dimension usage:

    Category    used
    Kind        used
    Type        used
    Scale       used
    Unit        used
    Role        used

The projected-coordinate experiment provides the first natural
controlled case for Role:

    Spatial.Coordinate.ProjectedCoordinate
    Scale: Interval
    Unit: meter

with only Role changing:

    Position.X
    Position.Y

Same-axis subtraction is admitted.

Cross-axis scalar subtraction is rejected.

This provides evidence that Role can carry computational semantics
independent of Type, Scale, and Unit.

Value and Invariants remain untested as dynamic execution dimensions.
