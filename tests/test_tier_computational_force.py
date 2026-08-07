import pytest

from fieldframe.errors import UndefinedOperation
from fieldframe.tier_experiments import (
    COUNTER_A,
    COUNTER_B,
    IPV4_A,
    IPV4_B,
    MAC_A,
    MEASUREMENT_A,
    MEASUREMENT_B,
    SPATIAL_A,
    SPATIAL_B,
    TEMPORAL_A,
    TEMPORAL_B,
    build_tier_experiment_runtime,
)
from fieldframe.vocabulary import Operation, Scale

runtime = build_tier_experiment_runtime()


def test_category_experiment_controls_other_dimensions():
    """Temporal and Spatial operands differ only in Category."""

    assert TEMPORAL_A.kind == SPATIAL_A.kind
    assert TEMPORAL_A.type == SPATIAL_A.type
    assert TEMPORAL_A.scale == SPATIAL_A.scale
    assert TEMPORAL_A.unit == SPATIAL_A.unit
    assert TEMPORAL_A.role == SPATIAL_A.role

    assert TEMPORAL_A.category != SPATIAL_A.category


def test_category_has_computational_force():
    temporal = runtime.resolve(
        Operation.SUB,
        TEMPORAL_A,
        TEMPORAL_B,
    )

    spatial = runtime.resolve(
        Operation.SUB,
        SPATIAL_A,
        SPATIAL_B,
    )

    assert temporal.output is not None
    assert spatial.output is not None

    assert temporal.output.classification_path == (
        "Temporal.Measurement.Difference"
    )

    assert spatial.output.classification_path == (
        "Spatial.Measurement.Displacement"
    )

    assert (
        temporal.output.classification_path
        != spatial.output.classification_path
    )


def test_kind_experiment_controls_other_dimensions():
    """Counter and Measurement operands differ only in Kind."""

    assert COUNTER_A.category == MEASUREMENT_A.category
    assert COUNTER_A.type == MEASUREMENT_A.type
    assert COUNTER_A.scale == MEASUREMENT_A.scale
    assert COUNTER_A.unit == MEASUREMENT_A.unit
    assert COUNTER_A.role == MEASUREMENT_A.role

    assert COUNTER_A.kind != MEASUREMENT_A.kind


def test_kind_has_computational_force():
    counter = runtime.resolve(
        Operation.SUB,
        COUNTER_A,
        COUNTER_B,
    )

    measurement = runtime.resolve(
        Operation.SUB,
        MEASUREMENT_A,
        MEASUREMENT_B,
    )

    assert counter.output is not None
    assert measurement.output is not None

    assert counter.output.type == "CountDelta"
    assert counter.output.scale is Scale.INTERVAL

    assert measurement.output.type == "Difference"
    assert measurement.output.scale is Scale.RATIO

    assert counter.output.semantic_signature != (
        measurement.output.semantic_signature
    )


def test_type_experiment_controls_other_dimensions():
    """IPv4 and MAC operands differ only in Type."""

    assert IPV4_A.category == MAC_A.category
    assert IPV4_A.kind == MAC_A.kind
    assert IPV4_A.scale == MAC_A.scale
    assert IPV4_A.unit == MAC_A.unit
    assert IPV4_A.role == MAC_A.role

    assert IPV4_A.type != MAC_A.type


def test_type_has_computational_force_for_admission():
    valid = runtime.resolve(
        Operation.EQ,
        IPV4_A,
        IPV4_B,
    )

    assert valid.rule.name == "experiment-address-equality"

    with pytest.raises(UndefinedOperation):
        runtime.resolve(
            Operation.EQ,
            IPV4_A,
            MAC_A,
        )
