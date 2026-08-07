"""Veridic Information Model.

Data becomes Information when Veridic forms a proposition about it.

The candidate irreducible informational primitive is:

    Proposition

An atomic Proposition is the application of a semantic relation to
data-bearing terms.

    P = R(t1, ..., tn)

Compound Propositions are constructed logically.

Information is not Knowledge.

A Proposition may exist in Veridic without possessing epistemic
warrant.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, TypeAlias

from .field import Field, FieldValue
from .utilities.units import Unit
from .vocabulary import Scale


class InformationError(RuntimeError):
    """Base Information Model error."""


class ArityError(InformationError):
    """A relation was instantiated with the wrong arity."""


class NotValueProposition(InformationError):
    """A Proposition does not encode a Field value statement."""


@dataclass(frozen=True, slots=True)
class SemanticValue:
    """Intrinsic semantic content of a FieldValue.

    Role and contextual Field identity are intentionally excluded.

    The Field identifies where the value occurs.

    SemanticValue identifies what value occurs there.
    """

    classification_path: str
    scale: Scale
    unit: Unit | None
    datum: Any

    @classmethod
    def from_field_value(
        cls,
        value: FieldValue,
    ) -> SemanticValue:
        return cls(
            classification_path=(
                value.field.classification_path
            ),
            scale=value.field.scale,
            unit=value.field.unit,
            datum=value.value,
        )


@dataclass(frozen=True, slots=True)
class InformationRelation:
    """Executable representation of an informational relation.

    Relation remains a Data Model candidate primitive.

    This class is the Information Model's current application surface
    for such a relation.
    """

    name: str
    arity: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError(
                "Information relation name cannot be empty"
            )

        if self.arity < 1:
            raise ValueError(
                "Information relation arity must be positive"
            )

    def __call__(
        self,
        *terms: Any,
    ) -> AtomicProposition:
        if len(terms) != self.arity:
            raise ArityError(
                f"{self.name} expects "
                f"{self.arity} terms, "
                f"received {len(terms)}"
            )

        return AtomicProposition(
            relation=self,
            terms=tuple(terms),
        )


@dataclass(frozen=True, slots=True)
class AtomicProposition:
    """Atomic truth-apt informational statement."""

    relation: InformationRelation
    terms: tuple[Any, ...]


class LogicalOperator(str, Enum):
    NOT = "not"
    AND = "and"
    OR = "or"
    IMPLIES = "implies"


@dataclass(frozen=True, slots=True)
class LogicalProposition:
    """Logical composition of Propositions."""

    operator: LogicalOperator
    operands: tuple[Proposition, ...]

    def __post_init__(self) -> None:
        expected = (
            1
            if self.operator is LogicalOperator.NOT
            else 2
        )

        if len(self.operands) != expected:
            raise ArityError(
                f"{self.operator.value} expects "
                f"{expected} operands"
            )


Proposition: TypeAlias = (
    AtomicProposition
    | LogicalProposition
)


HAS_VALUE = InformationRelation(
    name="has_value",
    arity=2,
)


def value_statement(
    value: FieldValue,
) -> AtomicProposition:
    """Construct Information from one instantiated Field value."""

    return HAS_VALUE(
        value.field,
        SemanticValue.from_field_value(
            value
        ),
    )


def field_value_from(
    proposition: Proposition,
) -> FieldValue:
    """Recover a FieldValue from a HAS_VALUE Proposition."""

    if not isinstance(
        proposition,
        AtomicProposition,
    ):
        raise NotValueProposition(
            "Logical Proposition is not a direct value statement"
        )

    if proposition.relation != HAS_VALUE:
        raise NotValueProposition(
            "Proposition relation is not HAS_VALUE"
        )

    field, semantic_value = (
        proposition.terms
    )

    if not isinstance(
        field,
        Field,
    ):
        raise NotValueProposition(
            "HAS_VALUE subject must be a Field"
        )

    if not isinstance(
        semantic_value,
        SemanticValue,
    ):
        raise NotValueProposition(
            "HAS_VALUE object must be SemanticValue"
        )

    expected = (
        field.classification_path,
        field.scale,
        field.unit,
    )

    actual = (
        semantic_value.classification_path,
        semantic_value.scale,
        semantic_value.unit,
    )

    if expected != actual:
        raise NotValueProposition(
            "SemanticValue contradicts Field semantics"
        )

    return FieldValue(
        field=field,
        value=semantic_value.datum,
    )


def negate(
    proposition: Proposition,
) -> Proposition:
    if (
        isinstance(
            proposition,
            LogicalProposition,
        )
        and proposition.operator
        is LogicalOperator.NOT
    ):
        return proposition.operands[0]

    return LogicalProposition(
        operator=LogicalOperator.NOT,
        operands=(proposition,),
    )


def conjunction(
    left: Proposition,
    right: Proposition,
) -> LogicalProposition:
    return LogicalProposition(
        operator=LogicalOperator.AND,
        operands=(
            left,
            right,
        ),
    )


def disjunction(
    left: Proposition,
    right: Proposition,
) -> LogicalProposition:
    return LogicalProposition(
        operator=LogicalOperator.OR,
        operands=(
            left,
            right,
        ),
    )


def implication(
    left: Proposition,
    right: Proposition,
) -> LogicalProposition:
    return LogicalProposition(
        operator=LogicalOperator.IMPLIES,
        operands=(
            left,
            right,
        ),
    )


class InformationState:
    """Open-world collection of represented Propositions.

    Presence means represented, not true.

    Absence means not represented, not false.

    P and NOT P may coexist because representation does not itself
    determine truth or epistemic warrant.
    """

    def __init__(
        self,
        *propositions: Proposition,
    ) -> None:
        self._propositions: list[
            Proposition
        ] = []

        for proposition in propositions:
            self.add(
                proposition
            )

    @property
    def propositions(
        self,
    ) -> tuple[Proposition, ...]:
        return tuple(
            self._propositions
        )

    def add(
        self,
        proposition: Proposition,
    ) -> None:
        if proposition not in self._propositions:
            self._propositions.append(
                proposition
            )

    def contains(
        self,
        proposition: Proposition,
    ) -> bool:
        return (
            proposition
            in self._propositions
        )

    def contains_negation(
        self,
        proposition: Proposition,
    ) -> bool:
        return self.contains(
            negate(proposition)
        )

    def polarity(
        self,
        proposition: Proposition,
    ) -> tuple[bool, bool]:
        """Return represented positive and negative forms.

        The tuple is:

            (
                P represented,
                NOT P represented,
            )

        This is representational state only.

        It is not Truth and not epistemic Support.
        """

        return (
            self.contains(
                proposition
            ),
            self.contains_negation(
                proposition
            ),
        )


def format_proposition(
    proposition: Proposition,
) -> str:
    if isinstance(
        proposition,
        AtomicProposition,
    ):
        if proposition.relation == HAS_VALUE:
            field, value = proposition.terms

            assert isinstance(
                field,
                Field,
            )

            assert isinstance(
                value,
                SemanticValue,
            )

            suffix = ""

            if value.unit is not None:
                suffix = (
                    " "
                    + value.unit.symbol
                )

            return (
                f"{field.name} = "
                f"{value.datum}"
                f"{suffix}"
            )

        terms = ", ".join(
            str(term)
            for term
            in proposition.terms
        )

        return (
            f"{proposition.relation.name}"
            f"({terms})"
        )

    if (
        proposition.operator
        is LogicalOperator.NOT
    ):
        return (
            "NOT "
            + format_proposition(
                proposition.operands[0]
            )
        )

    operator = {
        LogicalOperator.AND: "AND",
        LogicalOperator.OR: "OR",
        LogicalOperator.IMPLIES: "IMPLIES",
    }[
        proposition.operator
    ]

    return (
        "("
        + format_proposition(
            proposition.operands[0]
        )
        + f" {operator} "
        + format_proposition(
            proposition.operands[1]
        )
        + ")"
    )


__all__ = [
    "HAS_VALUE",
    "ArityError",
    "AtomicProposition",
    "InformationError",
    "InformationRelation",
    "InformationState",
    "LogicalOperator",
    "LogicalProposition",
    "NotValueProposition",
    "Proposition",
    "SemanticValue",
    "conjunction",
    "disjunction",
    "field_value_from",
    "format_proposition",
    "implication",
    "negate",
    "value_statement",
]
