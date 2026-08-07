"""Primitive vocabulary used by the Field model."""

from __future__ import annotations

from enum import Enum


class Scale(str, Enum):
    """Initial measurement-scale vocabulary.

    NOIR is a starting point, not assumed to be exhaustive.
    """

    NOMINAL = "nominal"
    ORDINAL = "ordinal"
    INTERVAL = "interval"
    RATIO = "ratio"


class Operation(str, Enum):
    """Initial semantic operations."""

    EQ = "eq"
    NE = "ne"

    LT = "lt"
    LE = "le"
    GT = "gt"
    GE = "ge"

    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"

    COUNT = "count"
    SUM = "sum"
    MEAN = "mean"
    MIN = "min"
    MAX = "max"


class ValidityLevel(str, Enum):
    """Three distinct validity thresholds."""

    REPRESENTATIONAL = "representational"
    SEMANTIC = "semantic"
    CONTEXTUAL = "contextual"
