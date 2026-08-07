import pytest

from fieldframe.domain_catalog import (
    TEMPERATURE_C_A,
    TEMPERATURE_C_B,
)
from fieldframe.domain_laws import build_domain_runtime
from fieldframe.errors import UndefinedOperation
from fieldframe.vocabulary import Operation, Scale

runtime = build_domain_runtime()


def test_absolute_celsius_difference_changes_type_and_scale():
    result = runtime.resolve(
        Operation.SUB,
        TEMPERATURE_C_A,
        TEMPERATURE_C_B,
    )

    assert result.output is not None

    assert result.output.classification_path == (
        "Physical.Measurement.TemperatureDifference"
    )

    assert result.output.scale is Scale.RATIO
    assert result.output.unit == "delta_degree_Celsius"


def test_absolute_celsius_addition_is_not_defined():
    with pytest.raises(UndefinedOperation):
        runtime.resolve(
            Operation.ADD,
            TEMPERATURE_C_A,
            TEMPERATURE_C_B,
        )
