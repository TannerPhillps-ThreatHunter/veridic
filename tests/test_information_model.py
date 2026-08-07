from veridic.catalog import (
    DURATION,
    TIMESTAMP_START,
)
from veridic.field import FieldValue
from veridic.information import (
    InformationState,
    conjunction,
    negate,
    value_statement,
)


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


def test_present_information_is_represented():
    information = proposition()

    state = InformationState(
        information
    )

    assert state.contains(
        information
    )


def test_absence_means_not_represented():
    information = proposition()

    state = InformationState()

    assert not state.contains(
        information
    )


def test_negative_information_is_separate_representation():
    information = proposition()

    negative = negate(
        information
    )

    state = InformationState(
        negative
    )

    assert not state.contains(
        information
    )

    assert state.contains(
        negative
    )

    assert (
        state.polarity(
            information
        )
        == (
            False,
            True,
        )
    )


def test_compound_information_can_be_represented():
    first = proposition()

    second = value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )

    compound = conjunction(
        first,
        second,
    )

    state = InformationState(
        compound
    )

    assert state.contains(
        compound
    )


def test_opposing_information_is_preserved_without_truth_collapse():
    information = proposition()

    state = InformationState(
        information,
        negate(information),
    )

    assert (
        state.polarity(
            information
        )
        == (
            True,
            True,
        )
    )
