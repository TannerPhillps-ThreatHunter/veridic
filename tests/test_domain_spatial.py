from veridic.utilities.testing import raises

from veridic.domain_catalog import (
    POSITION_X_A,
    POSITION_X_B,
    POSITION_Y_A,
)
from veridic.domain_laws import build_domain_runtime
from veridic.errors import UndefinedOperation
from veridic.vocabulary import Operation, Scale

runtime = build_domain_runtime()


def test_same_axis_coordinate_difference_is_valid():
    result = runtime.resolve(
        Operation.SUB,
        POSITION_X_A,
        POSITION_X_B,
    )

    assert result.output is not None

    assert result.output.classification_path == (
        "Spatial.Measurement.Displacement"
    )

    assert result.output.scale is Scale.RATIO
    assert result.output.unit == "meter"
    assert result.output.role == "Displacement.X"


def test_role_is_only_difference_between_x_and_y_fields():
    assert POSITION_X_A.category == POSITION_Y_A.category
    assert POSITION_X_A.kind == POSITION_Y_A.kind
    assert POSITION_X_A.type == POSITION_Y_A.type
    assert POSITION_X_A.scale == POSITION_Y_A.scale
    assert POSITION_X_A.unit == POSITION_Y_A.unit

    assert POSITION_X_A.role != POSITION_Y_A.role


def test_cross_axis_scalar_subtraction_is_rejected():
    with raises(UndefinedOperation):
        runtime.resolve(
            Operation.SUB,
            POSITION_X_A,
            POSITION_Y_A,
        )
