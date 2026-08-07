"""Immutable semantic expression model."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class UnaryOperator(str, Enum):
    NEGATE = "negate"
    NOT = "not"


class BinaryOperator(str, Enum):
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"

    EQ = "eq"
    NE = "ne"

    LT = "lt"
    LE = "le"
    GT = "gt"
    GE = "ge"

    AND = "and"
    OR = "or"


class Expression:
    """Base class for semantic expressions."""

    def dependencies(self) -> frozenset[str]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Literal(Expression):
    value: Any

    def dependencies(self) -> frozenset[str]:
        return frozenset()


@dataclass(frozen=True, slots=True)
class Reference(Expression):
    name: str

    def dependencies(self) -> frozenset[str]:
        return frozenset({self.name})


@dataclass(frozen=True, slots=True)
class Unary(Expression):
    operator: UnaryOperator
    operand: Expression

    def dependencies(self) -> frozenset[str]:
        return self.operand.dependencies()


@dataclass(frozen=True, slots=True)
class Binary(Expression):
    operator: BinaryOperator
    left: Expression
    right: Expression

    def dependencies(self) -> frozenset[str]:
        return (
            self.left.dependencies()
            | self.right.dependencies()
        )


def literal(value: Any) -> Literal:
    return Literal(value)


def ref(name: str) -> Reference:
    return Reference(name)


def binary(
    operator: BinaryOperator,
    left: Expression,
    right: Expression,
) -> Binary:
    return Binary(
        operator=operator,
        left=left,
        right=right,
    )


def add(
    left: Expression,
    right: Expression,
) -> Binary:
    return binary(
        BinaryOperator.ADD,
        left,
        right,
    )


def sub(
    left: Expression,
    right: Expression,
) -> Binary:
    return binary(
        BinaryOperator.SUB,
        left,
        right,
    )


def mul(
    left: Expression,
    right: Expression,
) -> Binary:
    return binary(
        BinaryOperator.MUL,
        left,
        right,
    )


def div(
    left: Expression,
    right: Expression,
) -> Binary:
    return binary(
        BinaryOperator.DIV,
        left,
        right,
    )


def eq(
    left: Expression,
    right: Expression,
) -> Binary:
    return binary(
        BinaryOperator.EQ,
        left,
        right,
    )
