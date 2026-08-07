"""Semantic operation specification primitives."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from .dimensions import SemanticDimension
from .field import Field
from .vocabulary import Operation

AdmissionRule = Callable[[tuple[Field, ...]], bool]
TransferRule = Callable[[tuple[Field, ...]], Field]


@dataclass(frozen=True, slots=True)
class OperatorRule:
    """Semantic rule for one operation family.

    `depends_on` declares which Field dimensions contribute to
    admission or result derivation for this rule.

    This is descriptive evidence about the rule itself; the runtime
    does not yet infer dependencies automatically.
    """

    name: str
    operation: Operation
    arity: int
    admit: AdmissionRule
    transfer: TransferRule | None = None
    depends_on: frozenset[SemanticDimension] = field(
        default_factory=frozenset
    )

    def matches(self, fields: tuple[Field, ...]) -> bool:
        if len(fields) != self.arity:
            return False

        return bool(self.admit(fields))

    def depends_on_dimension(
        self,
        dimension: SemanticDimension,
    ) -> bool:
        return dimension in self.depends_on
