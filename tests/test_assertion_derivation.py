from veridic.catalog import (
    BYTE_COUNT,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import FieldValue
from veridic.knowledge import (
    Assertion,
    Derivation,
    KnowledgeStore,
    Provenance,
)
from veridic.vocabulary import Operation


def build_store():
    return KnowledgeStore(
        build_domain_runtime()
    )


def test_assertion_introduces_external_knowledge():
    store = build_store()

    value = store.assert_value(
        "event.start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor",
            method="observation",
        ),
    )

    assert value.asserted
    assert not value.derived

    assert isinstance(
        value.origin,
        Assertion,
    )


def test_derivation_is_epistemically_distinct():
    store = build_store()

    store.assert_value(
        "event.start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    store.assert_value(
        "event.end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    duration = store.derive(
        "event.duration",
        Operation.SUB,
        "event.end",
        "event.start",
    )

    assert duration.derived
    assert not duration.asserted

    assert isinstance(
        duration.origin,
        Derivation,
    )

    assert duration.datum == 5.0

    assert (
        duration.field.classification_path
        == "Temporal.Measurement.Duration"
    )


def test_derivation_retains_dependencies():
    store = build_store()

    store.assert_value(
        "event.start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    store.assert_value(
        "event.end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    duration = store.derive(
        "event.duration",
        Operation.SUB,
        "event.end",
        "event.start",
    )

    assert isinstance(
        duration.origin,
        Derivation,
    )

    assert duration.origin.operands == (
        "event.end",
        "event.start",
    )

    assert duration.origin.rule
