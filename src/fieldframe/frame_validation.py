"""DataFrame-level contextual invariant validation."""

from __future__ import annotations

from dataclasses import dataclass

from .validation import (
    InvariantCheck,
    ValidationReport,
)


@dataclass(frozen=True, slots=True)
class RowValidation:
    """Invariant result for one DataFrame row."""

    row_index: int
    report: ValidationReport


@dataclass(frozen=True, slots=True)
class FrameViolation:
    """One contextual invariant violation."""

    row_index: int
    check: InvariantCheck


@dataclass(frozen=True, slots=True)
class FrameValidationReport:
    """Aggregate contextual validity over a DataFrame."""

    rows: tuple[RowValidation, ...]

    @property
    def violations(
        self,
    ) -> tuple[FrameViolation, ...]:
        result: list[FrameViolation] = []

        for row in self.rows:
            for check in row.report.violations:
                result.append(
                    FrameViolation(
                        row_index=row.row_index,
                        check=check,
                    )
                )

        return tuple(result)

    @property
    def unresolved(
        self,
    ) -> tuple[tuple[int, InvariantCheck], ...]:
        result: list[
            tuple[int, InvariantCheck]
        ] = []

        for row in self.rows:
            for check in row.report.unresolved:
                result.append(
                    (
                        row.row_index,
                        check,
                    )
                )

        return tuple(result)

    @property
    def is_valid(self) -> bool:
        return not self.violations

    @property
    def is_fully_verified(self) -> bool:
        return all(
            row.report.is_fully_verified
            for row in self.rows
        )
