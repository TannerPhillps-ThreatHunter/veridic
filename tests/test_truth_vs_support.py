from veridic.catalog import DURATION
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import FieldValue
from veridic.information import (
    InformationState,
    negate,
    value_statement,
)
from veridic.interpretation import evaluate_truth
from veridic.knowledge import Provenance
from veridic.knowledge_model import (
    KnowledgeBase,
)
from veridic.support import SupportState
from veridic.utilities.truth import Truth


def proposition():
    return value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )


class UnknownInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return Truth.UNKNOWN


def test_truth_enum_remains_three_valued():
    assert set(Truth) == {
        Truth.TRUE,
        Truth.FALSE,
        Truth.UNKNOWN,
    }


def test_representation_does_not_imply_truth():
    p = proposition()

    information = InformationState(
        p
    )

    assert information.contains(p)

    assert (
        evaluate_truth(
            p,
            under=UnknownInterpretation(),
        )
        is Truth.UNKNOWN
    )


def test_truth_and_knowledge_support_are_distinct():
    p = proposition()

    knowledge = KnowledgeBase(
        build_domain_runtime()
    )

    knowledge.assert_information(
        "K:P",
        p,
        provenance=Provenance(
            source="source-A"
        ),
    )

    knowledge.assert_information(
        "K:not-P",
        negate(p),
        provenance=Provenance(
            source="source-B"
        ),
    )

    assert (
        evaluate_truth(
            p,
            under=UnknownInterpretation(),
        )
        is Truth.UNKNOWN
    )

    assert (
        knowledge.support(p).state
        is SupportState.BOTH
    )


def test_both_support_does_not_create_arbitrary_knowledge():
    p = proposition()

    q = value_statement(
        FieldValue(
            DURATION,
            8.0,
        )
    )

    knowledge = KnowledgeBase(
        build_domain_runtime()
    )

    knowledge.assert_information(
        "K:P",
        p,
        provenance=Provenance(
            source="source-A"
        ),
    )

    knowledge.assert_information(
        "K:not-P",
        negate(p),
        provenance=Provenance(
            source="source-B"
        ),
    )

    assert (
        knowledge.support(p).state
        is SupportState.BOTH
    )

    assert (
        knowledge.support(q).state
        is SupportState.NEITHER
    )
