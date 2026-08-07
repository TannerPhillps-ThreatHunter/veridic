from fieldframe.catalog import DURATION
from fieldframe.domain_catalog import DIMENSIONLESS_SCALAR
from fieldframe.domain_laws import build_domain_runtime
from fieldframe.execution import execute
from fieldframe.field import FieldValue
from fieldframe.vocabulary import Operation

runtime = build_domain_runtime()


def test_same_field_semantics_can_carry_different_values():
    four_seconds = FieldValue(
        DURATION,
        4.0,
    )

    ten_seconds = FieldValue(
        DURATION,
        10.0,
    )

    assert four_seconds.field == ten_seconds.field
    assert four_seconds.value != ten_seconds.value


def test_value_affects_execution_not_static_admission():
    first = execute(
        runtime,
        Operation.MUL,
        FieldValue(DURATION, 4.0),
        FieldValue(DIMENSIONLESS_SCALAR, 2.0),
    )

    second = execute(
        runtime,
        Operation.MUL,
        FieldValue(DURATION, 10.0),
        FieldValue(DIMENSIONLESS_SCALAR, 2.0),
    )

    assert first.admission.rule == second.admission.rule

    assert first.output is not None
    assert second.output is not None

    assert first.output.field == second.output.field

    assert first.output.value == 8.0
    assert second.output.value == 20.0
