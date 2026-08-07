from veridic.utilities.truth import Truth
from veridic.utilities.testing import raises


def test_truth_negation():
    assert Truth.TRUE.negate() is Truth.FALSE
    assert Truth.FALSE.negate() is Truth.TRUE
    assert Truth.UNKNOWN.negate() is Truth.UNKNOWN


def test_unknown_cannot_be_coerced_to_bool():
    with raises(TypeError):
        bool(Truth.UNKNOWN)


def test_three_valued_and():
    assert (
        Truth.TRUE.and_(Truth.TRUE)
        is Truth.TRUE
    )

    assert (
        Truth.TRUE.and_(Truth.UNKNOWN)
        is Truth.UNKNOWN
    )

    assert (
        Truth.FALSE.and_(Truth.UNKNOWN)
        is Truth.FALSE
    )


def test_three_valued_or():
    assert (
        Truth.FALSE.or_(Truth.FALSE)
        is Truth.FALSE
    )

    assert (
        Truth.FALSE.or_(Truth.UNKNOWN)
        is Truth.UNKNOWN
    )

    assert (
        Truth.TRUE.or_(Truth.UNKNOWN)
        is Truth.TRUE
    )
