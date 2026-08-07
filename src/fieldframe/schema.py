"""Semantic schema composed of Field definitions."""

from __future__ import annotations

from dataclasses import dataclass

from .field import Field


@dataclass(frozen=True, slots=True)
class SemanticSchema:
    """Ordered collection of uniquely named Field definitions."""

    fields: tuple[Field, ...]

    def __post_init__(self) -> None:
        names = [
            field.name
            for field in self.fields
        ]

        if len(names) != len(set(names)):
            raise ValueError(
                "SemanticSchema Field names must be unique"
            )

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(
            field.name
            for field in self.fields
        )

    def get(self, name: str) -> Field:
        for field in self.fields:
            if field.name == name:
                return field

        raise KeyError(name)

    def contains(self, name: str) -> bool:
        return name in self.names

    def replace(self, field: Field) -> SemanticSchema:
        """Replace or append one Field definition."""

        updated: list[Field] = []
        replaced = False

        for current in self.fields:
            if current.name == field.name:
                updated.append(field)
                replaced = True
            else:
                updated.append(current)

        if not replaced:
            updated.append(field)

        return SemanticSchema(
            tuple(updated)
        )

    def select(
        self,
        *names: str,
    ) -> SemanticSchema:
        return SemanticSchema(
            tuple(
                self.get(name)
                for name in names
            )
        )
