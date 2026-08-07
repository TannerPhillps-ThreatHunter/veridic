from veridic.catalog import (
    BYTE_COUNT,
    DURATION,
    LATITUDE,
    PACKET_COUNT,
    TEMPERATURE,
    TIMESTAMP_START,
)
from veridic.domain_catalog import (
    POSITION_X_A,
    TEMPERATURE_C_A,
    TEMPERATURE_C_B,
)
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import Field
from veridic.hierarchy import Classification
from veridic.rules import build_runtime
from veridic.utilities.dimensions import (
    ANGLE,
    COUNT,
    DATA,
    LENGTH,
    TEMPERATURE as TEMPERATURE_DIMENSION,
    TIME,
)
from veridic.utilities.testing import raises
from veridic.utilities.units import (
    BYTE,
    CELSIUS,
    DEGREE,
    DELTA_CELSIUS,
    METER,
    PACKET,
    SECOND,
)
from veridic.vocabulary import Operation, Scale


def test_field_rejects_string_unit():
    with raises(TypeError):
        Field(
            name="bad.field",
            classification=Classification(
                category="Temporal",
                kind="Measurement",
                type="Duration",
            ),
            scale=Scale.RATIO,
            role="Bad",
            unit="second",
        )


def test_temporal_fields_use_native_time_unit():
    assert TIMESTAMP_START.unit is SECOND
    assert DURATION.unit is SECOND
    assert DURATION.dimension == TIME


def test_byte_count_uses_native_data_unit():
    assert BYTE_COUNT.unit is BYTE
    assert BYTE_COUNT.dimension == DATA


def test_packet_count_uses_native_count_unit():
    assert PACKET_COUNT.unit is PACKET
    assert PACKET_COUNT.dimension == COUNT


def test_temperature_uses_native_affine_unit():
    assert TEMPERATURE.unit is CELSIUS
    assert (
        TEMPERATURE.dimension
        == TEMPERATURE_DIMENSION
    )


def test_latitude_uses_native_angle_unit():
    assert LATITUDE.unit is DEGREE
    assert LATITUDE.dimension == ANGLE


def test_projected_coordinate_uses_length():
    assert POSITION_X_A.unit is METER
    assert POSITION_X_A.dimension == LENGTH


def test_data_rate_unit_is_derived_from_operands():
    runtime = build_runtime()

    result = runtime.resolve(
        Operation.DIV,
        BYTE_COUNT,
        DURATION,
    )

    assert result.output is not None
    assert result.output.unit is not None

    assert (
        result.output.unit
        == BYTE / SECOND
    )

    assert (
        result.output.dimension
        == DATA / TIME
    )


def test_packet_rate_unit_is_derived_from_operands():
    runtime = build_runtime()

    result = runtime.resolve(
        Operation.DIV,
        PACKET_COUNT,
        DURATION,
    )

    assert result.output is not None
    assert result.output.unit is not None

    assert (
        result.output.unit
        == PACKET / SECOND
    )

    assert (
        result.output.dimension
        == COUNT / TIME
    )


def test_temperature_subtraction_changes_unit_semantics():
    runtime = build_domain_runtime()

    result = runtime.resolve(
        Operation.SUB,
        TEMPERATURE_C_A,
        TEMPERATURE_C_B,
    )

    assert result.output is not None

    assert (
        result.output.unit
        is DELTA_CELSIUS
    )

    assert (
        result.output.dimension
        == TEMPERATURE_DIMENSION
    )


def test_field_semantics_and_dimensions_are_distinct():
    assert (
        BYTE_COUNT.classification_path
        == "Quantitative.Measurement.ByteCount"
    )

    assert BYTE_COUNT.dimension == DATA

    assert (
        BYTE_COUNT.type
        != str(BYTE_COUNT.dimension)
    )
