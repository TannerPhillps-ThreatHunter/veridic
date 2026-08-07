"""Minimal FieldFrame SemanticDataFrame example."""

from fieldframe.catalog import (
    BYTE_COUNT,
    DURATION,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from fieldframe.dataframe import SemanticDataFrame
from fieldframe.domain_catalog import (
    DIMENSIONLESS_SCALAR,
)
from fieldframe.errors import (
    ContextualValidationError,
)
from fieldframe.vocabulary import Operation


frame = SemanticDataFrame.from_data(
    {
        "event.start": [
            10.0,
            20.0,
        ],
        "event.end": [
            14.0,
            25.0,
        ],
        "event.duration": [
            4.0,
            5.0,
        ],
        "network.bytes": [
            400.0,
            1000.0,
        ],
        "scalar.multiplier": [
            2.0,
            2.0,
        ],
    },
    {
        "event.start": TIMESTAMP_START,
        "event.end": TIMESTAMP_END,
        "event.duration": DURATION,
        "network.bytes": BYTE_COUNT,
        "scalar.multiplier": (
            DIMENSIONLESS_SCALAR
        ),
    },
)

print(frame)
print()
print(frame.to_polars())

rate = frame.derive(
    "network.rate",
    Operation.DIV,
    "network.bytes",
    "event.duration",
)

print()
print(rate.to_polars())

scaled = frame.derive(
    "scaled.duration",
    Operation.MUL,
    "event.duration",
    "scalar.multiplier",
)

print()
print(scaled.to_polars())

try:
    frame.assign_values(
        "event.duration",
        scaled.to_polars()[
            "scaled.duration"
        ],
    )
except ContextualValidationError as exc:
    print()
    print(
        "Contextual assignment rejected:"
    )
    print(exc)
