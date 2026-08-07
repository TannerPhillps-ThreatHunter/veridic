"""Executable invariant validation."""

from __future__ import annotations

from dataclasses import dataclass

from .field import FieldValue
from .invariant import Invariant, InvariantScope
from .record import SemanticRecord


@dataclass(frozen=True, slots=True)
class InvariantCheck:
    """Result of evaluating one Invariant."""

    field_name: str
    invariant_name: str
    expression: str
    scope: InvariantScope
    result: bool | None

    @property
    def satisfied(self) -> bool:
        return self.result is True

    @property
    def violated(self) -> bool:
        return self.result is False

    @property
    def unresolved(self) -> bool:
        return self.result is None


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Aggregate invariant evaluation report."""

    checks: tuple[InvariantCheck, ...]

    @property
    def violations(self) -> tuple[InvariantCheck, ...]:
        return tuple(
            check
            for check in self.checks
            if check.violated
        )

    @property
    def unresolved(self) -> tuple[InvariantCheck, ...]:
        return tuple(
            check
            for check in self.checks
            if check.unresolved
        )

    @property
    def is_valid(self) -> bool:
        """No known invariant is violated."""

        return not self.violations

    @property
    def is_fully_verified(self) -> bool:
        """Every invariant has been evaluated and satisfied."""

        return bool(self.checks) and all(
            check.satisfied
            for check in self.checks
        )


def _check(
    field_value: FieldValue,
    invariant: Invariant,
    context: dict[str, object],
) -> InvariantCheck:
    evaluation_context = dict(context)

    evaluation_context["value"] = field_value.value

    result = invariant.evaluate(
        evaluation_context
    )

    return InvariantCheck(
        field_name=field_value.field.name,
        invariant_name=invariant.name,
        expression=invariant.expression,
        scope=invariant.scope,
        result=result,
    )


def validate_field_value(
    field_value: FieldValue,
    *,
    context: dict[str, object] | None = None,
) -> ValidationReport:
    """Validate one FieldValue.

    Relational invariants may remain unresolved when no surrounding
    record context is supplied.
    """

    evaluation_context = (
        dict(context)
        if context is not None
        else {}
    )

    checks = tuple(
        _check(
            field_value,
            invariant,
            evaluation_context,
        )
        for invariant in field_value.field.invariants
    )

    return ValidationReport(checks)


def validate_record(
    record: SemanticRecord,
) -> ValidationReport:
    """Evaluate all Field invariants against one record."""

    context = record.context()

    checks: list[InvariantCheck] = []

    for field_value in record.values.values():
        for invariant in field_value.field.invariants:
            checks.append(
                _check(
                    field_value,
                    invariant,
                    context,
                )
            )

    return ValidationReport(tuple(checks))
