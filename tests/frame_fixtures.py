"""Reusable SemanticDataFrame fixtures."""

from __future__ import annotations

from fieldframe.catalog import (
    BYTE_COUNT,
    DURATION,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from fieldframe.dataframe import SemanticDataFrame
from fieldframe.domain_catalog import DIMENSIONLESS_SCALAR


def valid_event_frame() -> SemanticDataFrame:
    return SemanticDataFrame.from_data(
        {
            "event.start": [
                10.0,
                20.0,
                30.0,
            ],
            "event.end": [
                14.0,
                25.0,
                36.0,
            ],
            "event.duration": [
                4.0,
                5.0,
                6.0,
            ],
            "network.bytes": [
                400.0,
                1000.0,
                1200.0,
            ],
            "scalar.multiplier": [
                2.0,
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
