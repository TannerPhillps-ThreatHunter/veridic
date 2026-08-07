from fractions import Fraction

from veridic.utilities.dimensions import (
    DATA,
    DIMENSIONLESS,
    LENGTH,
    TIME,
)


def test_base_dimension():
    assert str(TIME) == "Time"

    assert TIME.exponent(
        "Time"
    ) == Fraction(1)


def test_dimension_division():
    velocity = (
        LENGTH
        / TIME
    )

    assert velocity.exponent(
        "Length"
    ) == Fraction(1)

    assert velocity.exponent(
        "Time"
    ) == Fraction(-1)


def test_data_rate_dimension():
    rate = (
        DATA
        / TIME
    )

    assert rate.exponent(
        "Data"
    ) == Fraction(1)

    assert rate.exponent(
        "Time"
    ) == Fraction(-1)


def test_dimension_cancellation():
    result = (
        TIME
        / TIME
    )

    assert result == DIMENSIONLESS
    assert result.is_dimensionless


def test_dimension_power():
    area = (
        LENGTH
        ** 2
    )

    assert area.exponent(
        "Length"
    ) == Fraction(2)


def test_fractional_dimension_power():
    area = (
        LENGTH
        ** 2
    )

    length = (
        area
        ** Fraction(1, 2)
    )

    assert length == LENGTH


def test_dimension_normalization():
    result = (
        LENGTH
        * TIME
        / TIME
    )

    assert result == LENGTH
