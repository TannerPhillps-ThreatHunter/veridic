import polars as pl

from fieldframe.catalog import DURATION
from fieldframe.column import SemanticColumn


def test_semantic_column_binds_field_to_series():
    column = SemanticColumn(
        field=DURATION,
        series=pl.Series(
            "event.duration",
            [1.0, 2.0, 3.0],
        ),
    )

    assert column.field is DURATION
    assert len(column) == 3

    assert column.value_at(1).value == 2.0
    assert (
        column.value_at(1).field
        is DURATION
    )


def test_semantic_column_normalizes_series_name():
    column = SemanticColumn(
        field=DURATION,
        series=pl.Series(
            "wrong_name",
            [1.0],
        ),
    )

    assert (
        column.series.name
        == "event.duration"
    )
