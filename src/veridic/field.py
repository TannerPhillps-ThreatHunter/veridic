"""Core Field semantic model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .hierarchy import Classification
from .invariant import Invariant
from .utilities.dimensions import Dimension
from .utilities.units import Unit
from .vocabulary import Scale


@dataclass(frozen=True, slots=True)
class Field:
    """Definition of a semantic Field.

    Classification is tiered:

        Category -> Kind -> Type

    Scale, Role, Unit, and Invariants occupy separate semantic
    responsibilities and are not forced into that hierarchy.

    Unit is a native Veridic Unit rather than textual metadata.

    Value is excluded from the shared definition:

        FieldValue = <Field, Value>
    """

    name: str
    classification: Classification
    scale: Scale
    role: str
    unit: Unit | None = None
    invariants: tuple[Invariant, ...] = field(
        default_factory=tuple
    )

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError(
                "Field name cannot be empty"
            )

        if not self.role:
            raise ValueError(
                "Field role cannot be empty"
            )

        if (
            self.unit is not None
            and not isinstance(
                self.unit,
                Unit,
            )
        ):
            raise TypeError(
                "Field.unit must be a "
                "Veridic Unit or None"
            )

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
    def dimension(
        self,
    ) -> Dimension | None:
        if self.unit is None:
            return None

        return self.unit.dimension

    @property
    def unit_name(
        self,
    ) -> str | None:
        if self.unit is None:
            return None

        return self.unit.name

    @property
    def unit_symbol(
        self,
    ) -> str | None:
        if self.unit is None:
            return None

        return self.unit.symbol

    @property
    def semantic_signature(
        self,
    ) -> tuple[
        str,
        str,
        str,
        Scale,
        str,
        Unit | None,
    ]:
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
