"""Native dimensional algebra.

A Dimension is represented as a normalized product of named base
dimensions raised to rational powers.

Examples:

    Time
    Length
    Data

    Length / Time
    Data / Time
    Length ** 2

Internally:

    Data / Time

becomes:

    {
        "Data": 1,
        "Time": -1,
    }

No physical-unit library is required.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Self


Exponent = Fraction


@dataclass(frozen=True, slots=True)
class Dimension:
    """Immutable normalized dimensional signature."""

    powers: tuple[
        tuple[str, Exponent],
        ...,
    ] = ()

    def __post_init__(self) -> None:
        normalized: dict[
            str,
            Exponent,
        ] = {}

        for name, exponent in self.powers:
            if not name:
                raise ValueError(
                    "Base dimension name cannot be empty"
                )

            value = Fraction(exponent)

            if value == 0:
                continue

            normalized[name] = (
                normalized.get(
                    name,
                    Fraction(0),
                )
                + value
            )

            if normalized[name] == 0:
                del normalized[name]

        canonical = tuple(
            sorted(
                normalized.items()
            )
        )

        object.__setattr__(
            self,
            "powers",
            canonical,
        )

    @classmethod
    def base(
        cls,
        name: str,
    ) -> Self:
        return cls(
            (
                (
                    name,
                    Fraction(1),
                ),
            )
        )

    @classmethod
    def dimensionless(cls) -> Self:
        return cls()

    @property
    def is_dimensionless(self) -> bool:
        return not self.powers

    def exponent(
        self,
        name: str,
    ) -> Exponent:
        for dimension, exponent in self.powers:
            if dimension == name:
                return exponent

        return Fraction(0)

    def __mul__(
        self,
        other: Dimension,
    ) -> Dimension:
        return Dimension(
            self.powers
            + other.powers
        )

    def __truediv__(
        self,
        other: Dimension,
    ) -> Dimension:
        inverted = tuple(
            (
                name,
                -exponent,
            )
            for name, exponent
            in other.powers
        )

        return Dimension(
            self.powers
            + inverted
        )

    def __pow__(
        self,
        exponent: int | Fraction,
    ) -> Dimension:
        power = Fraction(exponent)

        return Dimension(
            tuple(
                (
                    name,
                    current * power,
                )
                for name, current
                in self.powers
            )
        )

    def __str__(self) -> str:
        if self.is_dimensionless:
            return "1"

        numerator: list[str] = []
        denominator: list[str] = []

        for name, exponent in self.powers:
            target = (
                numerator
                if exponent > 0
                else denominator
            )

            magnitude = abs(exponent)

            if magnitude == 1:
                target.append(name)
            else:
                target.append(
                    f"{name}^{magnitude}"
                )

        if not numerator:
            numerator_text = "1"
        else:
            numerator_text = "*".join(
                numerator
            )

        if not denominator:
            return numerator_text

        return (
            numerator_text
            + "/"
            + "*".join(denominator)
        )
