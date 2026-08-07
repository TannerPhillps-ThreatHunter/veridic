"""Native units and unit algebra."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TypeAlias

from ..dimensions import Dimension


Number: TypeAlias = int | float | Fraction


class UnitError(ValueError):
    """Base error for unit semantics."""


class DimensionMismatch(UnitError):
    """Units have incompatible dimensional signatures."""


class AffineUnitOperation(UnitError):
    """An invalid multiplicative operation involved an affine unit."""


@dataclass(frozen=True, slots=True)
class Unit:
    """A unit mapped onto a canonical dimensional coordinate.

    Conversion to canonical form:

        canonical = value * scale + offset

    Linear units have:

        offset == 0

    Affine units such as degrees Celsius have:

        offset != 0

    Affine units cannot safely participate in multiplicative unit
    algebra because their zero point is translated.
    """

    name: str
    symbol: str
    dimension: Dimension

    scale: Fraction = Fraction(1)
    offset: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError(
                "Unit name cannot be empty"
            )

        if not self.symbol:
            raise ValueError(
                "Unit symbol cannot be empty"
            )

        if self.scale == 0:
            raise ValueError(
                "Unit scale cannot be zero"
            )

    @property
    def is_affine(self) -> bool:
        return self.offset != 0

    @property
    def is_linear(self) -> bool:
        return not self.is_affine

    def to_canonical(
        self,
        value: Number,
    ) -> Number:
        return (
            value * self.scale
            + self.offset
        )

    def from_canonical(
        self,
        value: Number,
    ) -> Number:
        return (
            value - self.offset
        ) / self.scale

    def convert_value_to(
        self,
        value: Number,
        target: Unit,
    ) -> Number:
        if self.dimension != target.dimension:
            raise DimensionMismatch(
                f"{self.dimension} cannot convert "
                f"to {target.dimension}"
            )

        canonical = self.to_canonical(
            value
        )

        return target.from_canonical(
            canonical
        )

    def _require_linear(
        self,
        other: Unit | None = None,
    ) -> None:
        if self.is_affine:
            raise AffineUnitOperation(
                f"{self.name} is affine and cannot "
                "participate in multiplicative unit algebra"
            )

        if (
            other is not None
            and other.is_affine
        ):
            raise AffineUnitOperation(
                f"{other.name} is affine and cannot "
                "participate in multiplicative unit algebra"
            )

    def __mul__(
        self,
        other: Unit,
    ) -> Unit:
        self._require_linear(other)

        return Unit(
            name=(
                f"{self.name}*"
                f"{other.name}"
            ),
            symbol=(
                f"{self.symbol}*"
                f"{other.symbol}"
            ),
            dimension=(
                self.dimension
                * other.dimension
            ),
            scale=(
                self.scale
                * other.scale
            ),
        )

    def __truediv__(
        self,
        other: Unit,
    ) -> Unit:
        self._require_linear(other)

        return Unit(
            name=(
                f"{self.name}/"
                f"{other.name}"
            ),
            symbol=(
                f"{self.symbol}/"
                f"{other.symbol}"
            ),
            dimension=(
                self.dimension
                / other.dimension
            ),
            scale=(
                self.scale
                / other.scale
            ),
        )

    def __pow__(
        self,
        exponent: int,
    ) -> Unit:
        self._require_linear()

        return Unit(
            name=f"{self.name}^{exponent}",
            symbol=f"{self.symbol}^{exponent}",
            dimension=(
                self.dimension
                ** exponent
            ),
            scale=(
                self.scale
                ** exponent
            ),
        )
