"""Warranted Veridic Knowledge.

Canonical candidate:

    Knowledge = Information + Warrant

where:

    Warrant =
        Assertion
        | Derivation

The earlier KnownValue experiment remains intact in veridic.knowledge.
This module tests the deeper Proposition-based formulation without
deleting that experimental lineage.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TypeAlias

from .execution import execute
from .field import Field, FieldValue
from .information import (
    Proposition,
    field_value_from,
    format_proposition,
    value_statement,
)
from .knowledge import (
    KnowledgeState,
    Provenance,
)
from .runtime import SemanticRuntime
from .vocabulary import Operation


class KnowledgeModelError(RuntimeError):
    """Base error for warranted Knowledge."""


class DuplicateKnowledge(
    KnowledgeModelError
):
    """Knowledge identity already exists."""


class UnknownKnowledge(
    KnowledgeModelError
):
    """Knowledge identity does not exist."""


class InactiveKnowledge(
    KnowledgeModelError
):
    """Knowledge cannot currently serve as a premise."""


class SemanticTargetMismatch(
    KnowledgeModelError
):
    """Derived semantics cannot occupy the requested target Field."""


@dataclass(frozen=True, slots=True)
class AssertionWarrant:
    """External epistemic warrant."""

    provenance: Provenance


@dataclass(frozen=True, slots=True)
class DerivationWarrant:
    """Internal epistemic warrant."""

    premises: tuple[str, ...]
    operation: Operation
    rule: str
    governing_laws: tuple[str, ...]


Warrant: TypeAlias = (
    AssertionWarrant
    | DerivationWarrant
)


@dataclass(frozen=True, slots=True)
class Knowledge:
    """One warranted Proposition.

    Knowledge identity is distinct from Proposition identity.

    Multiple Knowledge items may therefore warrant the same Proposition
    independently.
    """

    identity: str
    proposition: Proposition
    warrant: Warrant
    state: KnowledgeState = (
        KnowledgeState.ACTIVE
    )

    @property
    def asserted(self) -> bool:
        return isinstance(
            self.warrant,
            AssertionWarrant,
        )

    @property
    def derived(self) -> bool:
        return isinstance(
            self.warrant,
            DerivationWarrant,
        )


def _field_shape(
    field: Field,
) -> tuple[
    str,
    object,
    object,
]:
    return (
        field.classification_path,
        field.scale,
        field.unit,
    )


class KnowledgeBase:
    """Dependency-aware warranted Information store."""

    def __init__(
        self,
        runtime: SemanticRuntime,
    ) -> None:
        self._runtime = runtime

        self._items: dict[
            str,
            Knowledge,
        ] = {}

        self._dependents: dict[
            str,
            set[str],
        ] = {}

    def __contains__(
        self,
        identity: str,
    ) -> bool:
        return identity in self._items

    def _require_unique(
        self,
        identity: str,
    ) -> None:
        if identity in self._items:
            raise DuplicateKnowledge(
                identity
            )

    def get(
        self,
        identity: str,
        *,
        require_active: bool = True,
    ) -> Knowledge:
        try:
            knowledge = self._items[
                identity
            ]
        except KeyError as exc:
            raise UnknownKnowledge(
                identity
            ) from exc

        if (
            require_active
            and knowledge.state
            is not KnowledgeState.ACTIVE
        ):
            raise InactiveKnowledge(
                f"{identity}: "
                f"{knowledge.state.value}"
            )

        return knowledge

    def assert_information(
        self,
        identity: str,
        proposition: Proposition,
        *,
        provenance: Provenance,
    ) -> Knowledge:
        self._require_unique(
            identity
        )

        knowledge = Knowledge(
            identity=identity,
            proposition=proposition,
            warrant=AssertionWarrant(
                provenance=provenance
            ),
        )

        self._items[
            identity
        ] = knowledge

        self._dependents.setdefault(
            identity,
            set(),
        )

        return knowledge

    def assert_value(
        self,
        identity: str,
        value: FieldValue,
        *,
        provenance: Provenance,
    ) -> Knowledge:
        return self.assert_information(
            identity,
            value_statement(value),
            provenance=provenance,
        )

    def derive_value(
        self,
        identity: str,
        target: Field,
        operation: Operation,
        *premise_ids: str,
    ) -> Knowledge:
        self._require_unique(
            identity
        )

        premises = tuple(
            self.get(
                premise_id
            )
            for premise_id
            in premise_ids
        )

        operands = tuple(
            field_value_from(
                premise.proposition
            )
            for premise
            in premises
        )

        result = execute(
            self._runtime,
            operation,
            *operands,
        )

        if result.output is None:
            raise KnowledgeModelError(
                "Derivation produced no value-bearing output"
            )

        if (
            _field_shape(
                result.output.field
            )
            != _field_shape(
                target
            )
        ):
            raise SemanticTargetMismatch(
                "Derived Field semantics "
                f"{result.output.field.classification_path} "
                "cannot occupy target "
                f"{target.classification_path}"
            )

        if (
            self._runtime.contracts
            is not None
        ):
            (
                self._runtime.contracts
                .assert_coherent(target)
            )

        bound_value = FieldValue(
            field=target,
            value=result.output.value,
        )

        rule = (
            result.admission.rule.name
        )

        knowledge = Knowledge(
            identity=identity,
            proposition=value_statement(
                bound_value
            ),
            warrant=DerivationWarrant(
                premises=tuple(
                    premise.identity
                    for premise
                    in premises
                ),
                operation=operation,
                rule=rule,
                governing_laws=(
                    rule,
                ),
            ),
        )

        self._items[
            identity
        ] = knowledge

        self._dependents.setdefault(
            identity,
            set(),
        )

        for premise in premises:
            self._dependents.setdefault(
                premise.identity,
                set(),
            ).add(
                identity
            )

        return knowledge

    def warrants_for(
        self,
        proposition: Proposition,
        *,
        active_only: bool = False,
    ) -> tuple[Knowledge, ...]:
        matches = []

        for knowledge in (
            self._items.values()
        ):
            if (
                knowledge.proposition
                != proposition
            ):
                continue

            if (
                active_only
                and knowledge.state
                is not KnowledgeState.ACTIVE
            ):
                continue

            matches.append(
                knowledge
            )

        return tuple(
            sorted(
                matches,
                key=lambda item: (
                    item.identity
                ),
            )
        )

    def direct_dependents(
        self,
        identity: str,
    ) -> tuple[str, ...]:
        self.get(
            identity,
            require_active=False,
        )

        return tuple(
            sorted(
                self._dependents.get(
                    identity,
                    set(),
                )
            )
        )

    def dependents(
        self,
        identity: str,
    ) -> tuple[str, ...]:
        self.get(
            identity,
            require_active=False,
        )

        discovered: set[str] = set()

        pending = list(
            self._dependents.get(
                identity,
                set(),
            )
        )

        while pending:
            current = pending.pop()

            if current in discovered:
                continue

            discovered.add(
                current
            )

            pending.extend(
                self._dependents.get(
                    current,
                    set(),
                )
            )

        return tuple(
            sorted(
                discovered
            )
        )

    def invalidate(
        self,
        identity: str,
    ) -> None:
        self.get(
            identity,
            require_active=False,
        )

        pending = [
            identity,
            *self.dependents(
                identity
            ),
        ]

        for current in pending:
            knowledge = self._items[
                current
            ]

            if (
                knowledge.state
                is KnowledgeState.RETRACTED
            ):
                continue

            self._items[
                current
            ] = replace(
                knowledge,
                state=KnowledgeState.INVALID,
            )

    def retract(
        self,
        identity: str,
    ) -> None:
        knowledge = self.get(
            identity,
            require_active=False,
        )

        self._items[
            identity
        ] = replace(
            knowledge,
            state=KnowledgeState.RETRACTED,
        )

        for dependent in (
            self.dependents(identity)
        ):
            current = self._items[
                dependent
            ]

            if (
                current.state
                is not KnowledgeState.RETRACTED
            ):
                self._items[
                    dependent
                ] = replace(
                    current,
                    state=KnowledgeState.INVALID,
                )

    def explain(
        self,
        identity: str,
    ) -> str:
        knowledge = self.get(
            identity,
            require_active=False,
        )

        lines = [
            f"knowledge: {knowledge.identity}",
            (
                "information: "
                + format_proposition(
                    knowledge.proposition
                )
            ),
            (
                "state: "
                + knowledge.state.value
            ),
        ]

        if isinstance(
            knowledge.warrant,
            AssertionWarrant,
        ):
            lines.extend(
                (
                    "warrant: assertion",
                    (
                        "source: "
                        + knowledge.warrant
                        .provenance.source
                    ),
                )
            )

            return "\n".join(
                lines
            )

        lines.extend(
            (
                "warrant: derivation",
                (
                    "operation: "
                    + knowledge.warrant
                    .operation.value
                ),
                (
                    "rule: "
                    + knowledge.warrant.rule
                ),
                (
                    "premises: "
                    + ", ".join(
                        knowledge.warrant
                        .premises
                    )
                ),
            )
        )

        return "\n".join(
            lines
        )


__all__ = [
    "AssertionWarrant",
    "DerivationWarrant",
    "DuplicateKnowledge",
    "InactiveKnowledge",
    "Knowledge",
    "KnowledgeBase",
    "KnowledgeModelError",
    "SemanticTargetMismatch",
    "UnknownKnowledge",
    "Warrant",
]
