"""Independent domain-law experiments.

These laws are derived from ordinary semantics of the represented
domains and then expressed using the Field model.

The purpose is to ask:

    Which Field dimensions are actually necessary to encode
    naturally occurring semantic behavior?
"""

from __future__ import annotations

from .dimensions import SemanticDimension as D
from .domain_law import DomainLaw
from .field import Field
from .relations import Relation, supports
from .runtime import SemanticRuntime
from .taxonomy import DEFAULT_CLASSIFICATION_REGISTRY as REGISTRY
from .utilities.units import (
    BYTE,
    CELSIUS,
    DELTA_CELSIUS,
    METER,
    SECOND,
)
from .vocabulary import Operation, Scale

# ============================================================
# TEMPORAL LAW
#
# Difference between two compatible timestamps is a duration.
# ============================================================


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


TEMPORAL_COORDINATE_DIFFERENCE = DomainLaw(
    name="domain-temporal-coordinate-difference",
    domain="Temporal",
    statement=(
        "The difference between two compatible temporal coordinates "
        "is a duration."
    ),
    operation=Operation.SUB,
    arity=2,
    depends_on=frozenset(
        {
            D.CATEGORY,
            D.KIND,
            D.TYPE,
            D.SCALE,
            D.UNIT,
        }
    ),
    admit=_timestamp_difference,
    transfer=_timestamp_difference_transfer,
)


# ============================================================
# PHYSICAL TEMPERATURE LAW
#
# Absolute Celsius temperatures are interval-scale coordinates
# on a temperature scale.
#
# T2 - T1 produces a temperature difference.
#
# The output is not another absolute Celsius temperature.
# ============================================================


