import pytest

from fieldframe.catalog import (
    DURATION,
    TIMESTAMP_START,
)
from fieldframe.schema import SemanticSchema


def test_schema_preserves_field_order():
    schema = SemanticSchema(
        (
            TIMESTAMP_START,
            DURATION,
        )
    )

    assert schema.names == (
        "event.start",
        "event.duration",
    )


def test_schema_requires_unique_names():
    with pytest.raises(ValueError):
        SemanticSchema(
            (
                DURATION,
                DURATION,
            )
        )


def test_schema_select():
    schema = SemanticSchema(
        (
            TIMESTAMP_START,
            DURATION,
        )
    )

    selected = schema.select(
        "event.duration"
    )

    assert selected.fields == (
        DURATION,
    )
