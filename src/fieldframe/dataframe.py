"""Field-aware SemanticDataFrame over Polars."""

from __future__ import annotations

import operator
from collections.abc import (
    Mapping,
    Sequence,
)
from dataclasses import replace
from typing import Any

import polars as pl

from .column import SemanticColumn
from .domain_laws import build_domain_runtime
from .errors import (
    ContextualValidationError,
    SemanticError,
)
from .field import Field, FieldValue
from .frame_validation import (
    FrameValidationReport,
    RowValidation,
)
from .record import SemanticRecord
from .runtime import SemanticRuntime
from .schema import SemanticSchema
from .validation import validate_record
from .vocabulary import Operation


def _add(
    lhs: pl.Series,
    rhs: pl.Series,
) -> pl.Series:
    return operator.add(lhs, rhs)


def _sub(
    lhs: pl.Series,
    rhs: pl.Series,
) -> pl.Series:
    return operator.sub(lhs, rhs)


def _mul(
    lhs: pl.Series,
    rhs: pl.Series,
) -> pl.Series:
    return operator.mul(lhs, rhs)


def _div(
    lhs: pl.Series,
    rhs: pl.Series,
) -> pl.Series:
    return operator.truediv(lhs, rhs)


_SERIES_OPERATORS = {
    Operation.ADD: _add,
    Operation.SUB: _sub,
    Operation.MUL: _mul,
    Operation.DIV: _div,
}