def _temperature_difference(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return (
        lhs.category == rhs.category == "Physical"
        and lhs.kind == rhs.kind == "Measurement"
        and lhs.type == rhs.type == "Temperature"
        and lhs.scale is Scale.INTERVAL
        and rhs.scale is Scale.INTERVAL
        and lhs.unit == rhs.unit == CELSIUS
    )


def _temperature_difference_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    return Field(
        name=f"({lhs.name}-{rhs.name})",
        classification=REGISTRY.classify(
            "Physical",
            "Measurement",
            "TemperatureDifference",
        ),
        scale=Scale.RATIO,
        role="Derived.TemperatureDifference",
        unit=DELTA_CELSIUS,
    )


TEMPERATURE_DIFFERENCE = DomainLaw(
    name="domain-temperature-difference",
    domain="Physical",
    statement=(
        "The difference between two absolute Celsius temperatures "
        "is a temperature difference, not an absolute temperature."
    ),
    operation=Operation.SUB,
    arity=2,
    depends_on=frozenset(
        {
            D.CATEGORY,
            D.KIND,
            D.TYPE,
            D.SCALE,
            D.UNIT,
        }
    ),
    admit=_temperature_difference,
    transfer=_temperature_difference_transfer,
)


# ============================================================
# SPATIAL LAW
#
# Difference between two projected coordinates on the SAME AXIS
# yields displacement along that axis.
#
# Role is required here:
#
#   Position.X - Position.X  -> meaningful
#   Position.X - Position.Y  -> semantically incoherent
#
# even though Type, Scale, and Unit are identical.
# ============================================================


def _projected_coordinate_difference(
    fields: tuple[Field, ...],
) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return (
        lhs.category == rhs.category == "Spatial"
        and lhs.kind == rhs.kind == "Coordinate"
        and lhs.type == rhs.type == "ProjectedCoordinate"
        and lhs.scale is Scale.INTERVAL
        and rhs.scale is Scale.INTERVAL
        and lhs.unit == rhs.unit == METER
        and lhs.role == rhs.role
        and lhs.role in {"Position.X", "Position.Y"}
    )


def _projected_coordinate_difference_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    axis = lhs.role.rsplit(".", maxsplit=1)[-1]

    return Field(
        name=f"({lhs.name}-{rhs.name})",
        classification=REGISTRY.classify(
            "Spatial",
            "Measurement",
            "Displacement",
        ),
        scale=Scale.RATIO,
        role=f"Displacement.{axis}",
        unit=METER,
    )


SPATIAL_COORDINATE_DIFFERENCE = DomainLaw(
    name="domain-projected-coordinate-difference",
    domain="Spatial",
    statement=(
        "The difference between compatible projected coordinates "
        "on the same axis is displacement along that axis."
    ),
    operation=Operation.SUB,
    arity=2,
    depends_on=frozenset(
        {
            D.CATEGORY,
            D.KIND,
            D.TYPE,
            D.SCALE,
            D.UNIT,
            D.ROLE,
        }
    ),
    admit=_projected_coordinate_difference,
    transfer=_projected_coordinate_difference_transfer,
)


# ============================================================
# IDENTITY LAW
#
# Address identity permits equality comparison between values of
# the same address Type.
#
# Arithmetic is not thereby implied.
# ============================================================


def _address_equality(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return (
        lhs.category == rhs.category == "Identity"
        and lhs.kind == rhs.kind == "Address"
        and lhs.type == rhs.type
        and supports(lhs.scale, Relation.EQUALITY)
        and supports(rhs.scale, Relation.EQUALITY)
    )


ADDRESS_EQUALITY = DomainLaw(
    name="domain-address-equality",
    domain="Identity",
    statement=(
        "Addresses of the same semantic address Type support "
        "identity comparison."
    ),
    operation=Operation.EQ,
    arity=2,
    depends_on=frozenset(
        {
            D.CATEGORY,
            D.KIND,
            D.TYPE,
            D.SCALE,
        }
    ),
    admit=_address_equality,
)


# ============================================================
# NETWORK QUANTITY LAW
#
# Data quantity divided by elapsed duration yields data rate.
# ============================================================


def _data_rate(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    amount, duration = fields

    return (
        amount.category == "Quantitative"
        and amount.kind == "Measurement"
        and amount.type == "ByteCount"
        and amount.scale is Scale.RATIO
        and amount.unit == BYTE
        and duration.category == "Temporal"
        and duration.kind == "Measurement"
        and duration.type == "Duration"
        and duration.scale is Scale.RATIO
        and duration.unit == SECOND
    )


def _data_rate_transfer(
    fields: tuple[Field, ...],
) -> Field:
    amount, duration = fields

    assert amount.unit is not None
    assert duration.unit is not None

    return Field(
        name=f"({amount.name}/{duration.name})",
        classification=REGISTRY.classify(
            "Quantitative",
            "Rate",
            "DataRate",
        ),
        scale=Scale.RATIO,
        role="Derived.DataRate",
        unit=(
            amount.unit
            / duration.unit
        ),
    )


NETWORK_DATA_RATE = DomainLaw(
    name="domain-network-data-rate",
    domain="Network",
    statement=(
        "A data quantity divided by elapsed duration yields a data rate."
    ),
    operation=Operation.DIV,
    arity=2,
    depends_on=frozenset(
        {
            D.CATEGORY,
            D.KIND,
            D.TYPE,
            D.SCALE,
            D.UNIT,
        }
    ),
    admit=_data_rate,
    transfer=_data_rate_transfer,
)


# ============================================================
# TEMPORAL SCALING LAW
#
# A duration multiplied by a dimensionless scalar remains a
# duration.
#
# This law is intentionally separate from contextual validity.
#
#     4 seconds * 2 = 8 seconds
#
# is semantically meaningful.
#
# Whether 8 seconds may replace a particular Event.Duration is
# determined later by Role and Invariants.
# ============================================================


def _duration_scaling(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    duration, scalar = fields

    return (
        duration.category == "Temporal"
        and duration.kind == "Measurement"
        and duration.type == "Duration"
        and duration.scale is Scale.RATIO
        and duration.unit is not None
        and scalar.category == "Quantitative"
        and scalar.kind == "Measurement"
        and scalar.type == "Scalar"
        and scalar.scale is Scale.RATIO
        and scalar.unit is None
    )


def _duration_scaling_transfer(
    fields: tuple[Field, ...],
) -> Field:
    duration, scalar = fields

    return Field(
        name=f"({duration.name}*{scalar.name})",
        classification=REGISTRY.classify(
            "Temporal",
            "Measurement",
            "Duration",
        ),
        scale=Scale.RATIO,
        role="Derived.Duration",
        unit=duration.unit,
    )


DURATION_SCALING = DomainLaw(
    name="domain-duration-scaling",
    domain="Temporal",
    statement=(
        "A duration multiplied by a dimensionless scalar "
        "remains a duration."
    ),
    operation=Operation.MUL,
    arity=2,
    depends_on=frozenset(
        {
            D.CATEGORY,
            D.KIND,
            D.TYPE,
            D.SCALE,
            D.UNIT,
        }
    ),
    admit=_duration_scaling,
    transfer=_duration_scaling_transfer,
)


DOMAIN_LAWS = (
    DURATION_SCALING,
    TEMPORAL_COORDINATE_DIFFERENCE,
    TEMPERATURE_DIFFERENCE,
    SPATIAL_COORDINATE_DIFFERENCE,
    ADDRESS_EQUALITY,
    NETWORK_DATA_RATE,
)


def build_domain_runtime() -> SemanticRuntime:
    """Build a runtime from independently motivated domain laws."""

    runtime = SemanticRuntime()

    for law in DOMAIN_LAWS:
        runtime.register(law.as_operator_rule())

    return runtime
