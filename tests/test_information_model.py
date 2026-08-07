from veridic.catalog import (
    DURATION,
    TIMESTAMP_START,
)
from veridic.field import FieldValue
from veridic.information import (
    InformationConflict,
    InformationState,
    conjunction,
    negate,
    value_statement,
)
from veridic.utilities.testing import raises
from veridic.utilities.truth import Truth


def proposition():
    return value_statement(
        FieldValue(
            TIMESTAMP_START,
            10.0,
        )
    )


def test_proposition_exists_without_knowledge():
    information = proposition()

    assert information is not None


def test_present_information_evaluates_true():
    information = proposition()

    state = InformationState(
        information
    )

    assert (
        state.evaluate(
            information
        )
        is Truth.TRUE
    )


def test_absence_is_unknown_not_false():
    information = proposition()

    state = InformationState()

    assert (
        state.evaluate(
            information
        )
        is Truth.UNKNOWN
    )


def test_explicit_negation_is_false():
    information = proposition()

    state = InformationState(
        negate(information)
    )

    assert (
        state.evaluate(
            information
        )
        is Truth.FALSE
    )


def test_compound_information():
    first = proposition()

    second = value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )

    state = InformationState(
        first,
        second,
    )

    compound = conjunction(
        first,
        second,
    )

    assert (
        state.evaluate(
            compound
        )
        is Truth.TRUE
    )


def test_contradiction_is_preserved():
    information = proposition()

    state = InformationState(
        information,
        negate(information),
    )

    with raises(
        InformationConflict
    ):
        state.evaluate(
            information
        )
