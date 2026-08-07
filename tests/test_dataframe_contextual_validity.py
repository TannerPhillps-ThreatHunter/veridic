import pytest

from fieldframe.errors import (
    ContextualValidationError,
)
from fieldframe.vocabulary import Operation
from tests.frame_fixtures import valid_event_frame


def test_semantically_valid_derived_column_is_allowed():
    frame = valid_event_frame()

    derived = frame.derive(
        "scaled.duration",
        Operation.MUL,
        "event.duration",
        "scalar.multiplier",
    )

    assert (
        derived.to_polars()[
            "scaled.duration"
        ].to_list()
        == [8.0, 10.0, 12.0]
    )


def test_assigning_scaled_duration_back_is_rejected():
    frame = valid_event_frame()

    derived = frame.derive(
        "scaled.duration",
        Operation.MUL,
        "event.duration",
        "scalar.multiplier",
    )

    values = derived.to_polars()[
        "scaled.duration"
    ]

    with pytest.raises(
        ContextualValidationError
    ):
        frame.assign_values(
            "event.duration",
            values,
            verify=True,
        )


def test_invalid_context_can_be_constructed_explicitly():
    frame = valid_event_frame()

    derived = frame.derive(
        "scaled.duration",
        Operation.MUL,
        "event.duration",
        "scalar.multiplier",
    )

    invalid = frame.assign_values(
        "event.duration",
        derived.to_polars()[
            "scaled.duration"
        ],
        verify=False,
    )

    report = invalid.validate()

    assert not report.is_valid

    assert {
        violation.row_index
        for violation
        in report.violations
    } == {0, 1, 2}
