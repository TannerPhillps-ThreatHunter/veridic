from veridic.catalog import (
    DURATION,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.domain_catalog import DIMENSIONLESS_SCALAR
from veridic.domain_laws import build_domain_runtime
from veridic.execution import execute
from veridic.field import FieldValue
from veridic.record import SemanticRecord
from veridic.validation import (
    validate_field_value,
    validate_record,
)
from veridic.vocabulary import Operation

runtime = build_domain_runtime()


def make_valid_record() -> SemanticRecord:
    return SemanticRecord(
        {
            "event.start": FieldValue(
                TIMESTAMP_START,
                10.0,
            ),
            "event.end": FieldValue(
                TIMESTAMP_END,
                14.0,
            ),
            "event.duration": FieldValue(
                DURATION,
                4.0,
            ),
        }
    )


def test_duration_scaling_is_semantically_valid():
    duration = FieldValue(
        DURATION,
        4.0,
    )

    scalar = FieldValue(
        DIMENSIONLESS_SCALAR,
        2.0,
    )

    result = execute(
        runtime,
        Operation.MUL,
        duration,
        scalar,
    )

    assert result.output is not None

    assert result.output.field.classification_path == (
        "Temporal.Measurement.Duration"
    )

    assert result.output.value == 8.0


def test_derived_duration_is_valid_in_isolation():
    duration = FieldValue(
        DURATION,
        4.0,
    )

    scalar = FieldValue(
        DIMENSIONLESS_SCALAR,
        2.0,
    )

    result = execute(
        runtime,
        Operation.MUL,
        duration,
        scalar,
    )

    assert result.output is not None

    report = validate_field_value(
        result.output
    )

    # No known invariant violation exists.
    assert report.is_valid


def test_semantically_valid_result_can_be_contextually_invalid():
    record = make_valid_record()

    original = validate_record(record)

    assert original.is_valid
    assert original.is_fully_verified

    result = execute(
        runtime,
        Operation.MUL,
        record.get("event.duration"),
        FieldValue(
            DIMENSIONLESS_SCALAR,
            2.0,
        ),
    )

    assert result.output is not None
    assert result.output.value == 8.0

    # The arithmetic result is a perfectly meaningful Duration.
    #
    # But assigning 8 seconds back into Event.Duration while:
    #
    #     start = 10
    #     end   = 14
    #
    # makes the record false.
    transformed = record.replace_value(
        "event.duration",
        result.output.value,
    )

    contextual = validate_record(
        transformed
    )

    assert not contextual.is_valid

    assert any(
        check.invariant_name == "matches_event_bounds"
        and check.violated
        for check in contextual.violations
    )
