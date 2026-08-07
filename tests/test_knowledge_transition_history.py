from dataclasses import FrozenInstanceError

from veridic.catalog import (
    DURATION,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import FieldValue
from veridic.knowledge import Provenance
from veridic.knowledge_model import (
    KnowledgeBase,
)
from veridic.lifecycle import (
    KnowledgeState,
    KnowledgeTransition,
)
from veridic.utilities.testing import raises
from veridic.vocabulary import Operation


def build_base():
    base = KnowledgeBase(
        build_domain_runtime()
    )

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


def test_knowledge_content_has_no_lifecycle_state():
    base = build_base()

    knowledge = base.get(
        "K:duration"
    )

    assert not hasattr(
        knowledge,
        "state",
    )


def test_creation_records_initial_transition():
    base = build_base()

    history = base.history(
        "K:end"
    )

    assert len(history) == 1

    transition = history[0]

    assert isinstance(
        transition,
        KnowledgeTransition,
    )

    assert (
        transition.from_state
        is None
    )

    assert (
        transition.to_state
        is KnowledgeState.ACTIVE
    )

    assert (
        transition.reason
        == "created"
    )


def test_current_state_is_derived_from_history():
    base = build_base()

    assert (
        base.state(
            "K:end"
        )
        is KnowledgeState.ACTIVE
    )

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
        base.history(
            "K:end"
        )[-1].to_state
        is KnowledgeState.INVALID
    )


def test_invalidation_history_preserves_cause():
    base = build_base()

    base.invalidate(
        "K:end"
    )

    target = base.history(
        "K:end"
    )

    dependent = base.history(
        "K:duration"
    )

    assert (
        tuple(
            transition.to_state
            for transition
            in target
        )
        == (
            KnowledgeState.ACTIVE,
            KnowledgeState.INVALID,
        )
    )

    assert (
        tuple(
            transition.to_state
            for transition
            in dependent
        )
        == (
            KnowledgeState.ACTIVE,
            KnowledgeState.STALE,
        )
    )

    assert (
        dependent[-1].reason
        == "premise-invalidated"
    )

    assert (
        dependent[-1].cause
        == "K:end"
    )


def test_retraction_history_preserves_cause():
    base = build_base()

    base.retract(
        "K:end"
    )

    dependent = base.history(
        "K:duration"
    )

    assert (
        dependent[-1].to_state
        is KnowledgeState.STALE
    )

    assert (
        dependent[-1].reason
        == "premise-retracted"
    )

    assert (
        dependent[-1].cause
        == "K:end"
    )


def test_same_current_state_can_have_different_history():
    invalidated = build_base()

    invalidated.invalidate(
        "K:end"
    )

    retracted = build_base()

    retracted.retract(
        "K:end"
    )

    assert (
        invalidated.state(
            "K:duration"
        )
        is KnowledgeState.STALE
    )

    assert (
        retracted.state(
            "K:duration"
        )
        is KnowledgeState.STALE
    )

    assert (
        invalidated.history(
            "K:duration"
        )[-1].reason
        != retracted.history(
            "K:duration"
        )[-1].reason
    )


def test_transition_records_are_immutable():
    base = build_base()

    transition = base.history(
        "K:end"
    )[0]

    with raises(
        FrozenInstanceError
    ):
        transition.reason = "changed"


def test_history_is_returned_as_immutable_tuple():
    base = build_base()

    history = base.history(
        "K:end"
    )

    assert isinstance(
        history,
        tuple,
    )


def test_transition_sequence_preserves_append_order():
    base = build_base()

    base.invalidate(
        "K:end"
    )

    transitions = (
        base.history(
            "K:start"
        )
        + base.history(
            "K:end"
        )
        + base.history(
            "K:duration"
        )
    )

    sequences = tuple(
        transition.sequence
        for transition
        in transitions
    )

    assert len(
        set(sequences)
    ) == len(sequences)

    assert min(sequences) == 1
