"""Semantic operation runtime.

Current pipeline:

    Resolve -> Admit -> Transfer

Execution and invariant verification will be added only after the
semantic algebra is stable enough to justify them.
"""

from __future__ import annotations

from dataclasses import dataclass

from .errors import UndefinedOperation
from .field import Field
from .operator import OperatorRule
from .vocabulary import Operation


@dataclass(frozen=True, slots=True)
class Admission:
    operation: Operation
    inputs: tuple[Field, ...]
    rule: OperatorRule
    output: Field | None


class SemanticRuntime:
    """Registry-driven Field operation engine."""

    def __init__(self) -> None:
        self._rules: list[OperatorRule] = []

    def register(self, rule: OperatorRule) -> None:
        self._rules.append(rule)

    def resolve(
        self,
        operation: Operation,
        *fields: Field,
    ) -> Admission:
        inputs = tuple(fields)

        for rule in self._rules:
            if rule.operation is not operation:
                continue

            if not rule.matches(inputs):
                continue

            output = rule.transfer(inputs) if rule.transfer else None

            return Admission(
                operation=operation,
                inputs=inputs,
                rule=rule,
                output=output,
            )

        signatures = ", ".join(
            (
                f"{f.category}.{f.kind}.{f.type}"
                f"[scale={f.scale.value}, unit={f.unit!r}, role={f.role}]"
            )
            for f in inputs
        )

        raise UndefinedOperation(
            f"{operation.value.upper()} is undefined for: {signatures}"
        )
