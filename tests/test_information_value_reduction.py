import veridic.information as information

from veridic.catalog import (
    BYTE_COUNT,
    DURATION,
)
from veridic.field import FieldValue
from veridic.information import (
    HAS_VALUE,
    AtomicProposition,
    field_value_from,
    format_proposition,
    value_statement,
)


def test_semantic_value_adapter_is_removed():
    assert not hasattr(
        information,
        "SemanticValue",
    )


def test_value_statement_contains_field_and_datum_only():
    proposition = value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )

    assert isinstance(
        proposition,
        AtomicProposition,
    )

    assert (
        proposition.relation
        == HAS_VALUE
    )

    assert (
        proposition.terms
        == (
            DURATION,
            5.0,
        )
    )


def test_field_supplies_semantics_to_same_datum():
    duration = value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )

    bytes_ = value_statement(
        FieldValue(
            BYTE_COUNT,
            5.0,
        )
    )

    assert (
        duration != bytes_
    )

    assert (
        duration.terms[1]
        == bytes_.terms[1]
    )


def test_field_value_round_trip_preserves_semantics():
    original = FieldValue(
        DURATION,
        5.0,
    )

    proposition = value_statement(
        original
    )

    restored = field_value_from(
        proposition
    )

    assert (
        restored == original
    )


def test_format_uses_field_unit():
    proposition = value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )

    assert (
        format_proposition(
            proposition
        )
        == "event.duration = 5.0 s"
    )


def test_no_duplicate_semantic_signature_in_value_term():
    proposition = value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )

    datum = proposition.terms[1]

    assert datum == 5.0

    assert not hasattr(
        datum,
        "classification_path",
    )

    assert not hasattr(
        datum,
        "scale",
    )

    assert not hasattr(
        datum,
        "unit",
    )
