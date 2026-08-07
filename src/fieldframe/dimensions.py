"""Semantic dimensions of a Field."""

from __future__ import annotations

from enum import Enum


class SemanticDimension(str, Enum):
    """Independent semantic responsibilities within a Field."""

    CATEGORY = "category"
    KIND = "kind"
    TYPE = "type"

    SCALE = "scale"
    UNIT = "unit"

    ROLE = "role"

    VALUE = "value"
    INVARIANTS = "invariants"
