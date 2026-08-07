from veridic.catalog import (
    DURATION,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import FieldValue
from veridic.knowledge import (
    InvalidKnowledge,
    KnowledgeState,
    KnowledgeStore,
    Provenance,
)
from veridic.knowledge_model import (
    DerivationWarrant,
    InactiveKnowledge,
    KnowledgeBase,
)
from veridic.support import SupportState
from veridic.utilities.testing import raises
from veridic.vocabulary import Operation


def old_store():
    return KnowledgeStore(
        build_domain_runtime()
    )


def new_base():
    return KnowledgeBase(
        build_domain_runtime()
    )


def populate_old():
    store = old_store()

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

    store.derive(
        "event.duration",
        Operation.SUB,
        "event.end",
        "event.start",
    )

    return store


def populate_new():
    base = new_base()

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

    base.derive_value(
        "K:duration",
        DURATION,
        Operation.SUB,
        "K:end",
        "K:start",
    )

    return base


def test_legacy_revision_marks_derivation_stale():
    store = populate_old()

    store.revise_assertion(
        "event.end",
        FieldValue(
            TIMESTAMP_END,
            20.0,
        ),
        provenance=Provenance(
            source="sensor",
            method="revision",
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


def test_legacy_retraction_marks_derivation_stale():
    store = populate_old()

    store.retract(
        "event.end"
    )

    assert (
        store.state(
            "event.end"
        )
        is KnowledgeState.RETRACTED
    )

    assert (
        store.state(
            "event.duration"
        )
        is KnowledgeState.STALE
    )


def test_legacy_stale_derivation_cannot_be_used_as_current_premise():
    store = populate_old()

    store.retract(
        "event.end"
    )

    with raises(
        InvalidKnowledge
    ):
        store.get(
            "event.duration"
        )


def test_direct_invalidation_invalidates_target_only():
    base = populate_new()

    base.invalidate(
        "K:end"
    )

    assert (
        base.state(
            "K:end"
        )
        is KnowledgeState.INVALID
    )

    assert (
        base.state(
            "K:duration"
        )
        is KnowledgeState.STALE
    )


def test_retraction_stales_downstream_derivation():
    base = populate_new()

    base.retract(
        "K:end"
    )

    assert (
        base.state(
            "K:end"
        )
        is KnowledgeState.RETRACTED
    )

    assert (
        base.state(
            "K:duration"
        )
        is KnowledgeState.STALE
    )


def test_stale_derivation_retains_original_warrant():
    base = populate_new()

    before = base.get(
        "K:duration"
    )

    assert isinstance(
        before.warrant,
        DerivationWarrant,
    )

    original_warrant = (
        before.warrant
    )

    base.retract(
        "K:end"
    )

    after = base.get(
        "K:duration",
        require_active=False,
    )

    assert (
        base.state(
            "K:duration"
        )
        is KnowledgeState.STALE
    )

    assert (
        after.warrant
        == original_warrant
    )


def test_stale_knowledge_cannot_serve_as_active_premise():
    base = populate_new()

    base.retract(
        "K:end"
    )

    with raises(
        InactiveKnowledge
    ):
        base.get(
            "K:duration"
        )


def test_stale_support_is_historical_not_active():
    base = populate_new()

    proposition = (
        base.get(
            "K:duration"
        ).proposition
    )

    assert (
        base.support(
            proposition
        ).state
        is SupportState.FOR
    )

    base.retract(
        "K:end"
    )

    assert (
        base.support(
            proposition
        ).state
        is SupportState.NEITHER
    )

    assert (
        base.support(
            proposition,
            active_only=False,
        ).state
        is SupportState.FOR
    )


def test_stale_lineage_remains_historically_available():
    base = populate_new()

    base.retract(
        "K:end"
    )

    assert (
        base.assertion_roots(
            "K:duration"
        )
        == (
            "K:end",
            "K:start",
        )
    )
