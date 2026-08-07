"""Semantic operation runtime.

Pipeline:

    Resolve
        ->
    Verify Inputs
        ->
    Admit
        ->
    Transfer
        ->
    Verify Output

Execution and contextual invariant verification remain separate layers.
"""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import (
    ContractRegistry,
)
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

    def __init__(
        self,
        *,
        contracts: ContractRegistry | None = None,
    ) -> None:
        self._rules: list[
            OperatorRule
        ] = []

        self._contracts = contracts

    def register(
        self,
        rule: OperatorRule,
    ) -> None:
        self._rules.append(
            rule
        )

    @property
    def rules(
        self,
    ) -> tuple[OperatorRule, ...]:
        return tuple(
            self._rules
        )

    @property
    def contracts(
        self,
    ) -> ContractRegistry | None:
        return self._contracts

    def _verify(
        self,
        field: Field,
    ) -> None:
        if self._contracts is None:
            return

        self._contracts.assert_coherent(
            field
        )

    def resolve(
        self,
        operation: Operation,
        *fields: Field,
    ) -> Admission:
        inputs = tuple(
            fields
        )

        for field in inputs:
            self._verify(
                field
            )

        for rule in self._rules:
            if (
                rule.operation
                is not operation
            ):
                continue

            if not rule.matches(
                inputs
            ):
                continue

            output = (
                rule.transfer(inputs)
                if rule.transfer
                else None
            )

            if output is not None:
                self._verify(
                    output
                )

            return Admission(
                operation=operation,
                inputs=inputs,
                rule=rule,
                output=output,
            )

        signatures = ", ".join(
            (
                f"{field.classification_path}"
                f"[scale={field.scale.value}, "
                f"unit={field.unit_symbol!r}, "
                f"dimension={field.dimension}, "
                f"role={field.role}]"
            )
            for field in inputs
        )

        raise UndefinedOperation(
            f"{operation.value.upper()} "
            f"is undefined for: "
            f"{signatures}"
        )
