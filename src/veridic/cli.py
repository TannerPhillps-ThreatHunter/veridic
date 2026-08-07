"""Operational command-line interface for Veridic."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass
from typing import Any, Sequence, TextIO

from . import catalog
from .domain_laws import build_domain_runtime
from .errors import VeridicError
from .execution import execute
from .field import Field, FieldValue
from .validation import (
    ValidationReport,
    validate_field_value,
)
from .vocabulary import Operation


class CLIError(ValueError):
    """Invalid command-line request."""


@dataclass(frozen=True, slots=True)
class ParsedOperand:
    field: Field
    value: Any

    @property
    def field_value(self) -> FieldValue:
        return FieldValue(
            field=self.field,
            value=self.value,
        )


def catalog_fields() -> tuple[Field, ...]:
    fields: dict[str, Field] = {}

    for value in vars(catalog).values():
        if isinstance(
            value,
            Field,
        ):
            fields[
                value.name
            ] = value

    return tuple(
        fields[name]
        for name in sorted(
            fields
        )
    )


def field_index() -> dict[str, Field]:
    return {
        field.name: field
        for field
        in catalog_fields()
    }


def resolve_field(
    name: str,
) -> Field:
    fields = field_index()

    try:
        return fields[name]
    except KeyError as exc:
        available = ", ".join(
            sorted(
                fields
            )
        )

        raise CLIError(
            f"unknown Field: {name}; "
            f"available: {available}"
        ) from exc


def parse_operation(
    text: str,
) -> Operation:
    try:
        return Operation(
            text.lower()
        )
    except ValueError as exc:
        available = ", ".join(
            operation.value
            for operation
            in Operation
        )

        raise CLIError(
            f"unknown operation: {text}; "
            f"available: {available}"
        ) from exc


def parse_datum(
    text: str,
) -> Any:
    try:
        return ast.literal_eval(
            text
        )
    except (
        ValueError,
        SyntaxError,
    ):
        return text


def parse_operand(
    text: str,
) -> ParsedOperand:
    if "=" not in text:
        raise CLIError(
            "operand must use FIELD=VALUE syntax: "
            f"{text}"
        )

    name, raw = text.split(
        "=",
        1,
    )

    if not name:
        raise CLIError(
            "operand Field name cannot be empty"
        )

    if not raw:
        raise CLIError(
            f"operand value cannot be empty: {name}"
        )

    return ParsedOperand(
        field=resolve_field(
            name
        ),
        value=parse_datum(
            raw
        ),
    )


def field_payload(
    field: Field,
) -> dict[str, Any]:
    return {
        "name": field.name,
        "classification": (
            field.classification_path
        ),
        "category": field.category,
        "kind": field.kind,
        "type": field.type,
        "scale": field.scale.value,
        "role": field.role,
        "unit": (
            field.unit_symbol
            if field.unit is not None
            else None
        ),
        "dimension": (
            str(
                field.dimension
            )
            if field.dimension is not None
            else None
        ),
        "invariants": [
            {
                "name": invariant.name,
                "expression": (
                    invariant.expression
                ),
                "scope": (
                    invariant.scope.value
                ),
            }
            for invariant
            in field.invariants
        ],
    }


def semantic_shape(
    field: Field,
) -> tuple[
    str,
    object,
    object,
]:
    """Semantic shape required for binding compatibility."""

    return (
        field.classification_path,
        field.scale,
        field.unit,
    )


def validation_payload(
    report: ValidationReport | None,
) -> dict[str, Any]:
    if (
        report is None
        or not report.checks
    ):
        return {
            "status": "not-applicable",
            "checks": [],
        }

    if report.violations:
        status = "violated"
    elif report.unresolved:
        status = "unresolved"
    elif report.is_fully_verified:
        status = "verified"
    else:
        status = "valid"

    return {
        "status": status,
        "checks": [
            {
                "field": check.field_name,
                "invariant": (
                    check.invariant_name
                ),
                "expression": (
                    check.expression
                ),
                "scope": (
                    check.scope.value
                ),
                "result": check.result,
            }
            for check
            in report.checks
        ],
    }


def print_json(
    payload: object,
    *,
    out: TextIO,
) -> None:
    print(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            default=str,
        ),
        file=out,
    )


def format_field(
    field: Field,
) -> str:
    unit = (
        field.unit_symbol
        if field.unit is not None
        else "-"
    )

    dimension = (
        str(field.dimension)
        if field.dimension is not None
        else "-"
    )

    return (
        f"{field.name} | "
        f"{field.classification_path} | "
        f"scale={field.scale.value} | "
        f"unit={unit} | "
        f"dimension={dimension} | "
        f"role={field.role}"
    )


def format_value(
    value: Any,
    field: Field | None,
) -> str:
    if field is None:
        return repr(
            value
        )

    suffix = ""

    if field.unit is not None:
        suffix = (
            " "
            + field.unit.symbol
        )

    return (
        f"{field.name} = "
        f"{value}"
        f"{suffix}"
    )


def command_fields(
    args: argparse.Namespace,
    *,
    out: TextIO,
) -> int:
    fields = catalog_fields()

    if args.json:
        print_json(
            [
                field_payload(
                    field
                )
                for field
                in fields
            ],
            out=out,
        )

        return 0

    print(
        "VERIDIC FIELD CATALOG",
        file=out,
    )

    for field in fields:
        print(
            format_field(
                field
            ),
            file=out,
        )

    return 0


def command_show(
    args: argparse.Namespace,
    *,
    out: TextIO,
) -> int:
    field = resolve_field(
        args.field
    )

    payload = field_payload(
        field
    )

    if args.json:
        print_json(
            payload,
            out=out,
        )

        return 0

    print(
        "VERIDIC FIELD",
        file=out,
    )

    print(
        f"name: {field.name}",
        file=out,
    )

    print(
        "classification: "
        f"{field.classification_path}",
        file=out,
    )

    print(
        f"scale: {field.scale.value}",
        file=out,
    )

    print(
        f"role: {field.role}",
        file=out,
    )

    print(
        "unit: "
        + (
            field.unit_symbol
            if field.unit is not None
            else "-"
        ),
        file=out,
    )

    print(
        "dimension: "
        + (
            str(field.dimension)
            if field.dimension is not None
            else "-"
        ),
        file=out,
    )

    print(
        "invariants:",
        file=out,
    )

    if not field.invariants:
        print(
            "  none",
            file=out,
        )

    for invariant in (
        field.invariants
    ):
        print(
            "  "
            f"{invariant.name}: "
            f"{invariant.expression} "
            f"[{invariant.scope.value}]",
            file=out,
        )

    return 0


def command_resolve(
    args: argparse.Namespace,
    *,
    out: TextIO,
) -> int:
    operation = parse_operation(
        args.operation
    )

    fields = tuple(
        resolve_field(
            name
        )
        for name
        in args.fields
    )

    runtime = build_domain_runtime()

    admission = runtime.resolve(
        operation,
        *fields,
    )

    payload = {
        "operation": (
            operation.value
        ),
        "admitted": True,
        "rule": (
            admission.rule.name
        ),
        "inputs": [
            field_payload(
                field
            )
            for field
            in admission.inputs
        ],
        "output": (
            field_payload(
                admission.output
            )
            if admission.output
            is not None
            else None
        ),
    }

    if args.json:
        print_json(
            payload,
            out=out,
        )

        return 0

    print(
        "VERIDIC SEMANTIC RESOLUTION",
        file=out,
    )

    print(
        f"operation: {operation.value.upper()}",
        file=out,
    )

    print(
        f"admitted: yes",
        file=out,
    )

    print(
        f"rule: {admission.rule.name}",
        file=out,
    )

    print(
        "inputs:",
        file=out,
    )

    for field in admission.inputs:
        print(
            "  "
            + format_field(
                field
            ),
            file=out,
        )

    print(
        "output:",
        file=out,
    )

    if admission.output is None:
        print(
            "  scalar result",
            file=out,
        )
    else:
        print(
            "  "
            + format_field(
                admission.output
            ),
            file=out,
        )

    return 0


def command_compute(
    args: argparse.Namespace,
    *,
    out: TextIO,
) -> int:
    operation = parse_operation(
        args.operation
    )

    parsed = tuple(
        parse_operand(
            operand
        )
        for operand
        in args.operands
    )

    operands = tuple(
        operand.field_value
        for operand
        in parsed
    )

    runtime = build_domain_runtime()

    result = execute(
        runtime,
        operation,
        *operands,
    )

    derived = result.output

    bound = None

    if args.target is not None:
        if derived is None:
            raise CLIError(
                "scalar result cannot be bound "
                "to a Field"
            )

        target = resolve_field(
            args.target
        )

        if (
            semantic_shape(
                derived.field
            )
            != semantic_shape(
                target
            )
        ):
            raise CLIError(
                "derived semantics "
                f"{derived.field.classification_path} "
                "cannot bind as "
                f"{target.classification_path}"
            )

        bound = FieldValue(
            field=target,
            value=derived.value,
        )

    context = {
        operand.field.name: (
            operand.value
        )
        for operand
        in operands
    }

    report = None

    if bound is not None:
        context[
            bound.field.name
        ] = bound.value

        report = validate_field_value(
            bound,
            context=context,
        )

    validation = validation_payload(
        report
    )

    payload = {
        "operation": (
            operation.value
        ),
        "rule": (
            result.admission.rule.name
        ),
        "inputs": [
            {
                "field": field_payload(
                    operand.field
                ),
                "value": operand.value,
            }
            for operand
            in operands
        ],
        "derived": {
            "value": result.value,
            "field": (
                field_payload(
                    derived.field
                )
                if derived is not None
                else None
            ),
        },
        "binding": (
            {
                "field": field_payload(
                    bound.field
                ),
                "value": bound.value,
            }
            if bound is not None
            else None
        ),
        "contextual_validation": (
            validation
        ),
    }

    if args.json:
        print_json(
            payload,
            out=out,
        )
    else:
        print(
            "VERIDIC SEMANTIC COMPUTATION",
            file=out,
        )

        print(
            f"operation: {operation.value.upper()}",
            file=out,
        )

        print(
            f"rule: {result.admission.rule.name}",
            file=out,
        )

        print(
            "inputs:",
            file=out,
        )

        for operand in operands:
            print(
                "  "
                + format_value(
                    operand.value,
                    operand.field,
                ),
                file=out,
            )

        print(
            "derived:",
            file=out,
        )

        print(
            "  "
            + format_value(
                result.value,
                (
                    derived.field
                    if derived is not None
                    else None
                ),
            ),
            file=out,
        )

        print(
            "semantic: admitted",
            file=out,
        )

        if bound is None:
            print(
                "binding: none",
                file=out,
            )
        else:
            print(
                "binding:",
                file=out,
            )

            print(
                "  "
                + format_value(
                    bound.value,
                    bound.field,
                ),
                file=out,
            )

        print(
            "contextual: "
            + validation[
                "status"
            ],
            file=out,
        )

        checks = validation[
            "checks"
        ]

        if checks:
            print(
                "invariants:",
                file=out,
            )

        for check in checks:
            marker = {
                True: "PASS",
                False: "FAIL",
                None: "UNKNOWN",
            }[
                check["result"]
            ]

            print(
                "  "
                f"{marker} "
                f"{check['invariant']}: "
                f"{check['expression']}",
                file=out,
            )

    if (
        report is not None
        and not report.is_valid
    ):
        return 3

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="veridic",
        description=(
            "Semantic computation with "
            "meaning preserved."
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version="veridic 0.2.0",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON",
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True,
    )

    fields = commands.add_parser(
        "fields",
        help="list known Fields",
    )

    fields.set_defaults(
        handler=command_fields
    )

    show = commands.add_parser(
        "show",
        help="inspect one Field",
    )

    show.add_argument(
        "field"
    )

    show.set_defaults(
        handler=command_show
    )

    resolve = commands.add_parser(
        "resolve",
        help=(
            "resolve semantic operation "
            "without values"
        ),
    )

    resolve.add_argument(
        "operation"
    )

    resolve.add_argument(
        "fields",
        nargs="+",
    )

    resolve.set_defaults(
        handler=command_resolve
    )

    compute = commands.add_parser(
        "compute",
        help=(
            "execute semantic operation "
            "over FIELD=VALUE operands"
        ),
    )

    compute.add_argument(
        "operation"
    )

    compute.add_argument(
        "--as",
        dest="target",
        help=(
            "bind the derived result "
            "to a contextual target Field"
        ),
    )

    compute.add_argument(
        "operands",
        nargs="+",
    )

    compute.set_defaults(
        handler=command_compute
    )

    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = (
        stdout
        if stdout is not None
        else sys.stdout
    )

    err = (
        stderr
        if stderr is not None
        else sys.stderr
    )

    parser = build_parser()

    try:
        args = parser.parse_args(
            argv
        )

        return args.handler(
            args,
            out=out,
        )

    except (
        CLIError,
        VeridicError,
        ValueError,
        TypeError,
        NotImplementedError,
        ZeroDivisionError,
    ) as exc:
        print(
            f"error: {exc}",
            file=err,
        )

        return 2


__all__ = [
    "CLIError",
    "build_parser",
    "catalog_fields",
    "field_index",
    "main",
    "parse_datum",
    "parse_operand",
    "parse_operation",
    "resolve_field",
]
