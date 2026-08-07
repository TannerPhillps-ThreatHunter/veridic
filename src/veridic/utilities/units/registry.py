"""Native Unit registry."""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import (
    DimensionMismatch,
    Number,
    Unit,
)


class DuplicateUnit(ValueError):
    """A unit name or symbol already exists."""


class UnknownUnit(KeyError):
    """Requested unit is not registered."""


@dataclass(slots=True)
class UnitRegistry:
    """Lookup and conversion registry."""

    _by_name: dict[str, Unit] = field(
        default_factory=dict
    )

    _by_symbol: dict[str, Unit] = field(
        default_factory=dict
    )

    def register(
        self,
        unit: Unit,
    ) -> None:
        if unit.name in self._by_name:
            raise DuplicateUnit(
                unit.name
            )

        if unit.symbol in self._by_symbol:
            raise DuplicateUnit(
                unit.symbol
            )

        self._by_name[
            unit.name
        ] = unit

        self._by_symbol[
            unit.symbol
        ] = unit

    def resolve(
        self,
        identifier: str,
    ) -> Unit:
        if identifier in self._by_name:
            return self._by_name[
                identifier
            ]

        if identifier in self._by_symbol:
            return self._by_symbol[
                identifier
            ]

        raise UnknownUnit(
            identifier
        )

    def convert(
        self,
        value: Number,
        source: str | Unit,
        target: str | Unit,
    ) -> Number:
        source_unit = (
            self.resolve(source)
            if isinstance(source, str)
            else source
        )

        target_unit = (
            self.resolve(target)
            if isinstance(target, str)
            else target
        )

        if (
            source_unit.dimension
            != target_unit.dimension
        ):
            raise DimensionMismatch(
                f"{source_unit.name} cannot convert "
                f"to {target_unit.name}"
            )

        return source_unit.convert_value_to(
            value,
            target_unit,
        )

    def units(self) -> tuple[Unit, ...]:
        return tuple(
            sorted(
                self._by_name.values(),
                key=lambda unit: unit.name,
            )
        )
