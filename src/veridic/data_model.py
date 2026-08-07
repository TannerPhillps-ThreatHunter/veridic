"""Experimental foundational Veridic Data Model.

Candidate primitives:

    Identity
    Datum
    Domain
    Relation

The module intentionally does not replace Field.

It tests whether familiar data structures can be reconstructed from
these smaller concepts before any substrate migration is attempted.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class DataModelError(ValueError):
    """Base foundational Data Model error."""


class RelationArityError(DataModelError):
    """A Relation was instantiated with the wrong arity."""


@dataclass(frozen=True, slots=True)
class Identity:
    """Continuity token for one particular represented thing.

    Identity is not an identifier Datum.

    The token is an implementation handle for identity, not a claim
    that identity metaphysically reduces to text.
    """

    token: str

    def __post_init__(self) -> None:
        if not self.token:
            raise DataModelError(
                "Identity token cannot be empty"
            )


@dataclass(frozen=True, slots=True)
class Datum:
    """Represented content without complete semantic interpretation."""

    value: Any


@dataclass(frozen=True, slots=True)
class Domain:
    """Identity of a semantic possibility space.

    Domain is deliberately minimal in this experiment.

    Characteristics of a Domain are expressed relationally rather than
    embedded directly here.

    This means Phase 18 does not yet prove Domain irreducible.
    """

    identity: Identity


@dataclass(frozen=True, slots=True)
class Value:
    """Derived semantic value.

    Value is not introduced as a primitive.

        Value = Domain + Datum
    """

    domain: Domain
    datum: Datum


@dataclass(frozen=True, slots=True)
class Relation:
    """General n-ary structural or semantic Relation."""

    identity: Identity
    name: str
    arity: int

    def __post_init__(self) -> None:
        if not self.name:
            raise DataModelError(
                "Relation name cannot be empty"
            )

        if self.arity < 1:
            raise DataModelError(
                "Relation arity must be positive"
            )

    def __call__(
        self,
        *terms: Any,
    ) -> RelationFact:
        if len(terms) != self.arity:
            raise RelationArityError(
                f"{self.name} expects "
                f"{self.arity} terms, "
                f"received {len(terms)}"
            )

        return RelationFact(
            relation=self,
            terms=tuple(terms),
        )


@dataclass(frozen=True, slots=True)
class RelationFact:
    """Derived application of a Relation to terms."""

    relation: Relation
    terms: tuple[Any, ...]


@dataclass(frozen=True, slots=True)
class DataState:
    """Immutable collection of represented relational structure."""

    facts: tuple[
        RelationFact,
        ...,
    ] = ()

    def add(
        self,
        *facts: RelationFact,
    ) -> DataState:
        return DataState(
            facts=(
                self.facts
                + tuple(facts)
            )
        )

    def facts_for(
        self,
        relation: Relation,
        *leading_terms: Any,
    ) -> tuple[
        RelationFact,
        ...,
    ]:
        size = len(
            leading_terms
        )

        return tuple(
            fact
            for fact
            in self.facts
            if (
                fact.relation
                == relation
                and fact.terms[:size]
                == leading_terms
            )
        )


__all__ = [
    "DataModelError",
    "DataState",
    "Datum",
    "Domain",
    "Identity",
    "Relation",
    "RelationArityError",
    "RelationFact",
    "Value",
]
