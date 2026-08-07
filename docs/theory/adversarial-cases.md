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
