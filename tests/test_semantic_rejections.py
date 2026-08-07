import pytest

from fieldframe.catalog import (
    DESTINATION_IPV4,
    EMPLOYEE_ID,
    SEVERITY,
    SOURCE_IPV4,
)
from fieldframe.errors import UndefinedOperation
from fieldframe.rules import build_runtime
from fieldframe.vocabulary import Operation

runtime = build_runtime()


def test_ipv4_addition_is_undefined():
    with pytest.raises(UndefinedOperation):
        runtime.resolve(
            Operation.ADD,
            SOURCE_IPV4,
            DESTINATION_IPV4,
        )


def test_ipv4_ordering_is_undefined():
    with pytest.raises(UndefinedOperation):
        runtime.resolve(
            Operation.LT,
            SOURCE_IPV4,
            DESTINATION_IPV4,
        )


def test_severity_division_is_undefined():
    with pytest.raises(UndefinedOperation):
        runtime.resolve(
            Operation.DIV,
            SEVERITY,
            SEVERITY,
        )


def test_identifier_arithmetic_is_undefined():
    with pytest.raises(UndefinedOperation):
        runtime.resolve(
            Operation.ADD,
            EMPLOYEE_ID,
            EMPLOYEE_ID,
        )
