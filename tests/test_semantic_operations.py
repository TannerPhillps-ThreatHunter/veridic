from fieldframe.catalog import (
    BYTE_COUNT,
    DESTINATION_IPV4,
    DURATION,
    PACKET_COUNT,
    SEVERITY,
    SOURCE_IPV4,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from fieldframe.rules import build_runtime
from fieldframe.vocabulary import Operation, Scale

runtime = build_runtime()


def test_ipv4_equality_is_valid():
    result = runtime.resolve(
        Operation.EQ,
        SOURCE_IPV4,
        DESTINATION_IPV4,
    )

    assert result.rule.name == "same-type-equality"
    assert result.output is None


def test_severity_ordering_is_valid():
    result = runtime.resolve(
        Operation.GT,
        SEVERITY,
        SEVERITY,
    )

    assert result.rule.name == "ordered-gt"


def test_timestamp_difference_derives_duration():
    result = runtime.resolve(
        Operation.SUB,
        TIMESTAMP_END,
        TIMESTAMP_START,
    )

    output = result.output

    assert output is not None
    assert output.category == "Temporal"
    assert output.kind == "Measurement"
    assert output.type == "Duration"
    assert output.scale is Scale.RATIO
    assert output.unit == "second"


def test_duration_plus_duration_derives_duration():
    result = runtime.resolve(
        Operation.ADD,
        DURATION,
        DURATION,
    )

    output = result.output

    assert output is not None
    assert output.type == "Duration"
    assert output.scale is Scale.RATIO
    assert output.unit == "second"


def test_bytes_divided_by_duration_derives_data_rate():
    result = runtime.resolve(
        Operation.DIV,
        BYTE_COUNT,
        DURATION,
    )

    output = result.output

    assert output is not None
    assert output.kind == "Rate"
    assert output.type == "DataRate"
    assert output.unit == "byte/second"


def test_packets_divided_by_duration_derives_packet_rate():
    result = runtime.resolve(
        Operation.DIV,
        PACKET_COUNT,
        DURATION,
    )

    output = result.output

    assert output is not None
    assert output.kind == "Rate"
    assert output.type == "PacketRate"
    assert output.unit == "packet/second"
