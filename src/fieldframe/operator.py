"""Semantic operation specification primitives."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .field import Field
from .vocabulary import Operation

AdmissionRule = Callable[[tuple[Field, ...]], bool]
TransferRule = Callable[[tuple[Field, ...]], Field]


@dataclass(frozen=True, slots=True)
class OperatorRule:
    """Semantic rule for one operation family."""

    name: str
    operation: Operation
    arity: int
    admit: AdmissionRule
    transfer: TransferRule | None = None

    def matches(self, fields: tuple[Field, ...]) -> bool:
        if len(fields) != self.arity:
            return False

        return bool(self.admit(fields))
