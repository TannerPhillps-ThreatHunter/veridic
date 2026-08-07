"""Projection between the current Field model and Data primitives.

This module is an adapter.

It allows Veridic to test whether Field can be decomposed into
foundational Data Model structures without changing the operational
Field runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data_model import (
    DataState,
    Datum,
    Domain,
    Identity,
    Relation,
)
from .field import Field
from .hierarchy import Classification
from .invariant import Invariant
from .utilities.units import Unit
from .vocabulary import Scale


FIELD_NAME = Relation(
    identity=Identity(
        "relation:field-name"
    ),
    name="field_name",
    arity=2,
)

FIELD_DOMAIN = Relation(
    identity=Identity(
        "relation:field-domain"
    ),
    name="field_domain",
    arity=2,
)

DOMAIN_CLASSIFICATION = Relation(
    identity=Identity(
        "relation:domain-classification"
    ),
    name="domain_classification",
    arity=2,
)

DOMAIN_SCALE = Relation(
    identity=Identity(
        "relation:domain-scale"
    ),
    name="domain_scale",
    arity=2,
)

DOMAIN_UNIT = Relation(
    identity=Identity(
        "relation:domain-unit"
    ),
    name="domain_unit",
    arity=2,
)

FIELD_ROLE = Relation(
    identity=Identity(
        "relation:field-role"
    ),
    name="field_role",
    arity=2,
)

FIELD_INVARIANT = Relation(
    identity=Identity(
        "relation:field-invariant"
    ),
    name="field_invariant",
    arity=2,
)


@dataclass(frozen=True, slots=True)
class FieldDecomposition:
    """Relational decomposition of one current Field."""

    field_identity: Identity
    domain: Domain
    state: DataState


def decompose_field(
    field: Field,
    *,
    field_identity: Identity,
    domain_identity: Identity,
) -> FieldDecomposition:
    domain = Domain(
        identity=domain_identity
    )

    facts = [
        FIELD_NAME(
            field_identity,
            Datum(field.name),
        ),
        FIELD_DOMAIN(
            field_identity,
            domain,
        ),
        DOMAIN_CLASSIFICATION(
            domain,
            Datum(
                field.classification
            ),
        ),
        DOMAIN_SCALE(
            domain,
            Datum(
                field.scale
            ),
        ),
        FIELD_ROLE(
            field_identity,
            Datum(
                field.role
            ),
        ),
    ]

    if field.unit is not None:
        facts.append(
            DOMAIN_UNIT(
                domain,
                Datum(
                    field.unit
                ),
            )
        )

    for invariant in field.invariants:
        facts.append(
            FIELD_INVARIANT(
                field_identity,
                Datum(
                    invariant
                ),
            )
        )

    return FieldDecomposition(
        field_identity=field_identity,
        domain=domain,
        state=DataState(
            facts=tuple(
                facts
            )
        ),
    )


def _single_datum(
    decomposition: FieldDecomposition,
    relation: Relation,
    subject: object,
) -> object:
    facts = decomposition.state.facts_for(
        relation,
        subject,
    )

    if len(facts) != 1:
        raise ValueError(
            f"{relation.name}: "
            f"expected one fact, "
            f"found {len(facts)}"
        )

    datum = facts[0].terms[1]

    if not isinstance(
        datum,
        Datum,
    ):
        raise TypeError(
            f"{relation.name}: "
            "expected Datum"
        )

    return datum.value


def reconstruct_field(
    decomposition: FieldDecomposition,
) -> Field:
    name = _single_datum(
        decomposition,
        FIELD_NAME,
        decomposition.field_identity,
    )

    classification = _single_datum(
        decomposition,
        DOMAIN_CLASSIFICATION,
        decomposition.domain,
    )

    scale = _single_datum(
        decomposition,
        DOMAIN_SCALE,
        decomposition.domain,
    )

    role = _single_datum(
        decomposition,
        FIELD_ROLE,
        decomposition.field_identity,
    )

    unit_facts = (
        decomposition.state.facts_for(
            DOMAIN_UNIT,
            decomposition.domain,
        )
    )

    unit = None

    if unit_facts:
        if len(unit_facts) != 1:
            raise ValueError(
                "domain_unit: expected at most one fact"
            )

        wrapped = (
            unit_facts[0].terms[1]
        )

        if not isinstance(
            wrapped,
            Datum,
        ):
            raise TypeError(
                "domain_unit: expected Datum"
            )

        unit = wrapped.value

    invariant_facts = (
        decomposition.state.facts_for(
            FIELD_INVARIANT,
            decomposition.field_identity,
        )
    )

    invariants = tuple(
        fact.terms[1].value
        for fact
        in invariant_facts
        if isinstance(
            fact.terms[1],
            Datum,
        )
    )

    if not isinstance(
        name,
        str,
    ):
        raise TypeError(
            "Field name must reconstruct as str"
        )

    if not isinstance(
        classification,
        Classification,
    ):
        raise TypeError(
            "Field classification must reconstruct "
            "as Classification"
        )

    if not isinstance(
        scale,
        Scale,
    ):
        raise TypeError(
            "Field scale must reconstruct as Scale"
        )

    if not isinstance(
        role,
        str,
    ):
        raise TypeError(
            "Field role must reconstruct as str"
        )

    if (
        unit is not None
        and not isinstance(
            unit,
            Unit,
        )
    ):
        raise TypeError(
            "Field unit must reconstruct as Unit"
        )

    if not all(
        isinstance(
            invariant,
            Invariant,
        )
        for invariant
        in invariants
    ):
        raise TypeError(
            "Field invariants failed reconstruction"
        )

    return Field(
        name=name,
        classification=classification,
        scale=scale,
        role=role,
        unit=unit,
        invariants=invariants,
    )


__all__ = [
    "DOMAIN_CLASSIFICATION",
    "DOMAIN_SCALE",
    "DOMAIN_UNIT",
    "FIELD_DOMAIN",
    "FIELD_INVARIANT",
    "FIELD_NAME",
    "FIELD_ROLE",
    "FieldDecomposition",
    "decompose_field",
    "reconstruct_field",
]
