from veridic.catalog import DURATION
from veridic.field import FieldValue
from veridic.validation import validate_field_value


def test_non_negative_duration_invariant_passes():
    value = FieldValue(
        field=DURATION,
        value=4.0,
    )

    report = validate_field_value(value)

    assert report.is_valid

    checks = {
        check.invariant_name: check
        for check in report.checks
    }

    assert checks["non_negative"].satisfied


def test_negative_duration_invariant_fails():
    value = FieldValue(
        field=DURATION,
        value=-1.0,
    )

    report = validate_field_value(value)

    assert not report.is_valid

    assert any(
        check.invariant_name == "non_negative"
        and check.violated
        for check in report.checks
    )


def test_relational_invariant_is_unresolved_without_context():
    value = FieldValue(
        field=DURATION,
        value=4.0,
    )

    report = validate_field_value(value)

    assert report.is_valid
    assert not report.is_fully_verified

    assert any(
        check.invariant_name == "matches_event_bounds"
        and check.unresolved
        for check in report.checks
    )
