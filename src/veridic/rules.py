"""Initial experimental Field algebra."""

from __future__ import annotations

from .contracts import DEFAULT_CONTRACT_REGISTRY
from .dimensions import SemanticDimension as D
from .field import Field
from .operator import OperatorRule
from .relations import Relation, supports
from .runtime import SemanticRuntime
from .taxonomy import DEFAULT_CLASSIFICATION_REGISTRY as REGISTRY
from .utilities.units import (
    BYTE,
    PACKET,
    SECOND,
)
from .vocabulary import Operation, Scale

CLASSIFICATION = frozenset(
    {
        D.CATEGORY,
        D.KIND,
        D.TYPE,
    }
)

MEASUREMENT = frozenset(
    {
        D.SCALE,
        D.UNIT,
    }
)


def _same_semantic_type(fields: tuple[Field, ...]) -> bool:
    if not fields:
        return False

    first = fields[0]

    return all(
        field.category == first.category
        and field.kind == first.kind
        and field.type == first.type
        for field in fields[1:]
    )


def _equality(fields: tuple[Field, ...]) -> bool:
    return (
        len(fields) == 2
        and _same_semantic_type(fields)
        and all(
            supports(field.scale, Relation.EQUALITY)
            for field in fields
        )
    )


def _ordering(fields: tuple[Field, ...]) -> bool:
    return (
        len(fields) == 2
        and _same_semantic_type(fields)
        and all(
            supports(field.scale, Relation.ORDER)
            for field in fields
        )
    )


def _timestamp_difference(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return (
        lhs.category == rhs.category == "Temporal"
        and lhs.kind == rhs.kind == "Coordinate"
        and lhs.type == rhs.type == "Timestamp"
        and lhs.scale is Scale.INTERVAL
        and rhs.scale is Scale.INTERVAL
        and lhs.unit == rhs.unit
    )


def _timestamp_difference_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    return Field(
        name=f"({lhs.name}-{rhs.name})",
        classification=REGISTRY.classify(
            "Temporal",
            "Measurement",
            "Duration",
        ),
        scale=Scale.RATIO,
        role="Derived.Duration",
        unit=lhs.unit,
    )


def _duration_addition(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return (
        lhs.category == rhs.category == "Temporal"
        and lhs.kind == rhs.kind == "Measurement"
        and lhs.type == rhs.type == "Duration"
        and lhs.scale is rhs.scale is Scale.RATIO
        and lhs.unit == rhs.unit
    )


def _duration_addition_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    return Field(
        name=f"({lhs.name}+{rhs.name})",
        classification=REGISTRY.classify(
            "Temporal",
            "Measurement",
            "Duration",
        ),
        scale=Scale.RATIO,
        role="Derived.Duration",
        unit=lhs.unit,
    )


def _byte_rate(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return (
        lhs.type == "ByteCount"
        and lhs.scale is Scale.RATIO
        and lhs.unit == BYTE
        and rhs.category == "Temporal"
        and rhs.kind == "Measurement"
        and rhs.type == "Duration"
        and rhs.scale is Scale.RATIO
        and rhs.unit == SECOND
    )


def _byte_rate_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    assert lhs.unit is not None
    assert rhs.unit is not None

    return Field(
        name=f"({lhs.name}/{rhs.name})",
        classification=REGISTRY.classify(
            "Quantitative",
            "Rate",
            "DataRate",
        ),
        scale=Scale.RATIO,
        role="Derived.DataRate",
        unit=(
            lhs.unit
            / rhs.unit
        ),
    )


def _packet_rate(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return (
        lhs.type == "PacketCount"
        and lhs.scale is Scale.RATIO
        and lhs.unit == PACKET
        and rhs.category == "Temporal"
        and rhs.kind == "Measurement"
        and rhs.type == "Duration"
        and rhs.scale is Scale.RATIO
        and rhs.unit == SECOND
    )


def _packet_rate_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    assert lhs.unit is not None
    assert rhs.unit is not None

    return Field(
        name=f"({lhs.name}/{rhs.name})",
        classification=REGISTRY.classify(
            "Quantitative",
            "Rate",
            "PacketRate",
        ),
        scale=Scale.RATIO,
        role="Derived.PacketRate",
        unit=(
            lhs.unit
            / rhs.unit
        ),
    )


def build_runtime() -> SemanticRuntime:
    runtime = SemanticRuntime(
        contracts=DEFAULT_CONTRACT_REGISTRY,
    )

    runtime.register(
        OperatorRule(
            name="same-type-equality",
            operation=Operation.EQ,
            arity=2,
            admit=_equality,
            depends_on=CLASSIFICATION
            | frozenset({D.SCALE}),
        )
    )

    for operation in (
        Operation.LT,
        Operation.LE,
        Operation.GT,
        Operation.GE,
    ):
        runtime.register(
            OperatorRule(
                name=f"ordered-{operation.value}",
                operation=operation,
                arity=2,
                admit=_ordering,
                depends_on=CLASSIFICATION
                | frozenset({D.SCALE}),
            )
        )

    runtime.register(
        OperatorRule(
            name="temporal-coordinate-difference",
            operation=Operation.SUB,
            arity=2,
            admit=_timestamp_difference,
            transfer=_timestamp_difference_transfer,
            depends_on=CLASSIFICATION | MEASUREMENT,
        )
    )

    runtime.register(
        OperatorRule(
            name="duration-addition",
            operation=Operation.ADD,
            arity=2,
            admit=_duration_addition,
            transfer=_duration_addition_transfer,
            depends_on=CLASSIFICATION | MEASUREMENT,
        )
    )

    runtime.register(
        OperatorRule(
            name="byte-count-per-duration",
            operation=Operation.DIV,
            arity=2,
            admit=_byte_rate,
            transfer=_byte_rate_transfer,
            depends_on=CLASSIFICATION | MEASUREMENT,
        )
    )

    runtime.register(
        OperatorRule(
            name="packet-count-per-duration",
            operation=Operation.DIV,
            arity=2,
            admit=_packet_rate,
            transfer=_packet_rate_transfer,
            depends_on=CLASSIFICATION | MEASUREMENT,
        )
    )

    return runtime
