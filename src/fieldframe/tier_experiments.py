"""Controlled experiments for classification-tier semantics.

These Fields are intentionally synthetic and MUST NOT be treated as
canonical FieldFrame taxonomy.

They exist to answer one question:

    Does Category, Kind, or Type independently affect computation?
"""

from __future__ import annotations

from .dimensions import SemanticDimension as D
from .field import Field
from .hierarchy import ClassificationRegistry
from .operator import OperatorRule
from .relations import Relation, supports
from .runtime import SemanticRuntime
from .vocabulary import Operation, Scale


def build_experiment_registry() -> ClassificationRegistry:
    registry = ClassificationRegistry()

    for category in (
        "Identity",
        "Quantitative",
        "Spatial",
        "Temporal",
    ):
        registry.register_category(category)

    # Same Kind and Type labels under different Categories.
    registry.register_kind("Temporal", "Coordinate")
    registry.register_type(
        "Temporal",
        "Coordinate",
        "Scalar",
    )
    registry.register_kind("Temporal", "Measurement")
    registry.register_type(
        "Temporal",
        "Measurement",
        "Difference",
    )

    registry.register_kind("Spatial", "Coordinate")
    registry.register_type(
        "Spatial",
        "Coordinate",
        "Scalar",
    )
    registry.register_kind("Spatial", "Measurement")
    registry.register_type(
        "Spatial",
        "Measurement",
        "Displacement",
    )

    # Same Category and Type label under different Kinds.
    registry.register_kind("Quantitative", "Counter")
    registry.register_type(
        "Quantitative",
        "Counter",
        "Scalar",
    )

    registry.register_kind("Quantitative", "Measurement")
    registry.register_type(
        "Quantitative",
        "Measurement",
        "Scalar",
    )
    registry.register_type(
        "Quantitative",
        "Measurement",
        "CountDelta",
    )
    registry.register_type(
        "Quantitative",
        "Measurement",
        "Difference",
    )

    # Same Category and Kind; different Types.
    registry.register_kind("Identity", "Address")
    registry.register_type(
        "Identity",
        "Address",
        "IPv4Address",
    )
    registry.register_type(
        "Identity",
        "Address",
        "MACAddress",
    )

    return registry


REGISTRY = build_experiment_registry()


# ------------------------------------------------------------
# Category experiment
#
# These differ ONLY in Category.
#
# Kind       = Coordinate
# Type       = Scalar
# Scale      = Interval
# Unit       = unit
# Role       = Experiment.Operand
# ------------------------------------------------------------

TEMPORAL_A = Field(
    name="experiment.temporal.a",
    classification=REGISTRY.classify(
        "Temporal",
        "Coordinate",
        "Scalar",
    ),
    scale=Scale.INTERVAL,
    role="Experiment.Operand",
    unit="unit",
)

TEMPORAL_B = Field(
    name="experiment.temporal.b",
    classification=REGISTRY.classify(
        "Temporal",
        "Coordinate",
        "Scalar",
    ),
    scale=Scale.INTERVAL,
    role="Experiment.Operand",
    unit="unit",
)

SPATIAL_A = Field(
    name="experiment.spatial.a",
    classification=REGISTRY.classify(
        "Spatial",
        "Coordinate",
        "Scalar",
    ),
    scale=Scale.INTERVAL,
    role="Experiment.Operand",
    unit="unit",
)

SPATIAL_B = Field(
    name="experiment.spatial.b",
    classification=REGISTRY.classify(
        "Spatial",
        "Coordinate",
        "Scalar",
    ),
    scale=Scale.INTERVAL,
    role="Experiment.Operand",
    unit="unit",
)


# ------------------------------------------------------------
# Kind experiment
#
# These differ ONLY in Kind.
#
# Category   = Quantitative
# Type       = Scalar
# Scale      = Ratio
# Unit       = unit
# Role       = Experiment.Operand
# ------------------------------------------------------------

COUNTER_A = Field(
    name="experiment.counter.a",
    classification=REGISTRY.classify(
        "Quantitative",
        "Counter",
        "Scalar",
    ),
    scale=Scale.RATIO,
    role="Experiment.Operand",
    unit="unit",
)

COUNTER_B = Field(
    name="experiment.counter.b",
    classification=REGISTRY.classify(
        "Quantitative",
        "Counter",
        "Scalar",
    ),
    scale=Scale.RATIO,
    role="Experiment.Operand",
    unit="unit",
)

MEASUREMENT_A = Field(
    name="experiment.measurement.a",
    classification=REGISTRY.classify(
        "Quantitative",
        "Measurement",
        "Scalar",
    ),
    scale=Scale.RATIO,
    role="Experiment.Operand",
    unit="unit",
)

MEASUREMENT_B = Field(
    name="experiment.measurement.b",
    classification=REGISTRY.classify(
        "Quantitative",
        "Measurement",
        "Scalar",
    ),
    scale=Scale.RATIO,
    role="Experiment.Operand",
    unit="unit",
)


# ------------------------------------------------------------
# Type experiment
#
# These differ ONLY in Type.
# ------------------------------------------------------------

IPV4_A = Field(
    name="experiment.address.a",
    classification=REGISTRY.classify(
        "Identity",
        "Address",
        "IPv4Address",
    ),
    scale=Scale.NOMINAL,
    role="Experiment.Address",
)

