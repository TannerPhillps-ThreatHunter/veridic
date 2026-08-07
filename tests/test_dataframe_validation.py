from tests.frame_fixtures import valid_event_frame


def test_valid_dataframe_is_fully_verified():
    frame = valid_event_frame()

    report = frame.validate()

    assert report.is_valid
    assert report.is_fully_verified
    assert not report.violations


def test_frame_validation_is_row_sensitive():
    frame = valid_event_frame()

    invalid = frame.assign_values(
        "event.duration",
        [
            4.0,
            99.0,
            6.0,
        ],
        verify=False,
    )

    report = invalid.validate()

    assert not report.is_valid

    assert len(
        report.violations
    ) == 1

    violation = (
        report.violations[0]
    )

    assert violation.row_index == 1

    assert (
        violation.check.invariant_name
        == "matches_event_bounds"
    )
