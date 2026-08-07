from veridic.utilities.testing import raises

from veridic.domain_catalog import (
    DESTINATION_IPV4,
    SOURCE_IPV4,
)
from veridic.domain_laws import build_domain_runtime
from veridic.errors import UndefinedOperation
from veridic.vocabulary import Operation

runtime = build_domain_runtime()


def test_ipv4_identity_equality_is_valid():
    result = runtime.resolve(
        Operation.EQ,
        SOURCE_IPV4,
        DESTINATION_IPV4,
    )

    assert result.rule.name == "domain-address-equality"


def test_ipv4_arithmetic_remains_undefined():
    with raises(UndefinedOperation):
        runtime.resolve(
            Operation.ADD,
            SOURCE_IPV4,
            DESTINATION_IPV4,
        )
