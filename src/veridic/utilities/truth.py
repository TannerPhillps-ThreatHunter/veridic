"""Three-valued epistemic truth."""

from __future__ import annotations

from enum import Enum


class Truth(str, Enum):
    """A proposition may be true, false, or unresolved."""

    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"

    def __bool__(self) -> bool:
        if self is Truth.UNKNOWN:
            raise TypeError(
                "Truth.UNKNOWN cannot be coerced to bool"
            )

        return self is Truth.TRUE

    def negate(self) -> Truth:
        if self is Truth.TRUE:
            return Truth.FALSE

        if self is Truth.FALSE:
            return Truth.TRUE

        return Truth.UNKNOWN

    def and_(self, other: Truth) -> Truth:
        if self is Truth.FALSE or other is Truth.FALSE:
            return Truth.FALSE

        if self is Truth.UNKNOWN or other is Truth.UNKNOWN:
            return Truth.UNKNOWN

        return Truth.TRUE

    def or_(self, other: Truth) -> Truth:
        if self is Truth.TRUE or other is Truth.TRUE:
            return Truth.TRUE

        if self is Truth.UNKNOWN or other is Truth.UNKNOWN:
            return Truth.UNKNOWN

        return Truth.FALSE
