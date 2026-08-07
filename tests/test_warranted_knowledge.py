from veridic.catalog import (
    BYTE_COUNT,
    DURATION,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import FieldValue
from veridic.information import (
    value_statement,
)
from veridic.knowledge import (
    KnowledgeState,
    Provenance,
)
from veridic.knowledge_model import (
    AssertionWarrant,
    DerivationWarrant,
    KnowledgeBase,
)
from veridic.vocabulary import Operation


def build_base():
    return KnowledgeBase(
        build_domain_runtime()
    )


def test_assertion_warrants_information():
    base = build_base()

    knowledge = base.assert_value(
        "K:start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor-A",
            method="observation",
        ),
    )

    assert knowledge.asserted
    assert not knowledge.derived

    assert isinstance(
        knowledge.warrant,
        AssertionWarrant,
    )


def test_derivation_warrants_new_information():
    base = build_base()

    base.assert_value(
        "K:start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor-A"
        ),
    )

    base.assert_value(
        "K:end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor-A"
        ),
    )

    duration = base.derive_value(
        "K:duration",
        DURATION,
        Operation.SUB,
        "K:end",
        "K:start",
    )

    assert duration.derived

    assert isinstance(
        duration.warrant,
        DerivationWarrant,
    )


def test_same_information_can_have_multiple_warrants():
    base = build_base()

    asserted = base.assert_value(
        "K:duration:manual",
        FieldValue(
            DURATION,
            5.0,
        ),
        provenance=Provenance(
            source="operator"
        ),
    )

    base.assert_value(
        "K:start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor-A"
        ),
    )

    base.assert_value(
        "K:end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor-A"
        ),
    )

    derived = base.derive_value(
        "K:duration:derived",
        DURATION,
        Operation.SUB,
        "K:end",
        "K:start",
    )

    assert (
        asserted.proposition
        == derived.proposition
    )

    warrants = base.warrants_for(
        asserted.proposition
    )

    assert len(warrants) == 2

    assert {
        knowledge.identity
        for knowledge
        in warrants
    } == {
        "K:duration:manual",
        "K:duration:derived",
    }


def test_knowledge_identity_is_not_proposition_identity():
    base = build_base()

    proposition = value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )

    first = base.assert_information(
        "K:first",
        proposition,
        provenance=Provenance(
            source="source-A"
        ),
    )

    second = base.assert_information(
        "K:second",
        proposition,
        provenance=Provenance(
            source="source-B"
        ),
    )

    assert (
        first.proposition
        == second.proposition
    )

    assert (
        first.identity
        != second.identity
    )


def test_derivation_chain_preserves_warrant():
    base = build_base()

    base.assert_value(
        "K:start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    base.assert_value(
        "K:end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    base.assert_value(
        "K:bytes",
        FieldValue(
            BYTE_COUNT,
            10000.0,
        ),
        provenance=Provenance(
            source="counter"
        ),
    )

    base.derive_value(
        "K:duration",
        DURATION,
        Operation.SUB,
        "K:end",
        "K:start",
    )

    rate_field = (
        build_domain_runtime()
        .resolve(
            Operation.DIV,
            BYTE_COUNT,
            DURATION,
        )
        .output
    )

    assert rate_field is not None

    rate = base.derive_value(
        "K:rate",
        rate_field,
        Operation.DIV,
        "K:bytes",
        "K:duration",
    )

    assert rate.derived

    assert (
        rate.warrant.premises
        == (
            "K:bytes",
            "K:duration",
        )
    )


def test_invalidation_stales_downstream_without_changing_warrant():
    base = build_base()

    start = base.assert_value(
        "K:start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    base.assert_value(
        "K:end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    base.derive_value(
        "K:duration",
        DURATION,
        Operation.SUB,
        "K:end",
        "K:start",
    )

    base.invalidate(
        start.identity
    )

    assert (
        base.state(
            "K:start"
        )
        is KnowledgeState.INVALID
    )

    assert (
        base.state(
            "K:duration"
        )
        is KnowledgeState.STALE
    )

    assert isinstance(
        base.get(
            "K:start",
            require_active=False,
        ).warrant,
        AssertionWarrant,
    )
