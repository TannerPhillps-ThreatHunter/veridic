"""Small experimental Field catalog.

These are fixtures for theory testing, not a canonical ontology.
"""

from __future__ import annotations

from .field import Field
from .invariant import Invariant, InvariantScope
from .taxonomy import DEFAULT_CLASSIFICATION_REGISTRY as REGISTRY
from .vocabulary import Scale


def _classification(
    category: str,
    kind: str,
    type_name: str,
):
    return REGISTRY.classify(category, kind, type_name)


TIMESTAMP_START = Field(
    name="event.start",
    classification=_classification(
        "Temporal",
        "Coordinate",
        "Timestamp",
    ),
    scale=Scale.INTERVAL,
    role="Event.Start",
    unit="second",
)

TIMESTAMP_END = Field(
    name="event.end",
    classification=_classification(
        "Temporal",
        "Coordinate",
        "Timestamp",
    ),
    scale=Scale.INTERVAL,
    role="Event.End",
    unit="second",
)

DURATION = Field(
    name="event.duration",
    classification=_classification(
        "Temporal",
        "Measurement",
        "Duration",
    ),
    scale=Scale.RATIO,
    role="Event.Duration",
    unit="second",
    invariants=(
        Invariant(
            name="non_negative",
            expression="value >= 0",
            scope=InvariantScope.VALUE,
            predicate=lambda context: context["value"] >= 0,
            required_keys=("value",),
        ),
        Invariant(
            name="matches_event_bounds",
            expression=(
                "event.duration == "
                "event.end - event.start"
            ),
            scope=InvariantScope.RELATIONAL,
            predicate=lambda context: (
                context["event.duration"]
                == context["event.end"]
                - context["event.start"]
            ),
            required_keys=(
                "event.start",
                "event.end",
                "event.duration",
            ),
        ),
    ),
)

SOURCE_IPV4 = Field(
    name="source.ip",
    classification=_classification(
        "Identity",
        "Address",
        "IPv4Address",
    ),
    scale=Scale.NOMINAL,
    role="Participant.Source",
)

DESTINATION_IPV4 = Field(
    name="destination.ip",
    classification=_classification(
        "Identity",
        "Address",
        "IPv4Address",
    ),
    scale=Scale.NOMINAL,
    role="Participant.Destination",
)

BYTE_COUNT = Field(
    name="network.bytes",
    classification=_classification(
        "Quantitative",
        "Measurement",
        "ByteCount",
    ),
    scale=Scale.RATIO,
    role="Network.Transferred",
    unit="byte",
)

PACKET_COUNT = Field(
    name="network.packets",
    classification=_classification(
        "Quantitative",
        "Counter",
        "PacketCount",
    ),
    scale=Scale.RATIO,
    role="Network.Transferred",
    unit="packet",
)

SEVERITY = Field(
    name="detection.severity",
    classification=_classification(
        "Categorical",
        "Classification",
        "Severity",
    ),
    scale=Scale.ORDINAL,
    role="Detection.Severity",
)

EMPLOYEE_ID = Field(
    name="employee.id",
    classification=_classification(
        "Identity",
        "Identifier",
        "EmployeeIdentifier",
    ),
    scale=Scale.NOMINAL,
    role="Employee.Identity",
)

TEMPERATURE = Field(
    name="sensor.temperature",
    classification=_classification(
        "Physical",
        "Measurement",
        "Temperature",
    ),
    scale=Scale.INTERVAL,
    role="Sensor.Measurement",
    unit="degree_Celsius",
)

LATITUDE = Field(
    name="location.latitude",
    classification=_classification(
        "Spatial",
        "Coordinate",
        "Latitude",
    ),
    scale=Scale.INTERVAL,
    role="Location.Latitude",
    unit="degree",
)

FREE_TEXT = Field(
    name="message.text",
    classification=_classification(
        "Descriptive",
        "Text",
        "FreeText",
    ),
    scale=Scale.NOMINAL,
    role="Message.Content",
)

TAG_SET = Field(
    name="record.tags",
    classification=_classification(
        "Categorical",
        "Collection",
        "TagSet",
    ),
    scale=Scale.NOMINAL,
    role="Record.Tags",
)

EDGE = Field(
    name="graph.edge",
    classification=_classification(
        "Relational",
        "Relationship",
        "Edge",
    ),
    scale=Scale.NOMINAL,
    role="Graph.Relationship",
)
