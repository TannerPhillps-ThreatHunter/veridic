"""Core Field semantic model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .hierarchy import Classification
from .invariant import Invariant
from .vocabulary import Scale


@dataclass(frozen=True, slots=True)
class Field:
    """Definition of a semantic Field.

    Classification is tiered:

        Category -> Kind -> Type

    Scale, Role, Unit, and Invariants occupy separate semantic
    responsibilities and are not forced into that hierarchy.

    Value is excluded from the shared definition because a DataFrame
    column carries one Field definition and many values:

        Column = <Field, [v1, v2, ... vn]>
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
    def classification_path(self) -> str:
        return self.classification.path

    @property
    def semantic_signature(
        self,
    ) -> tuple[str, str, str, Scale, str, str | None]:
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
