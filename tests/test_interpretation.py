from veridic.catalog import DURATION
from veridic.field import FieldValue
from veridic.information import value_statement
from veridic.interpretation import evaluate_truth
from veridic.utilities.testing import raises
from veridic.utilities.truth import Truth


def proposition():
    return value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )


class TrueInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return Truth.TRUE


class FalseInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return Truth.FALSE


class UnknownInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return Truth.UNKNOWN


class InvalidInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return "true"


def test_truth_requires_interpretation():
    p = proposition()

    assert (
        evaluate_truth(
            p,
            under=TrueInterpretation(),
        )
        is Truth.TRUE
    )

    assert (
        evaluate_truth(
            p,
            under=FalseInterpretation(),
        )
        is Truth.FALSE
    )

    assert (
        evaluate_truth(
            p,
            under=UnknownInterpretation(),
        )
        is Truth.UNKNOWN
    )


def test_interpretation_must_return_truth():
    with raises(TypeError):
        evaluate_truth(
            proposition(),
            under=InvalidInterpretation(),
        )