IPV4_B = Field(
    name="experiment.address.b",
    classification=REGISTRY.classify(
        "Identity",
        "Address",
        "IPv4Address",
    ),
    scale=Scale.NOMINAL,
    role="Experiment.Address",
)

MAC_A = Field(
    name="experiment.address.mac",
    classification=REGISTRY.classify(
        "Identity",
        "Address",
        "MACAddress",
    ),
    scale=Scale.NOMINAL,
    role="Experiment.Address",
)


def _same(
    lhs: Field,
    rhs: Field,
    *,
    category: str,
    kind: str,
    type_name: str,
) -> bool:
    return (
        lhs.category == rhs.category == category
        and lhs.kind == rhs.kind == kind
        and lhs.type == rhs.type == type_name
        and lhs.scale == rhs.scale
        and lhs.unit == rhs.unit
    )


# ------------------------------------------------------------
# Category-sensitive SUB rules
# ------------------------------------------------------------

def _temporal_sub(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return _same(
        lhs,
        rhs,
        category="Temporal",
        kind="Coordinate",
        type_name="Scalar",
    )


def _temporal_sub_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    return Field(
        name=f"({lhs.name}-{rhs.name})",
        classification=REGISTRY.classify(
            "Temporal",
            "Measurement",
            "Difference",
        ),
        scale=Scale.RATIO,
        role="Experiment.Result",
        unit=lhs.unit,
    )


def _spatial_sub(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return _same(
        lhs,
        rhs,
        category="Spatial",
        kind="Coordinate",
        type_name="Scalar",
    )


def _spatial_sub_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    return Field(
        name=f"({lhs.name}-{rhs.name})",
        classification=REGISTRY.classify(
            "Spatial",
            "Measurement",
            "Displacement",
        ),
        scale=Scale.RATIO,
        role="Experiment.Result",
        unit=lhs.unit,
    )


# ------------------------------------------------------------
# Kind-sensitive SUB rules
# ------------------------------------------------------------

def _counter_sub(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return _same(
        lhs,
        rhs,
        category="Quantitative",
        kind="Counter",
        type_name="Scalar",
    )


def _counter_sub_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    return Field(
        name=f"({lhs.name}-{rhs.name})",
        classification=REGISTRY.classify(
            "Quantitative",
            "Measurement",
            "CountDelta",
        ),
        scale=Scale.INTERVAL,
        role="Experiment.Result",
        unit=lhs.unit,
    )


def _measurement_sub(fields: tuple[Field, ...]) -> bool:
    if len(fields) != 2:
        return False

    lhs, rhs = fields

    return _same(
        lhs,
        rhs,
        category="Quantitative",
        kind="Measurement",
        type_name="Scalar",
    )


def _measurement_sub_transfer(
    fields: tuple[Field, ...],
) -> Field:
    lhs, rhs = fields

    return Field(
        name=f"({lhs.name}-{rhs.name})",
        classification=REGISTRY.classify(
            "Quantitative",
            "Measurement",
            "Difference",
        ),
        scale=Scale.RATIO,
        role="Experiment.Result",
        unit=lhs.unit,
    )


# ------------------------------------------------------------
# Type-sensitive equality rule
# ------------------------------------------------------------

def _same_address_type(fields: tuple[Field, ...]) -> bool:
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


def build_tier_experiment_runtime() -> SemanticRuntime:
    runtime = SemanticRuntime()

    runtime.register(
        OperatorRule(
            name="experiment-temporal-coordinate-sub",
            operation=Operation.SUB,
            arity=2,
            admit=_temporal_sub,
            transfer=_temporal_sub_transfer,
            depends_on=frozenset(
                {
                    D.CATEGORY,
                    D.KIND,
                    D.TYPE,
                    D.SCALE,
                    D.UNIT,
                }
            ),
        )
    )

    runtime.register(
        OperatorRule(
            name="experiment-spatial-coordinate-sub",
            operation=Operation.SUB,
            arity=2,
            admit=_spatial_sub,
            transfer=_spatial_sub_transfer,
            depends_on=frozenset(
                {
                    D.CATEGORY,
                    D.KIND,
                    D.TYPE,
                    D.SCALE,
                    D.UNIT,
                }
            ),
        )
    )

    runtime.register(
        OperatorRule(
            name="experiment-counter-sub",
            operation=Operation.SUB,
            arity=2,
            admit=_counter_sub,
            transfer=_counter_sub_transfer,
            depends_on=frozenset(
                {
                    D.CATEGORY,
                    D.KIND,
                    D.TYPE,
                    D.SCALE,
                    D.UNIT,
                }
            ),
        )
    )

    runtime.register(
        OperatorRule(
            name="experiment-measurement-sub",
            operation=Operation.SUB,
            arity=2,
            admit=_measurement_sub,
            transfer=_measurement_sub_transfer,
            depends_on=frozenset(
                {
                    D.CATEGORY,
                    D.KIND,
                    D.TYPE,
                    D.SCALE,
                    D.UNIT,
                }
            ),
        )
    )

    runtime.register(
        OperatorRule(
            name="experiment-address-equality",
            operation=Operation.EQ,
            arity=2,
            admit=_same_address_type,
            depends_on=frozenset(
                {
                    D.CATEGORY,
                    D.KIND,
                    D.TYPE,
                    D.SCALE,
                }
            ),
        )
    )

    return runtime