class SemanticDataFrame:
    """A DataFrame whose columns carry explicit Field semantics.

    Polars owns physical execution.

    FieldFrame owns:

        semantic admission;
        Field transfer;
        contextual validation.
    """

    def __init__(
        self,
        frame: pl.DataFrame,
        schema: SemanticSchema,
        *,
        runtime: SemanticRuntime | None = None,
    ) -> None:
        if tuple(frame.columns) != schema.names:
            raise ValueError(
                "Physical columns and SemanticSchema "
                "must have identical names and order"
            )

        self._frame = frame
        self._schema = schema

        self._runtime = (
            runtime
            if runtime is not None
            else build_domain_runtime()
        )

    @classmethod
    def from_columns(
        cls,
        *columns: SemanticColumn,
        runtime: SemanticRuntime | None = None,
    ) -> SemanticDataFrame:
        if not columns:
            return cls(
                pl.DataFrame(),
                SemanticSchema(()),
                runtime=runtime,
            )

        lengths = {
            len(column)
            for column in columns
        }

        if len(lengths) != 1:
            raise ValueError(
                "SemanticColumn lengths must match"
            )

        frame = pl.DataFrame(
            [
                column.series.rename(
                    column.field.name
                )
                for column in columns
            ]
        )

        schema = SemanticSchema(
            tuple(
                column.field
                for column in columns
            )
        )

        return cls(
            frame,
            schema,
            runtime=runtime,
        )

    @classmethod
    def from_data(
        cls,
        data: Mapping[
            str,
            Sequence[Any],
        ],
        fields: Mapping[str, Field],
        *,
        runtime: SemanticRuntime | None = None,
    ) -> SemanticDataFrame:
        if tuple(data.keys()) != tuple(fields.keys()):
            raise ValueError(
                "Data and Field mappings must have "
                "identical names and order"
            )

        columns = tuple(
            SemanticColumn(
                field=fields[name],
                series=pl.Series(
                    name=name,
                    values=list(values),
                ),
            )
            for name, values in data.items()
        )

        return cls.from_columns(
            *columns,
            runtime=runtime,
        )

    @property
    def schema(self) -> SemanticSchema:
        return self._schema

    @property
    def columns(self) -> tuple[str, ...]:
        return self._schema.names

    @property
    def height(self) -> int:
        return self._frame.height

    @property
    def width(self) -> int:
        return self._frame.width

    @property
    def shape(self) -> tuple[int, int]:
        return self._frame.shape

    def field(
        self,
        name: str,
    ) -> Field:
        return self._schema.get(name)

    def column(
        self,
        name: str,
    ) -> SemanticColumn:
        return SemanticColumn(
            field=self.field(name),
            series=self._frame[name],
        )

    def to_polars(self) -> pl.DataFrame:
        """Return a defensive clone of the physical frame."""

        return self._frame.clone()

    def select(
        self,
        *names: str,
    ) -> SemanticDataFrame:
        return SemanticDataFrame(
            self._frame.select(
                list(names)
            ),
            self._schema.select(
                *names
            ),
            runtime=self._runtime,
        )

    def derive(
        self,
        name: str,
        operation: Operation,
        lhs: str,
        rhs: str,
    ) -> SemanticDataFrame:
        """Derive a new semantic column.

        Pipeline:

            Resolve
            Admit
            Execute
            Transfer

        Contextual assignment is a separate operation.
        """

        lhs_field = self.field(lhs)
        rhs_field = self.field(rhs)

        admission = self._runtime.resolve(
            operation,
            lhs_field,
            rhs_field,
        )

        if admission.output is None:
            raise SemanticError(
                f"{operation.value} does not "
                "derive a Field"
            )

        try:
            value_operator = (
                _SERIES_OPERATORS[
                    operation
                ]
            )
        except KeyError as exc:
            raise NotImplementedError(
                "Vector execution not implemented for "
                f"{operation.value}"
            ) from exc

        values = value_operator(
            self._frame[lhs],
            self._frame[rhs],
        ).rename(name)

        output_field = replace(
            admission.output,
            name=name,
        )

        next_frame = self._frame.with_columns(
            values
        )

        next_schema = self._schema.replace(
            output_field
        )

        # with_columns appends a new column but replaces
        # an existing one in-place. Reorder physically to
        # match the semantic schema exactly.
        next_frame = next_frame.select(
            list(next_schema.names)
        )

        return SemanticDataFrame(
            next_frame,
            next_schema,
            runtime=self._runtime,
        )

    def assign_values(
        self,
        name: str,
        values: pl.Series | Sequence[Any],
        *,
        verify: bool = True,
    ) -> SemanticDataFrame:
        """Assign Values to an existing semantic Field.

        The Field definition is preserved.

        If verify=True, all applicable Invariants must remain
        contextually valid.
        """

        field = self.field(name)

        if isinstance(values, pl.Series):
            series = values.rename(name)
        else:
            series = pl.Series(
                name=name,
                values=list(values),
            )

        if len(series) != self.height:
            raise ValueError(
                "Assigned Value count must match "
                "DataFrame height"
            )

        next_frame = self._frame.with_columns(
            series
        ).select(
            list(self._schema.names)
        )

        result = SemanticDataFrame(
            next_frame,
            self._schema,
            runtime=self._runtime,
        )

        if verify:
            report = result.validate()

            if not report.is_valid:
                first = report.violations[0]

                raise ContextualValidationError(
                    "Contextual invariant violation "
                    f"at row {first.row_index}: "
                    f"{first.check.expression}"
                )

        # Field is deliberately referenced above to ensure
        # assignment target exists and remains semantically
        # bound to the existing definition.
        _ = field

        return result

    def validate(
        self,
    ) -> FrameValidationReport:
        """Evaluate Field invariants row-by-row.

        This is intentionally correctness-first.

        Vectorized invariant execution can be introduced later
        without changing the semantic contract.
        """

        rows: list[RowValidation] = []

        for index, raw_row in enumerate(
            self._frame.iter_rows(
                named=True
            )
        ):
            values = {
                name: FieldValue(
                    field=self.field(name),
                    value=value,
                )
                for name, value
                in raw_row.items()
            }

            record = SemanticRecord(
                values
            )

            rows.append(
                RowValidation(
                    row_index=index,
                    report=validate_record(
                        record
                    ),
                )
            )

        return FrameValidationReport(
            tuple(rows)
        )

    def __repr__(self) -> str:
        return (
            "SemanticDataFrame("
            f"shape={self.shape}, "
            f"fields={self.columns}"
            ")"
        )
