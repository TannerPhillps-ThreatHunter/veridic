"""Small experimental Field catalog.

These are fixtures for theory testing, not a canonical ontology.
"""

from __future__ import annotations

from .field import Classification, Field
from .invariant import Invariant, InvariantScope
from .vocabulary import Scale

TIMESTAMP_START = Field(
    name="event.start",
    classification=Classification(
        category="Temporal",
        kind="Coordinate",
        type="Timestamp",
    ),
    scale=Scale.INTERVAL,
    role="Event.Start",
    unit="second",
)

TIMESTAMP_END = Field(
    name="event.end",
    classification=Classification(
        category="Temporal",
        kind="Coordinate",
        type="Timestamp",
    ),
    scale=Scale.INTERVAL,
    role="Event.End",
    unit="second",
)

DURATION = Field(
    name="event.duration",
    classification=Classification(
        category="Temporal",
        kind="Measurement",
        type="Duration",
    ),
    scale=Scale.RATIO,
    role="Event.Duration",
    unit="second",
    invariants=(
        Invariant(
            name="non_negative",
            expression="value >= 0",
            scope=InvariantScope.VALUE,
        ),
    ),
)

SOURCE_IPV4 = Field(
    name="source.ip",
    classification=Classification(
        category="Identity",
        kind="Address",
        type="IPv4Address",
    ),
    scale=Scale.NOMINAL,
    role="Participant.Source",
)

DESTINATION_IPV4 = Field(
    name="destination.ip",
    classification=Classification(
        category="Identity",
        kind="Address",
        type="IPv4Address",
    ),
    scale=Scale.NOMINAL,
    role="Participant.Destination",
)

BYTE_COUNT = Field(
    name="network.bytes",
    classification=Classification(
        category="Quantitative",
        kind="Measurement",
        type="ByteCount",
    ),
    scale=Scale.RATIO,
    role="Network.Transferred",
    unit="byte",
)

PACKET_COUNT = Field(
    name="network.packets",
    classification=Classification(
        category="Quantitative",
        kind="Counter",
        type="PacketCount",
    ),
    scale=Scale.RATIO,
    role="Network.Transferred",
    unit="packet",
)

SEVERITY = Field(
    name="detection.severity",
    classification=Classification(
        category="Categorical",
        kind="Classification",
        type="Severity",
    ),
    scale=Scale.ORDINAL,
    role="Detection.Severity",
)

EMPLOYEE_ID = Field(
    name="employee.id",
    classification=Classification(
        category="Identity",
        kind="Identifier",
        type="EmployeeIdentifier",
    ),
    scale=Scale.NOMINAL,
    role="Employee.Identity",
)
