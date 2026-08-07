from veridic.catalog import (
    BYTE_COUNT,
    DURATION,
    EMPLOYEE_ID,
    FREE_TEXT,
    LATITUDE,
    PACKET_COUNT,
    SEVERITY,
    SOURCE_IPV4,
    TAG_SET,
    TEMPERATURE,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.contracts import (
    DEFAULT_CONTRACT_REGISTRY,
)
from veridic.domain_catalog import (
    DIMENSIONLESS_SCALAR,
    POSITION_X_A,
    TEMPERATURE_C_A,
)
from veridic.utilities.truth import Truth


def test_all_current_canonical_fields_have_contracts():
    fields = (
        TIMESTAMP_START,
        TIMESTAMP_END,
        DURATION,
        SOURCE_IPV4,
        BYTE_COUNT,
        PACKET_COUNT,
        SEVERITY,
        EMPLOYEE_ID,
        TEMPERATURE,
        LATITUDE,
        FREE_TEXT,
        TAG_SET,
        DIMENSIONLESS_SCALAR,
        POSITION_X_A,
        TEMPERATURE_C_A,
    )

    for field in fields:
        result = (
            DEFAULT_CONTRACT_REGISTRY
            .evaluate(field)
        )

        assert (
            result.truth
            is Truth.TRUE
        ), (
            field.classification_path,
            result.reasons,
        )
