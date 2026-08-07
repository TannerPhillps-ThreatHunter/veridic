"""Core Field semantic model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .invariant import Invariant
from .vocabulary import Scale


@dataclass(frozen=True, slots=True)
class Classification:
    """Tiered semantic classification.

    category -> kind -> type

    Examples:

        Temporal -> Coordinate -> Timestamp
        Temporal -> Measurement -> Duration
        Identity -> Address -> IPv4Address
        Quantitative -> Counter -> PacketCount
    """

    category: str
    kind: str
    type: str

    def __post_init__(self) -> None:
        for name, value in (
            ("category", self.category),
            ("kind", self.kind),
            ("type", self.type),
        ):
            if not value or not value.strip():
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True, slots=True)
class Field:
    """Definition of a semantic Field.

    Value is deliberately excluded from the shared Field definition.

    A DataFrame column should carry one Field definition and many values:

        Column = <Field, [v1, v2, ... vn]>

    FieldValue represents an individual instantiation.
    """

    name: str
    classification: Classification
    scale: Scale
    role: str
    unit: str | None = None
    invariants: tuple[Invariant, ...] = field(default_factory=tuple)

    @property
    def category(self) -> str:
        return self.classification.category

    @property
    def kind(self) -> str:
        return self.classification.kind

    @property
    def type(self) -> str:
        return self.classification.type

    @property
    def semantic_signature(self) -> tuple[str, str, str, Scale, str, str | None]:
        """Identity-independent semantic signature."""

        return (
            self.category,
            self.kind,
            self.type,
            self.scale,
            self.role,
            self.unit,
        )


@dataclass(frozen=True, slots=True)
class FieldValue:
    """A single Field instantiation."""

    field: Field
    value: Any
