"""Semantic record composed of instantiated Fields."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .field import FieldValue


@dataclass(frozen=True, slots=True)
class SemanticRecord:
    """A set of FieldValue instances sharing one record context."""

    values: dict[str, FieldValue]

    def __post_init__(self) -> None:
        for name, field_value in self.values.items():
            if name != field_value.field.name:
                raise ValueError(
                    "Record key must match Field name: "
                    f"{name!r} != {field_value.field.name!r}"
                )

    def context(self) -> dict[str, Any]:
        """Return the record as a semantic evaluation context."""

        return {
            name: field_value.value
            for name, field_value in self.values.items()
        }

    def get(self, name: str) -> FieldValue:
        return self.values[name]

    def replace_value(
        self,
        name: str,
        value: Any,
    ) -> SemanticRecord:
        """Replace one Value while preserving its Field definition."""

        current = self.values[name]

        updated = dict(self.values)

        updated[name] = FieldValue(
            field=current.field,
            value=value,
        )

        return SemanticRecord(updated)
