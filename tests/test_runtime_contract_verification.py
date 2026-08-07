from veridic.catalog import (
    DURATION,
)
from veridic.contracts import (
    DEFAULT_CONTRACT_REGISTRY,
    ContractViolation,
)
from veridic.field import Field
from veridic.operator import OperatorRule
from veridic.runtime import SemanticRuntime
from veridic.taxonomy import (
    DEFAULT_CLASSIFICATION_REGISTRY
    as REGISTRY,
)
from veridic.utilities.testing import raises
from veridic.utilities.units import (
    BYTE,
    METER,
    SECOND,
)
from veridic.vocabulary import (
    Operation,
    Scale,
)


def test_runtime_rejects_incoherent_input():
    bad_duration = Field(
        name="bad.duration",
        classification=REGISTRY.classify(
            "Temporal",
            "Measurement",
            "Duration",
        ),
        scale=Scale.RATIO,
        role="Bad.Duration",
        unit=BYTE,
    )

    runtime = SemanticRuntime(
        contracts=DEFAULT_CONTRACT_REGISTRY
    )

    runtime.register(
        OperatorRule(
            name="always",
            operation=Operation.ADD,
            arity=2,
            admit=lambda fields: True,
        )
    )

    with raises(
        ContractViolation
    ):
        runtime.resolve(
            Operation.ADD,
            bad_duration,
            DURATION,
        )


def test_runtime_rejects_incoherent_transfer():
    runtime = SemanticRuntime(
        contracts=DEFAULT_CONTRACT_REGISTRY
    )

    def transfer(
        fields: tuple[Field, ...],
    ) -> Field:
        lhs, rhs = fields

        return Field(
            name=f"({lhs.name}/{rhs.name})",
            classification=REGISTRY.classify(
                "Quantitative",
                "Rate",
                "DataRate",
            ),
            scale=Scale.RATIO,
            role="Derived.BadRate",
            unit=(
                METER
                / SECOND
            ),
        )

    runtime.register(
        OperatorRule(
            name="bad-data-rate-transfer",
            operation=Operation.DIV,
            arity=2,
            admit=lambda fields: True,
            transfer=transfer,
        )
    )

    with raises(
        ContractViolation
    ):
        runtime.resolve(
            Operation.DIV,
            DURATION,
            DURATION,
        )


def test_runtime_accepts_coherent_transfer():
    runtime = SemanticRuntime(
        contracts=DEFAULT_CONTRACT_REGISTRY
    )

    def transfer(
        fields: tuple[Field, ...],
    ) -> Field:
        lhs, rhs = fields

        return Field(
            name=f"({lhs.name}/{rhs.name})",
            classification=REGISTRY.classify(
                "Quantitative",
                "Rate",
                "DataRate",
            ),
            scale=Scale.RATIO,
            role="Derived.DataRate",
            unit=(
                BYTE
                / SECOND
            ),
        )

    runtime.register(
        OperatorRule(
            name="good-data-rate-transfer",
            operation=Operation.DIV,
            arity=2,
            admit=lambda fields: True,
            transfer=transfer,
        )
    )

    result = runtime.resolve(
        Operation.DIV,
        DURATION,
        DURATION,
    )

    assert result.output is not None

    assert (
        result.output.classification_path
        == "Quantitative.Rate.DataRate"
    )
