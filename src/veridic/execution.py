"""Semantic execution over instantiated Field values."""

from __future__ import annotations

import operator
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .field import FieldValue
from .runtime import Admission, SemanticRuntime
from .vocabulary import Operation

ValueOperator = Callable[..., Any]


_VALUE_OPERATORS: dict[Operation, ValueOperator] = {
    Operation.EQ: operator.eq,
    Operation.NE: operator.ne,
    Operation.LT: operator.lt,
    Operation.LE: operator.le,
    Operation.GT: operator.gt,
    Operation.GE: operator.ge,
    Operation.ADD: operator.add,
    Operation.SUB: operator.sub,
    Operation.MUL: operator.mul,
    Operation.DIV: operator.truediv,
}


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Result of one admitted semantic operation."""

    admission: Admission
    value: Any
    output: FieldValue | None


def execute(
    runtime: SemanticRuntime,
    operation: Operation,
    *operands: FieldValue,
) -> ExecutionResult:
    """Resolve semantic meaning, then execute over Values."""

    admission = runtime.resolve(
        operation,
        *(operand.field for operand in operands),
    )

    try:
        value_operator = _VALUE_OPERATORS[operation]
    except KeyError as exc:
        raise NotImplementedError(
            "Value execution is not implemented for "
            f"{operation.value}"
        ) from exc

    value = value_operator(
        *(operand.value for operand in operands)
    )

    output = None

    if admission.output is not None:
        output = FieldValue(
            field=admission.output,
            value=value,
        )

    return ExecutionResult(
        admission=admission,
        value=value,
        output=output,
    )
