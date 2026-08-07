"""Representative Fields for domain-law experiments."""

from __future__ import annotations

from .catalog import (
    BYTE_COUNT,
    DESTINATION_IPV4,
    DURATION,
    SOURCE_IPV4,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from .field import Field
from .taxonomy import DEFAULT_CLASSIFICATION_REGISTRY as REGISTRY
from .vocabulary import Scale

# ------------------------------------------------------------
# Physical measurement
#
# Celsius absolute temperature is treated here as interval-scale.
#
# A difference between two Celsius temperatures is a distinct
# semantic quantity from an absolute Celsius temperature.
# ------------------------------------------------------------

TEMPERATURE_C_A = Field(
    name="sensor_a.temperature",
    classification=REGISTRY.classify(
        "Physical",
        "Measurement",
        "Temperature",
    ),
    scale=Scale.INTERVAL,
    role="Sensor.Temperature",
    unit="degree_Celsius",
)

TEMPERATURE_C_B = Field(
    name="sensor_b.temperature",
    classification=REGISTRY.classify(
        "Physical",
        "Measurement",
        "Temperature",
    ),
    scale=Scale.INTERVAL,
    role="Sensor.Temperature",
    unit="degree_Celsius",
)


# ------------------------------------------------------------
# Spatial coordinates
#
# Projected coordinates are used instead of latitude/longitude
# because ordinary subtraction in a projected linear coordinate
# system is easier to define cleanly.
#
# X and Y deliberately share:
#
#   Category
#   Kind
#   Type
#   Scale
#   Unit
#
# and differ only in Role.
#
# This lets us test whether Role has natural computational force.
# ------------------------------------------------------------

POSITION_X_A = Field(
    name="position_a.x",
    classification=REGISTRY.classify(
        "Spatial",
        "Coordinate",
        "ProjectedCoordinate",
    ),
    scale=Scale.INTERVAL,
    role="Position.X",
    unit="meter",
)

POSITION_X_B = Field(
    name="position_b.x",
    classification=REGISTRY.classify(
        "Spatial",
        "Coordinate",
        "ProjectedCoordinate",
    ),
    scale=Scale.INTERVAL,
    role="Position.X",
    unit="meter",
)

POSITION_Y_A = Field(
    name="position_a.y",
    classification=REGISTRY.classify(
        "Spatial",
        "Coordinate",
        "ProjectedCoordinate",
    ),
    scale=Scale.INTERVAL,
    role="Position.Y",
    unit="meter",
)


# ------------------------------------------------------------
# Dimensionless scalar
# ------------------------------------------------------------

DIMENSIONLESS_SCALAR = Field(
    name="scalar.multiplier",
    classification=REGISTRY.classify(
        "Quantitative",
        "Measurement",
        "Scalar",
    ),
    scale=Scale.RATIO,
    role="Arithmetic.Multiplier",
    unit=None,
)


__all__ = [
    "BYTE_COUNT",
    "DESTINATION_IPV4",
    "DIMENSIONLESS_SCALAR",
    "DURATION",
    "POSITION_X_A",
    "POSITION_X_B",
    "POSITION_Y_A",
    "SOURCE_IPV4",
    "TEMPERATURE_C_A",
    "TEMPERATURE_C_B",
    "TIMESTAMP_END",
    "TIMESTAMP_START",
]
