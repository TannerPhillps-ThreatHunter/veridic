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
    KnowledgeState,
    KnowledgeStore,
    Provenance,
    format_explanation,
)
from veridic.vocabulary import Operation


def build_chain():
    store = KnowledgeStore(
        build_domain_runtime()
    )

    store.assert_value(
        "event.start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="sensor-A",
            method="observation",
        ),
    )

    store.assert_value(
        "event.end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="sensor-A",
            method="observation",
        ),
    )

    store.assert_value(
        "network.bytes",
        FieldValue(
            BYTE_COUNT,
            10000.0,
        ),
        provenance=Provenance(
            source="network-counter",
            method="measurement",
        ),
    )

    store.derive(
        "event.duration",
        Operation.SUB,
        "event.end",
        "event.start",
    )

    store.derive(
        "network.rate",
        Operation.DIV,
        "network.bytes",
        "event.duration",
    )

    return store


def test_composed_derivation():
    store = build_chain()

    duration = store.get(
        "event.duration"
    )

    rate = store.get(
        "network.rate"
    )

    assert duration.datum == 5.0
    assert rate.datum == 2000.0

    assert (
        rate.field.classification_path
        == "Quantitative.Rate.DataRate"
    )

    assert (
        rate.field.unit_symbol
        == "B/s"
    )


def test_transitive_dependency_tracking():
    store = build_chain()

    assert store.dependents(
        "event.end"
    ) == (
        "event.duration",
        "network.rate",
    )


def test_revision_makes_downstream_derivations_stale():
    store = build_chain()

    store.revise_assertion(
        "event.end",
        FieldValue(
            TIMESTAMP_END,
            20.0,
        ),
        provenance=Provenance(
            source="sensor-A",
            method="corrected-observation",
        ),
    )

    assert (
        store.state(
            "event.end"
        )
        is KnowledgeState.ACTIVE
    )

    assert (
        store.state(
            "event.duration"
        )
        is KnowledgeState.STALE
    )

    assert (
        store.state(
            "network.rate"
        )
        is KnowledgeState.STALE
    )

    assert (
        store.state(
            "network.bytes"
        )
        is KnowledgeState.ACTIVE
    )


def test_explanation_preserves_full_lineage():
    store = build_chain()

    explanation = store.explain(
        "network.rate"
    )

    text = format_explanation(
        explanation
    )

    assert (
        "network.rate = 2000.0 B/s [derived]"
        in text
    )

    assert (
        "event.duration = 5.0 s [derived]"
        in text
    )

    assert (
        "event.end = 15.0 s [asserted]"
        in text
    )

    assert (
        "event.start = 10.0 s [asserted]"
        in text
    )
