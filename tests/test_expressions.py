from veridic.utilities.expressions import (
    UNKNOWN,
    eq,
    evaluate,
    ref,
    sub,
)
from veridic.utilities.truth import Truth


def duration_invariant():
    return eq(
        ref("event.duration"),
        sub(
            ref("event.end"),
            ref("event.start"),
        ),
    )


def test_expression_dependencies():
    expression = duration_invariant()

    assert expression.dependencies() == frozenset(
        {
            "event.duration",
            "event.end",
            "event.start",
        }
    )


def test_expression_true():
    result = evaluate(
        duration_invariant(),
        {
            "event.start": 10,
            "event.end": 14,
            "event.duration": 4,
        },
    )

    assert result is Truth.TRUE


def test_expression_false():
    result = evaluate(
        duration_invariant(),
        {
            "event.start": 10,
            "event.end": 14,
            "event.duration": 8,
        },
    )

    assert result is Truth.FALSE


def test_expression_unknown():
    result = evaluate(
        duration_invariant(),
        {
            "event.start": 10,
            "event.end": 14,
        },
    )

    assert result is Truth.UNKNOWN


def test_missing_arithmetic_reference_is_unknown():
    expression = sub(
        ref("missing"),
        ref("event.start"),
    )

    result = evaluate(
        expression,
        {
            "event.start": 10,
        },
    )

    assert result is UNKNOWN
