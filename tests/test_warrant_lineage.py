from veridic.catalog import (
    DURATION,
    TIMESTAMP_END,
    TIMESTAMP_START,
)
from veridic.domain_catalog import (
    DIMENSIONLESS_SCALAR,
)
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import FieldValue
from veridic.information import (
    negate,
    value_statement,
)
from veridic.knowledge import Provenance
from veridic.knowledge_model import (
    KnowledgeBase,
)
from veridic.vocabulary import Operation


def build_base():
    return KnowledgeBase(
        build_domain_runtime()
    )


def duration_five():
    return value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )


def test_direct_assertion_is_its_own_root():
    base = build_base()

    base.assert_value(
        "K:duration",
        FieldValue(
            DURATION,
            5.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    assert (
        base.assertion_roots(
            "K:duration"
        )
        == (
            "K:duration",
        )
    )


def test_derived_duration_has_input_assertions_as_roots():
    base = build_base()

    base.assert_value(
        "K:start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="clock-A"
        ),
    )

    base.assert_value(
        "K:end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="clock-B"
        ),
    )

    base.derive_value(
        "K:duration",
        DURATION,
        Operation.SUB,
        "K:end",
        "K:start",
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


def test_deep_derivation_does_not_create_new_roots():
    base = build_base()

    base.assert_value(
        "K:duration",
        FieldValue(
            DURATION,
            5.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    base.assert_value(
        "K:one",
        FieldValue(
            DIMENSIONLESS_SCALAR,
            1.0,
        ),
        provenance=Provenance(
            source="constant"
        ),
    )

    base.derive_value(
        "K:branch-1",
        DURATION,
        Operation.MUL,
        "K:duration",
        "K:one",
    )

    base.derive_value(
        "K:branch-2",
        DURATION,
        Operation.MUL,
        "K:branch-1",
        "K:one",
    )

    assert (
        base.assertion_roots(
            "K:branch-2"
        )
        == (
            "K:duration",
            "K:one",
        )
    )


def test_many_warrants_from_same_roots_are_one_lineage_group():
    base = build_base()

    proposition = duration_five()

    base.assert_value(
        "K:duration",
        FieldValue(
            DURATION,
            5.0,
        ),
        provenance=Provenance(
            source="sensor"
        ),
    )

    base.assert_value(
        "K:one",
        FieldValue(
            DIMENSIONLESS_SCALAR,
            1.0,
        ),
        provenance=Provenance(
            source="constant"
        ),
    )

    base.derive_value(
        "K:branch-1",
        DURATION,
        Operation.MUL,
        "K:duration",
        "K:one",
    )

    base.derive_value(
        "K:branch-2",
        DURATION,
        Operation.MUL,
        "K:duration",
        "K:one",
    )

    base.derive_value(
        "K:branch-3",
        DURATION,
        Operation.MUL,
        "K:branch-1",
        "K:one",
    )

    analysis = base.support_lineage(
        proposition
    )

    assert (
        analysis.for_warrant_count
        == 4
    )

    assert (
        analysis.for_lineage_count
        == 1
    )

    assert (
        analysis.redundant_for_warrants
        == 3
    )


def test_separate_assertion_adds_separate_lineage_group():
    base = build_base()

    proposition = duration_five()

    base.assert_value(
        "K:duration:A",
        FieldValue(
            DURATION,
            5.0,
        ),
        provenance=Provenance(
            source="sensor-A"
        ),
    )

    base.assert_value(
        "K:one",
        FieldValue(
            DIMENSIONLESS_SCALAR,
            1.0,
        ),
        provenance=Provenance(
            source="constant"
        ),
    )

    base.derive_value(
        "K:derived",
        DURATION,
        Operation.MUL,
        "K:duration:A",
        "K:one",
    )

    base.assert_value(
        "K:duration:B",
        FieldValue(
            DURATION,
            5.0,
        ),
        provenance=Provenance(
            source="sensor-B"
        ),
    )

    analysis = base.support_lineage(
        proposition
    )

    assert (
        analysis.for_warrant_count
        == 3
    )

    assert (
        analysis.for_lineage_count
        == 2
    )


def test_shared_auxiliary_root_makes_lineages_dependent():
    base = build_base()

    proposition = duration_five()

    base.assert_value(
        "K:A",
        FieldValue(
            DURATION,
            5.0,
        ),
        provenance=Provenance(
            source="sensor-A"
        ),
    )

    base.assert_value(
        "K:B",
        FieldValue(
            DURATION,
            5.0,
        ),
        provenance=Provenance(
            source="sensor-B"
        ),
    )

    base.assert_value(
        "K:shared-one",
        FieldValue(
            DIMENSIONLESS_SCALAR,
            1.0,
        ),
        provenance=Provenance(
            source="shared-constant"
        ),
    )

    base.derive_value(
        "K:A-derived",
        DURATION,
        Operation.MUL,
        "K:A",
        "K:shared-one",
    )

    base.derive_value(
        "K:B-derived",
        DURATION,
        Operation.MUL,
        "K:B",
        "K:shared-one",
    )

    analysis = base.support_lineage(
        proposition
    )

    assert (
        analysis.for_warrant_count
        == 4
    )

    assert (
        analysis.for_lineage_count
        == 1
    )


def test_positive_and_negative_lineages_are_analyzed_separately():
    base = build_base()

    proposition = duration_five()

    base.assert_information(
        "K:for:A",
        proposition,
        provenance=Provenance(
            source="sensor-A"
        ),
    )

    base.assert_information(
        "K:for:B",
        proposition,
        provenance=Provenance(
            source="sensor-B"
        ),
    )

    base.assert_information(
        "K:against",
        negate(
            proposition
        ),
        provenance=Provenance(
            source="sensor-C"
        ),
    )

    analysis = base.support_lineage(
        proposition
    )

    assert (
        analysis.for_warrant_count
        == 2
    )

    assert (
        analysis.for_lineage_count
        == 2
    )

    assert (
        analysis.against_warrant_count
        == 1
    )

    assert (
        analysis.against_lineage_count
        == 1
    )


def test_asserted_inputs_can_produce_independent_derived_lineage():
    base = build_base()

    proposition = duration_five()

    base.assert_value(
        "K:start",
        FieldValue(
            TIMESTAMP_START,
            10.0,
        ),
        provenance=Provenance(
            source="clock-A"
        ),
    )

    base.assert_value(
        "K:end",
        FieldValue(
            TIMESTAMP_END,
            15.0,
        ),
        provenance=Provenance(
            source="clock-B"
        ),
    )

    base.derive_value(
        "K:derived-duration",
        DURATION,
        Operation.SUB,
        "K:end",
        "K:start",
    )

    base.assert_information(
        "K:direct-duration",
        proposition,
        provenance=Provenance(
            source="duration-sensor"
        ),
    )

    analysis = base.support_lineage(
        proposition
    )

    assert (
        analysis.for_warrant_count
        == 2
    )

    assert (
        analysis.for_lineage_count
        == 2
    )

    groups = (
        analysis.for_groups
    )

    assert {
        group.assertion_roots
        for group
        in groups
    } == {
        (
            "K:direct-duration",
        ),
        (
            "K:end",
            "K:start",
        ),
    }
