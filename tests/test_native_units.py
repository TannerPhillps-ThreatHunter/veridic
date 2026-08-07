from fractions import Fraction

from veridic.utilities.dimensions import (
    DATA,
    TIME,
)
from veridic.utilities.testing import raises
from veridic.utilities.units import (
    BYTE,
    CELSIUS,
    DATA_RATE,
    DEFAULT_UNIT_REGISTRY,
    DELTA_CELSIUS,
    KELVIN,
    KILOBYTE,
    KILOMETER,
    METER,
    MILLISECOND,
    SECOND,
    AffineUnitOperation,
    DimensionMismatch,
)


def test_milliseconds_to_seconds_exact():
    result = DEFAULT_UNIT_REGISTRY.convert(
        1000,
        MILLISECOND,
        SECOND,
    )

    assert result == 1


def test_seconds_to_milliseconds_exact():
    result = DEFAULT_UNIT_REGISTRY.convert(
        1,
        SECOND,
        MILLISECOND,
    )

    assert result == 1000


def test_kilometers_to_meters():
    result = DEFAULT_UNIT_REGISTRY.convert(
        3,
        KILOMETER,
        METER,
    )

    assert result == 3000


def test_kilobytes_to_bytes():
    result = DEFAULT_UNIT_REGISTRY.convert(
        2,
        KILOBYTE,
        BYTE,
    )

    assert result == 2000


def test_zero_celsius_to_kelvin_exact():
    result = DEFAULT_UNIT_REGISTRY.convert(
        0,
        CELSIUS,
        KELVIN,
    )

    assert result == Fraction(
        27315,
        100,
    )


def test_kelvin_to_celsius_exact():
    result = DEFAULT_UNIT_REGISTRY.convert(
        Fraction(
            27315,
            100,
        ),
        KELVIN,
        CELSIUS,
    )

    assert result == 0


def test_delta_celsius_is_linear():
    assert DELTA_CELSIUS.is_linear


def test_absolute_celsius_is_affine():
    assert CELSIUS.is_affine


def test_affine_unit_cannot_be_multiplied():
    with raises(
        AffineUnitOperation
    ):
        _ = (
            CELSIUS
            * SECOND
        )


def test_incompatible_conversion_rejected():
    with raises(
        DimensionMismatch
    ):
        DEFAULT_UNIT_REGISTRY.convert(
            1,
            BYTE,
            SECOND,
        )


def test_byte_per_second_is_derived():
    derived = (
        BYTE
        / SECOND
    )

    assert (
        derived.dimension
        == DATA / TIME
    )

    assert (
        derived.dimension
        == DATA_RATE.dimension
    )

    assert derived.scale == 1


def test_unit_composition_is_deterministic():
    first = (
        BYTE
        / SECOND
    )

    second = (
        BYTE
        / SECOND
    )

    assert first == second
