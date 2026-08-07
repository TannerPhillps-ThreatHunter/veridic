from dataclasses import replace

from veridic.catalog import (
    BYTE_COUNT,
    DURATION,
)
from veridic.data_model import (
    DataState,
    Datum,
    Domain,
    Identity,
    Relation,
    RelationArityError,
    Value,
)
from veridic.field_projection import (
    DOMAIN_CLASSIFICATION,
    DOMAIN_SCALE,
    FIELD_DOMAIN,
    FIELD_ROLE,
    decompose_field,
    reconstruct_field,
)
from veridic.utilities.testing import raises


def test_identity_is_not_identifier_datum():
    identity = Identity(
        "entity:42"
    )

    identifier = Datum(
        "entity:42"
    )

    assert identity != identifier


def test_equal_datums_can_have_distinct_identity():
    first = Identity(
        "occurrence:A"
    )

    second = Identity(
        "occurrence:B"
    )

    datum_a = Datum(
        5
    )

    datum_b = Datum(
        5
    )

    assert datum_a == datum_b
    assert first != second


def test_value_reduces_to_domain_plus_datum():
    duration = Domain(
        Identity(
            "domain:duration"
        )
    )

    bytes_ = Domain(
        Identity(
            "domain:bytes"
        )
    )

    datum = Datum(
        5
    )

    duration_value = Value(
        duration,
        datum,
    )

    byte_value = Value(
        bytes_,
        datum,
    )

    assert (
        duration_value.datum
        == byte_value.datum
    )

    assert (
        duration_value
        != byte_value
    )


def test_relation_is_general_n_ary_structure():
    edge = Relation(
        identity=Identity(
            "relation:edge"
        ),
        name="edge",
        arity=3,
    )

    source = Identity(
        "node:A"
    )

    destination = Identity(
        "node:B"
    )

    fact = edge(
        source,
        Datum("connects"),
        destination,
    )

    assert (
        fact.terms
        == (
            source,
            Datum("connects"),
            destination,
        )
    )


def test_relation_enforces_arity():
    relation = Relation(
        identity=Identity(
            "relation:test"
        ),
        name="test",
        arity=2,
    )

    with raises(
        RelationArityError
    ):
        relation(
            Datum(1)
        )


def test_missing_is_absence_of_relation():
    binds = Relation(
        identity=Identity(
            "relation:binds"
        ),
        name="binds",
        arity=2,
    )

    field = Identity(
        "field:example"
    )

    state = DataState()

    assert (
        state.facts_for(
            binds,
            field,
        )
        == ()
    )


def test_null_is_explicit_value_not_missing():
    binds = Relation(
        identity=Identity(
            "relation:binds"
        ),
        name="binds",
        arity=2,
    )

    field = Identity(
        "field:example"
    )

    null_domain = Domain(
        Identity(
            "domain:null"
        )
    )

    null_value = Value(
        null_domain,
        Datum(None),
    )

    state = DataState().add(
        binds(
            field,
            null_value,
        )
    )

    facts = state.facts_for(
        binds,
        field,
    )

    assert len(facts) == 1

    assert (
        facts[0].terms[1]
        == null_value
    )


def test_existing_field_round_trips_through_primitives():
    decomposition = decompose_field(
        DURATION,
        field_identity=Identity(
            "field:duration:instance"
        ),
        domain_identity=Identity(
            "domain:duration"
        ),
    )

    restored = reconstruct_field(
        decomposition
    )

    assert restored == DURATION


def test_field_identity_is_independent_of_field_name():
    identity = Identity(
        "field:internal:001"
    )

    decomposition = decompose_field(
        DURATION,
        field_identity=identity,
        domain_identity=Identity(
            "domain:duration"
        ),
    )

    assert (
        identity.token
        != DURATION.name
    )

    restored = reconstruct_field(
        decomposition
    )

    assert (
        restored.name
        == DURATION.name
    )


def test_role_is_field_relation_not_domain_identity():
    shared_domain = Identity(
        "domain:duration"
    )

    first = decompose_field(
        DURATION,
        field_identity=Identity(
            "field:first"
        ),
        domain_identity=shared_domain,
    )

    alternate = replace(
        DURATION,
        name="alternate.duration",
        role="alternate",
    )

    second = decompose_field(
        alternate,
        field_identity=Identity(
            "field:second"
        ),
        domain_identity=shared_domain,
    )

    assert (
        first.domain
        == second.domain
    )

    first_role = (
        first.state.facts_for(
            FIELD_ROLE,
            first.field_identity,
        )[0].terms[1]
    )

    second_role = (
        second.state.facts_for(
            FIELD_ROLE,
            second.field_identity,
        )[0].terms[1]
    )

    assert first_role != second_role


def test_domain_characteristics_are_relational():
    decomposition = decompose_field(
        BYTE_COUNT,
        field_identity=Identity(
            "field:bytes"
        ),
        domain_identity=Identity(
            "domain:bytes"
        ),
    )

    assert len(
        decomposition.state.facts_for(
            FIELD_DOMAIN,
            decomposition.field_identity,
        )
    ) == 1

    assert len(
        decomposition.state.facts_for(
            DOMAIN_CLASSIFICATION,
            decomposition.domain,
        )
    ) == 1

    assert len(
        decomposition.state.facts_for(
            DOMAIN_SCALE,
            decomposition.domain,
        )
    ) == 1
