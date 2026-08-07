import pytest

from fieldframe.domain_catalog import (
    DESTINATION_IPV4,
    SOURCE_IPV4,
)
from fieldframe.domain_laws import build_domain_runtime
from fieldframe.errors import UndefinedOperation
from fieldframe.vocabulary import Operation

runtime = build_domain_runtime()


def test_ipv4_identity_equality_is_valid():
    result = runtime.resolve(
        Operation.EQ,
        SOURCE_IPV4,
        DESTINATION_IPV4,
    )

    assert result.rule.name == "domain-address-equality"


def test_ipv4_arithmetic_remains_undefined():
    with pytest.raises(UndefinedOperation):
        runtime.resolve(
            Operation.ADD,
            SOURCE_IPV4,
            DESTINATION_IPV4,
        )
