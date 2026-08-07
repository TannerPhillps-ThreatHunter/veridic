from tests.frame_fixtures import (
    valid_event_frame,
)


def test_frame_has_physical_and_semantic_shape():
    frame = valid_event_frame()

    assert frame.shape == (3, 5)

    assert frame.columns == (
        "event.start",
        "event.end",
        "event.duration",
        "network.bytes",
        "scalar.multiplier",
    )


def test_field_semantics_survive_column_access():
    frame = valid_event_frame()

    duration = frame.column(
        "event.duration"
    )

    assert duration.field.type == "Duration"
    assert duration.field.scale.value == "ratio"
    assert duration.field.unit == "second"


def test_select_preserves_semantic_schema():
    frame = valid_event_frame()

    selected = frame.select(
        "event.start",
        "event.duration",
    )

    assert selected.columns == (
        "event.start",
        "event.duration",
    )

    assert (
        selected.field(
            "event.duration"
        ).classification_path
        == "Temporal.Measurement.Duration"
    )
