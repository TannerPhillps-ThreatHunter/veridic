from veridic.domain_catalog import (
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.domain_laws import build_domain_runtime
from veridic.vocabulary import Operation, Scale

runtime = build_domain_runtime()


def test_timestamp_difference_is_duration():
    result = runtime.resolve(
        Operation.SUB,
        TIMESTAMP_END,
        TIMESTAMP_START,
    )

    assert result.output is not None

    assert result.output.classification_path == (
        "Temporal.Measurement.Duration"
    )

    assert result.output.scale is Scale.RATIO
    assert result.output.unit == "second"
