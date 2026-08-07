"""Field-aware semantic column."""

from __future__ import annotations

from dataclasses import dataclass

import polars as pl

from .field import Field, FieldValue


@dataclass(frozen=True, slots=True)
class SemanticColumn:
    """A Polars Series governed by one Field definition."""

    field: Field
    series: pl.Series

    def __post_init__(self) -> None:
        if self.series.name != self.field.name:
            object.__setattr__(
                self,
                "series",
                self.series.rename(
                    self.field.name
                ),
            )

    def __len__(self) -> int:
        return len(self.series)

    def value_at(
        self,
        index: int,
    ) -> FieldValue:
        return FieldValue(
            field=self.field,
            value=self.series[index],
        )

    def to_polars(self) -> pl.Series:
        return self.series.clone()
