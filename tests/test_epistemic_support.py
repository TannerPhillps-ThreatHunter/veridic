from veridic.catalog import (
    DURATION,
)
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import FieldValue
from veridic.information import (
    negate,
    value_statement,
)
from veridic.knowledge import (
    KnowledgeState,
    Provenance,
)
from veridic.knowledge_model import (
    KnowledgeBase,
)
from veridic.support import (
    SupportState,
)


def build_base():
    return KnowledgeBase(
        build_domain_runtime()
    )


def duration_proposition():
    return value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )


def test_no_warrant_means_neither():
    base = build_base()

    proposition = (
        duration_proposition()
    )

    support = base.support(
        proposition
    )

    assert (
        support.state
        is SupportState.NEITHER
    )

    assert support.unsupported


def test_positive_warrant_means_for():
    base = build_base()

    proposition = (
        duration_proposition()
    )

    base.assert_information(
        "K:positive",
        proposition,
        provenance=Provenance(
            source="source-A"
        ),
    )

    support = base.support(
        proposition
    )

    assert (
        support.state
        is SupportState.FOR
    )

    assert (
        support.for_knowledge
        == (
            "K:positive",
        )
    )

    assert (
        support.against_knowledge
        == ()
    )


def test_negative_warrant_means_against():
    base = build_base()

    proposition = (
        duration_proposition()
    )

    base.assert_information(
        "K:negative",
        negate(
            proposition
        ),
        provenance=Provenance(
            source="source-B"
        ),
    )

    support = base.support(
        proposition
    )

    assert (
        support.state
        is SupportState.AGAINST
    )

    assert (
        support.for_knowledge
        == ()
    )

    assert (
        support.against_knowledge
        == (
            "K:negative",
        )
    )


def test_opposing_warrants_mean_both():
    base = build_base()

    proposition = (
        duration_proposition()
    )

    base.assert_information(
        "K:positive",
        proposition,
        provenance=Provenance(
            source="source-A"
        ),
    )

    base.assert_information(
        "K:negative",
        negate(
            proposition
        ),
        provenance=Provenance(
            source="source-B"
        ),
    )

    support = base.support(
        proposition
    )

    assert (
        support.state
        is SupportState.BOTH
    )

    assert support.contested

    assert (
        support.for_knowledge
        == (
            "K:positive",
        )
    )

    assert (
        support.against_knowledge
        == (
            "K:negative",
        )
    )


def test_multiple_positive_warrants_are_preserved():
    base = build_base()

    proposition = (
        duration_proposition()
    )

    base.assert_information(
        "K:A",
        proposition,
        provenance=Provenance(
            source="source-A"
        ),
    )

    base.assert_information(
        "K:B",
        proposition,
        provenance=Provenance(
            source="source-B"
        ),
    )

    support = base.support(
        proposition
    )

    assert (
        support.state
        is SupportState.FOR
    )

    assert (
        support.for_knowledge
        == (
            "K:A",
            "K:B",
        )
    )


def test_invalid_warrant_does_not_count_as_active_support():
    base = build_base()

    proposition = (
        duration_proposition()
    )

    base.assert_information(
        "K:positive",
        proposition,
        provenance=Provenance(
            source="source-A"
        ),
    )

    base.invalidate(
        "K:positive"
    )

    support = base.support(
        proposition
    )

    assert (
        support.state
        is SupportState.NEITHER
    )

    historical = base.support(
        proposition,
        active_only=False,
    )

    assert (
        historical.state
        is SupportState.FOR
    )


def test_retracted_negative_warrant_resolves_active_contest():
    base = build_base()

    proposition = (
        duration_proposition()
    )

    base.assert_information(
        "K:positive",
        proposition,
        provenance=Provenance(
            source="source-A"
        ),
    )

    base.assert_information(
        "K:negative",
        negate(
            proposition
        ),
        provenance=Provenance(
            source="source-B"
        ),
    )

    assert (
        base.support(
            proposition
        ).state
        is SupportState.BOTH
    )

    base.retract(
        "K:negative"
    )

    assert (
        base.support(
            proposition
        ).state
        is SupportState.FOR
    )

    assert (
        base.state(
            "K:negative"
        )
        is KnowledgeState.RETRACTED
    )


def test_support_is_relative_to_queried_polarity():
    base = build_base()

    proposition = (
        duration_proposition()
    )

    negative = negate(
        proposition
    )

    base.assert_information(
        "K:positive",
        proposition,
        provenance=Provenance(
            source="source-A"
        ),
    )

    assert (
        base.support(
            proposition
        ).state
        is SupportState.FOR
    )

    assert (
        base.support(
            negative
        ).state
        is SupportState.AGAINST
    )
