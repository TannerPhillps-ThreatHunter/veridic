from fieldframe.catalog import (
    DURATION,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from fieldframe.field import FieldValue
from fieldframe.record import SemanticRecord
from fieldframe.validation import validate_record


def make_record(
    *,
    start: float,
    end: float,
    duration: float,
) -> SemanticRecord:
    return SemanticRecord(
        {
            "event.start": FieldValue(
                TIMESTAMP_START,
                start,
            ),
            "event.end": FieldValue(
                TIMESTAMP_END,
                end,
            ),
            "event.duration": FieldValue(
                DURATION,
                duration,
            ),
        }
    )


def test_consistent_event_record_is_valid():
    record = make_record(
        start=10.0,
        end=14.0,
        duration=4.0,
    )

    report = validate_record(record)

    assert report.is_valid
    assert report.is_fully_verified


def test_inconsistent_event_duration_is_rejected():
    record = make_record(
        start=10.0,
        end=14.0,
        duration=8.0,
    )

    report = validate_record(record)

    assert not report.is_valid

    assert any(
        check.invariant_name == "matches_event_bounds"
        and check.violated
        for check in report.violations
    )


def test_negative_duration_can_violate_multiple_invariants():
    record = make_record(
        start=10.0,
        end=14.0,
        duration=-4.0,
    )

    report = validate_record(record)

    names = {
        check.invariant_name
        for check in report.violations
    }

    assert "non_negative" in names
    assert "matches_event_bounds" in names
