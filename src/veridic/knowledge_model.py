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
from .lineage import (
    SupportLineage,
    WarrantLineage,
)
from .knowledge import (
    KnowledgeState,
    Provenance,
)
from .runtime import SemanticRuntime
from .support import EpistemicSupport
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

    def support(
        self,
        proposition: Proposition,
        *,
        active_only: bool = True,
    ) -> EpistemicSupport:
        """Return warranted support for and against a Proposition.

        Positive support consists of Knowledge warranting P.

        Negative support consists of Knowledge warranting NOT P.

        The two sets remain independent.
        """

        from .information import negate

        positive = self.warrants_for(
            proposition,
            active_only=active_only,
        )

        negative = self.warrants_for(
            negate(proposition),
            active_only=active_only,
        )

        return EpistemicSupport(
            proposition=proposition,
            for_knowledge=tuple(
                knowledge.identity
                for knowledge
                in positive
            ),
            against_knowledge=tuple(
                knowledge.identity
                for knowledge
                in negative
            ),
        )

    def assertion_roots(
        self,
        identity: str,
    ) -> tuple[str, ...]:
        """Return the asserted roots supporting one Knowledge item.

        A directly asserted Knowledge item is its own root.

        A derived Knowledge item recursively inherits the roots of its
        premises.

        The result describes epistemic ancestry, not source
        independence.
        """

        roots: set[str] = set()
        visiting: set[str] = set()
        visited: set[str] = set()

        def walk(
            current: str,
        ) -> None:
            if current in visited:
                return

            if current in visiting:
                raise KnowledgeModelError(
                    "Cyclic derivation lineage detected: "
                    f"{current}"
                )

            knowledge = self.get(
                current,
                require_active=False,
            )

            if isinstance(
                knowledge.warrant,
                AssertionWarrant,
            ):
                roots.add(
                    current
                )

                visited.add(
                    current
                )

                return

            visiting.add(
                current
            )

            for premise in (
                knowledge.warrant.premises
            ):
                walk(
                    premise
                )

            visiting.remove(
                current
            )

            visited.add(
                current
            )

        walk(
            identity
        )

        return tuple(
            sorted(
                roots
            )
        )

    def support_lineage(
        self,
        proposition: Proposition,
        *,
        active_only: bool = True,
    ) -> SupportLineage:
        """Analyze assertion-root ancestry around a Proposition."""

        from .information import negate

        positive = self.warrants_for(
            proposition,
            active_only=active_only,
        )

        negative = self.warrants_for(
            negate(proposition),
            active_only=active_only,
        )

        return SupportLineage(
            proposition=proposition,
            for_lineages=tuple(
                WarrantLineage(
                    knowledge=knowledge.identity,
                    assertion_roots=(
                        self.assertion_roots(
                            knowledge.identity
                        )
                    ),
                )
                for knowledge
                in positive
            ),
            against_lineages=tuple(
                WarrantLineage(
                    knowledge=knowledge.identity,
                    assertion_roots=(
                        self.assertion_roots(
                            knowledge.identity
                        )
                    ),
                )
                for knowledge
                in negative
            ),
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

    def _stale_dependents(
        self,
        identity: str,
    ) -> None:
        """Mark downstream Knowledge stale.

        Staleness means the warrant remains historically well-formed,
        but the Knowledge is no longer currently supported because one
        of its premises ceased to be active.
        """

        for dependent in self.dependents(
            identity
        ):
            knowledge = self._items[
                dependent
            ]

            if (
                knowledge.state
                is KnowledgeState.ACTIVE
            ):
                self._items[
                    dependent
                ] = replace(
                    knowledge,
                    state=KnowledgeState.STALE,
                )

    def invalidate(
        self,
        identity: str,
    ) -> None:
        """Declare one Knowledge item invalid.

        Invalidity applies to the target itself.

        Downstream Derivations become STALE because their warrants
        remain historically well-formed but no longer have an active
        premise.
        """

        knowledge = self.get(
            identity,
            require_active=False,
        )

        if (
            knowledge.state
            is not KnowledgeState.RETRACTED
        ):
            self._items[
                identity
            ] = replace(
                knowledge,
                state=KnowledgeState.INVALID,
            )

        self._stale_dependents(
            identity
        )

    def retract(
        self,
        identity: str,
    ) -> None:
        """Explicitly withdraw one Knowledge item.

        Retraction changes the target to RETRACTED.

        Downstream Derivations become STALE rather than INVALID.
        """

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

        self._stale_dependents(
            identity
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
