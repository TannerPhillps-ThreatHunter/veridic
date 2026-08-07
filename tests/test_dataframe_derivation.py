from fieldframe.vocabulary import Operation
from tests.frame_fixtures import valid_event_frame


def test_timestamp_subtraction_derives_duration_column():
    frame = valid_event_frame()

    derived = frame.derive(
        "derived.duration",
        Operation.SUB,
        "event.end",
        "event.start",
    )

    field = derived.field(
        "derived.duration"
    )

    assert (
        field.classification_path
        == "Temporal.Measurement.Duration"
    )

    assert field.scale.value == "ratio"
    assert field.unit == "second"

    assert (
        derived.to_polars()[
            "derived.duration"
        ].to_list()
        == [4.0, 5.0, 6.0]
    )


def test_bytes_per_duration_derives_data_rate():
    frame = valid_event_frame()

    derived = frame.derive(
        "network.rate",
        Operation.DIV,
        "network.bytes",
        "event.duration",
    )

    field = derived.field(
        "network.rate"
    )

    assert (
        field.classification_path
        == "Quantitative.Rate.DataRate"
    )

    assert field.unit == "byte/second"

    assert (
        derived.to_polars()[
            "network.rate"
        ].to_list()
        == [100.0, 200.0, 200.0]
    )


def test_duration_scaling_derives_duration():
    frame = valid_event_frame()

    derived = frame.derive(
        "scaled.duration",
        Operation.MUL,
        "event.duration",
        "scalar.multiplier",
    )

    field = derived.field(
        "scaled.duration"
    )

    assert (
        field.classification_path
        == "Temporal.Measurement.Duration"
    )

    assert (
        derived.to_polars()[
            "scaled.duration"
        ].to_list()
        == [8.0, 10.0, 12.0]
    )
