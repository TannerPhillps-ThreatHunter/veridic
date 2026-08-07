from veridic.catalog import (
    BYTE_COUNT,
    SOURCE_IPV4,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.errors import UndefinedOperation
from veridic.field import FieldValue
from veridic.knowledge import (
    InvalidKnowledge,
    InvalidRevision,
    KnowledgeState,
    KnowledgeStore,
    Provenance,
)
from veridic.utilities.testing import raises
from veridic.vocabulary import Operation


def store():
    return KnowledgeStore(
        build_domain_runtime()
    )


def test_observation_reduces_to_assertion_with_provenance():
    knowledge = store()

    value = knowledge.assert_value(
        "event.start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="clock",
            method="observation",
        ),
    )

    assert value.asserted

    assert (
        value.origin.provenance.method
        == "observation"
    )


def test_measurement_reduces_to_assertion_with_provenance():
    knowledge = store()

    value = knowledge.assert_value(
        "network.bytes",
        FieldValue(
            BYTE_COUNT,
            10000,
        ),
        provenance=Provenance(
            source="counter",
            method="measurement",
        ),
    )

    assert value.asserted


def test_nondeterministic_input_is_still_asserted_boundary_knowledge():
    knowledge = store()

    value = knowledge.assert_value(
        "external.sample",
        FieldValue(
            BYTE_COUNT,
            17,
        ),
        provenance=Provenance(
            source="external-random-source",
            method="nondeterministic-input",
        ),
    )

    assert value.asserted


def test_failed_derivation_creates_no_knowledge():
    knowledge = store()

    knowledge.assert_value(
        "source.ip",
        FieldValue(
            SOURCE_IPV4,
            "192.0.2.1",
        ),
        provenance=Provenance(
            source="packet"
        ),
    )

    with raises(
        UndefinedOperation
    ):
        knowledge.derive(
            "impossible",
            Operation.ADD,
            "source.ip",
            "source.ip",
        )

    assert "impossible" not in knowledge


def test_retraction_is_lifecycle_not_new_origin():
    knowledge = store()

    knowledge.assert_value(
        "event.start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    knowledge.retract(
        "event.start"
    )

    assert (
        knowledge.state(
            "event.start"
        )
        is KnowledgeState.RETRACTED
    )


def test_retracted_dependency_cannot_be_derived_from():
    knowledge = store()

    knowledge.assert_value(
        "event.start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    knowledge.assert_value(
        "event.end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    knowledge.retract(
        "event.start"
    )

    with raises(
        InvalidKnowledge
    ):
        knowledge.derive(
            "event.duration",
            Operation.SUB,
            "event.end",
            "event.start",
        )


def test_derived_value_cannot_silently_become_asserted():
    knowledge = store()

    knowledge.assert_value(
        "event.start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    knowledge.assert_value(
        "event.end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    knowledge.derive(
        "event.duration",
        Operation.SUB,
        "event.end",
        "event.start",
    )

    with raises(
        InvalidRevision
    ):
        knowledge.revise_assertion(
            "event.duration",
            knowledge.get(
                "event.duration"
            ).field_value,
            provenance=Provenance(
                source="manual"
            ),
        )
