from veridic.catalog import (
    BYTE_COUNT,
    DURATION,
    EMPLOYEE_ID,
    LATITUDE,
    PACKET_COUNT,
    SEVERITY,
    TEMPERATURE,
    TIMESTAMP_START,
)
from veridic.contracts import (
    DEFAULT_CONTRACT_REGISTRY,
    ContractRegistry,
    ContractViolation,
)
from veridic.field import Field
from veridic.hierarchy import (
    Classification,
)
from veridic.utilities.dimensions import (
    DATA,
    TIME,
)
from veridic.utilities.testing import raises
from veridic.utilities.truth import Truth
from veridic.utilities.units import (
    BYTE,
    METER,
    SECOND,
)
from veridic.vocabulary import Scale


def test_canonical_fields_are_coherent():
    for field in (
        TIMESTAMP_START,
        DURATION,
        BYTE_COUNT,
        PACKET_COUNT,
        TEMPERATURE,
        LATITUDE,
        EMPLOYEE_ID,
        SEVERITY,
    ):
        result = (
            DEFAULT_CONTRACT_REGISTRY
            .evaluate(field)
        )

        assert (
            result.truth
            is Truth.TRUE
        )


def test_unknown_type_is_epistemically_unknown():
    field = Field(
        name="experimental.value",
        classification=Classification(
            category="Experimental",
            kind="Unknown",
            type="Mystery",
        ),
        scale=Scale.NOMINAL,
        role="Experiment",
    )

    result = (
        DEFAULT_CONTRACT_REGISTRY
        .evaluate(field)
    )

    assert (
        result.truth
        is Truth.UNKNOWN
    )


def test_duration_rejects_data_dimension():
    field = Field(
        name="bad.duration",
        classification=Classification(
            category="Temporal",
            kind="Measurement",
            type="Duration",
        ),
        scale=Scale.RATIO,
        role="Bad.Duration",
        unit=BYTE,
    )

    result = (
        DEFAULT_CONTRACT_REGISTRY
        .evaluate(field)
    )

    assert (
        result.truth
        is Truth.FALSE
    )

    assert any(
        "dimension mismatch"
        in reason
        for reason
        in result.reasons
    )


def test_duration_rejects_interval_scale():
    field = Field(
        name="bad.duration",
        classification=Classification(
            category="Temporal",
            kind="Measurement",
            type="Duration",
        ),
        scale=Scale.INTERVAL,
        role="Bad.Duration",
        unit=SECOND,
    )

    result = (
        DEFAULT_CONTRACT_REGISTRY
        .evaluate(field)
    )

    assert (
        result.truth
        is Truth.FALSE
    )

    assert any(
        "invalid scale"
        in reason
        for reason
        in result.reasons
    )


def test_identifier_rejects_unit():
    field = Field(
        name="employee.id.bad",
        classification=Classification(
            category="Identity",
            kind="Identifier",
            type="EmployeeIdentifier",
        ),
        scale=Scale.NOMINAL,
        role="Employee.Identity",
        unit=SECOND,
    )

    with raises(
        ContractViolation
    ):
        (
            DEFAULT_CONTRACT_REGISTRY
            .assert_coherent(field)
        )


def test_data_rate_requires_data_per_time():
    field = Field(
        name="bad.rate",
        classification=Classification(
            category="Quantitative",
            kind="Rate",
            type="DataRate",
        ),
        scale=Scale.RATIO,
        role="Bad.Rate",
        unit=(
            METER
            / SECOND
        ),
    )

    with raises(
        ContractViolation
    ):
        (
            DEFAULT_CONTRACT_REGISTRY
            .assert_coherent(field)
        )


def test_correct_data_rate_contract():
    field = Field(
        name="good.rate",
        classification=Classification(
            category="Quantitative",
            kind="Rate",
            type="DataRate",
        ),
        scale=Scale.RATIO,
        role="Good.Rate",
        unit=(
            BYTE
            / SECOND
        ),
    )

    result = (
        DEFAULT_CONTRACT_REGISTRY
        .assert_coherent(field)
    )

    assert result.coherent

    assert (
        field.dimension
        == DATA / TIME
    )


def test_empty_registry_returns_unknown():
    registry = ContractRegistry()

    result = registry.evaluate(
        DURATION
    )

    assert (
        result.truth
        is Truth.UNKNOWN
    )
