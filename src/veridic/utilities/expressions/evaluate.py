"""Evaluate Veridic semantic expressions."""

from __future__ import annotations

import operator
from collections.abc import Mapping
from typing import Any

from ..truth import Truth
from .model import (
    Binary,
    BinaryOperator,
    Expression,
    Literal,
    Reference,
    Unary,
    UnaryOperator,
)


class _Unknown:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNKNOWN"


UNKNOWN = _Unknown()


_ARITHMETIC = {
    BinaryOperator.ADD: operator.add,
    BinaryOperator.SUB: operator.sub,
    BinaryOperator.MUL: operator.mul,
    BinaryOperator.DIV: operator.truediv,
}


_COMPARISONS = {
    BinaryOperator.EQ: operator.eq,
    BinaryOperator.NE: operator.ne,
    BinaryOperator.LT: operator.lt,
    BinaryOperator.LE: operator.le,
    BinaryOperator.GT: operator.gt,
    BinaryOperator.GE: operator.ge,
}


def _truth(value: Any) -> Truth:
    if value is UNKNOWN:
        return Truth.UNKNOWN

    if isinstance(value, Truth):
        return value

    return Truth.TRUE if bool(value) else Truth.FALSE


def evaluate(
    expression: Expression,
    context: Mapping[str, Any],
) -> Any:
    """Evaluate an expression against a semantic context."""

    if isinstance(expression, Literal):
        return expression.value

    if isinstance(expression, Reference):
        return context.get(
            expression.name,
            UNKNOWN,
        )

    if isinstance(expression, Unary):
        value = evaluate(
            expression.operand,
            context,
        )

        if value is UNKNOWN:
            return UNKNOWN

        if expression.operator is UnaryOperator.NEGATE:
            return -value

        if expression.operator is UnaryOperator.NOT:
            return _truth(value).negate()

        raise ValueError(
            f"Unsupported unary operator: "
            f"{expression.operator}"
        )

    if isinstance(expression, Binary):
        left = evaluate(
            expression.left,
            context,
        )

        right = evaluate(
            expression.right,
            context,
        )

        if expression.operator in _ARITHMETIC:
            if left is UNKNOWN or right is UNKNOWN:
                return UNKNOWN

            return _ARITHMETIC[
                expression.operator
            ](
                left,
                right,
            )

        if expression.operator in _COMPARISONS:
            if left is UNKNOWN or right is UNKNOWN:
                return Truth.UNKNOWN

            result = _COMPARISONS[
                expression.operator
            ](
                left,
                right,
            )

            return (
                Truth.TRUE
                if result
                else Truth.FALSE
            )

        if expression.operator is BinaryOperator.AND:
            return _truth(left).and_(
                _truth(right)
            )

        if expression.operator is BinaryOperator.OR:
            return _truth(left).or_(
                _truth(right)
            )

        raise ValueError(
            f"Unsupported binary operator: "
            f"{expression.operator}"
        )

    raise TypeError(
        "Unknown Expression implementation: "
        f"{type(expression).__name__}"
    )
