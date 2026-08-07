from fieldframe.domain_catalog import BYTE_COUNT, DURATION
from fieldframe.domain_laws import build_domain_runtime
from fieldframe.vocabulary import Operation, Scale

runtime = build_domain_runtime()


def test_bytes_per_duration_derives_data_rate():
    result = runtime.resolve(
        Operation.DIV,
        BYTE_COUNT,
        DURATION,
    )

    assert result.output is not None

    assert result.output.classification_path == (
        "Quantitative.Rate.DataRate"
    )

    assert result.output.scale is Scale.RATIO
    assert result.output.unit == "byte/second"
