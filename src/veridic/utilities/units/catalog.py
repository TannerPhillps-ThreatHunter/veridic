"""Canonical experimental Veridic units.

This is a minimal catalog required by current domain-law research.
It is not intended to be an exhaustive physical-unit ontology.
"""

from __future__ import annotations

from fractions import Fraction

from ..dimensions import (
    COUNT,
    DATA,
    DIMENSIONLESS,
    LENGTH,
    TEMPERATURE,
    TIME,
)
from .model import Unit
from .registry import UnitRegistry


ONE = Unit(
    name="one",
    symbol="1",
    dimension=DIMENSIONLESS,
)

SECOND = Unit(
    name="second",
    symbol="s",
    dimension=TIME,
)

MILLISECOND = Unit(
    name="millisecond",
    symbol="ms",
    dimension=TIME,
    scale=Fraction(1, 1000),
)

MINUTE = Unit(
    name="minute",
    symbol="min",
    dimension=TIME,
    scale=Fraction(60),
)

HOUR = Unit(
    name="hour",
    symbol="h",
    dimension=TIME,
    scale=Fraction(3600),
)

METER = Unit(
    name="meter",
    symbol="m",
    dimension=LENGTH,
)

KILOMETER = Unit(
    name="kilometer",
    symbol="km",
    dimension=LENGTH,
    scale=Fraction(1000),
)

BYTE = Unit(
    name="byte",
    symbol="B",
    dimension=DATA,
)

KILOBYTE = Unit(
    name="kilobyte",
    symbol="kB",
    dimension=DATA,
    scale=Fraction(1000),
)

BIT = Unit(
    name="bit",
    symbol="bit",
    dimension=DATA,
    scale=Fraction(1, 8),
)

ITEM = Unit(
    name="item",
    symbol="item",
    dimension=COUNT,
)

KELVIN = Unit(
    name="kelvin",
    symbol="K",
    dimension=TEMPERATURE,
)

CELSIUS = Unit(
    name="degree Celsius",
    symbol="degC",
    dimension=TEMPERATURE,
    scale=Fraction(1),
    offset=Fraction(
        27315,
        100,
    ),
)

DELTA_CELSIUS = Unit(
    name="delta degree Celsius",
    symbol="delta_degC",
    dimension=TEMPERATURE,
)

DATA_RATE = BYTE / SECOND

DEFAULT_UNIT_REGISTRY = UnitRegistry()

for _unit in (
    ONE,
    SECOND,
    MILLISECOND,
    MINUTE,
    HOUR,
    METER,
    KILOMETER,
    BYTE,
    KILOBYTE,
    BIT,
    ITEM,
    KELVIN,
    CELSIUS,
    DELTA_CELSIUS,
    DATA_RATE,
):
    DEFAULT_UNIT_REGISTRY.register(
        _unit
    )


__all__ = [
    "BIT",
    "BYTE",
    "CELSIUS",
    "DATA_RATE",
    "DEFAULT_UNIT_REGISTRY",
    "DELTA_CELSIUS",
    "HOUR",
    "ITEM",
    "KELVIN",
    "KILOBYTE",
    "KILOMETER",
    "METER",
    "MILLISECOND",
    "MINUTE",
    "ONE",
    "SECOND",
]
