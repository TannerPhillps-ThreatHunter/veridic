"""Assertion and Derivation epistemics.

FieldValue answers:

    What value is this?

KnownValue additionally answers:

    How does Veridic know it?

Two candidate root knowledge-producing acts are modeled:

    Assertion
        knowledge enters Veridic from outside the current derivation graph;

    Derivation
        knowledge is established from existing knowledge through an
        admitted semantic operation.

This layer intentionally sits above FieldValue.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import TypeAlias

from .execution import execute
from .field import FieldValue
from .runtime import SemanticRuntime
from .vocabulary import Operation


class KnowledgeError(RuntimeError):
    """Base error for epistemic computation."""


class DuplicateKnowledge(KnowledgeError):
    """A knowledge identifier already exists."""


class UnknownKnowledge(KnowledgeError):
    """A knowledge identifier does not exist."""


class InvalidKnowledge(KnowledgeError):
    """Knowledge cannot currently participate in derivation."""


class InvalidRevision(KnowledgeError):
    """A requested knowledge revision is not epistemically valid."""


class KnowledgeState(str, Enum):
    ACTIVE = "active"
    STALE = "stale"
    INVALID = "invalid"
    RETRACTED = "retracted"


@dataclass(frozen=True, slots=True)
class Provenance:
    """External origin information for an Assertion."""

    source: str
    method: str | None = None
    details: tuple[
        tuple[str, str],
        ...,
    ] = ()

    def __post_init__(self) -> None:
        if not self.source:
            raise ValueError(
                "Assertion provenance requires a source"
            )


@dataclass(frozen=True, slots=True)
class Assertion:
    """Knowledge introduced into Veridic."""

    provenance: Provenance


@dataclass(frozen=True, slots=True)
class Derivation:
    """Knowledge established from existing knowledge."""

    operation: Operation
    operands: tuple[str, ...]
    rule: str
    governing_laws: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.operands:
            raise ValueError(
                "Derivation requires at least one operand"
            )

        if not self.rule:
            raise ValueError(
                "Derivation requires its governing rule"
            )


KnowledgeOrigin: TypeAlias = (
    Assertion
    | Derivation
)


@dataclass(frozen=True, slots=True)
class KnownValue:
    """A semantically typed value with explicit epistemic origin."""

    identifier: str
    field_value: FieldValue
    origin: KnowledgeOrigin

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError(
                "Knowledge identifier cannot be empty"
            )

    @property
    def asserted(self) -> bool:
        return isinstance(
            self.origin,
            Assertion,
        )

    @property
    def derived(self) -> bool:
        return isinstance(
            self.origin,
            Derivation,
        )

    @property
    def field(self):
        return self.field_value.field

    @property
    def datum(self):
        return self.field_value.value


@dataclass(frozen=True, slots=True)
class Explanation:
    """Structured explanation of one KnownValue."""

    identifier: str
    classification: str
    datum: object
    unit: str | None
    origin: str
    provenance: Provenance | None = None
    operation: Operation | None = None
    rule: str | None = None
    governing_laws: tuple[str, ...] = ()
    dependencies: tuple[
        Explanation,
        ...,
    ] = ()


class KnowledgeStore:
    """Dependency-aware store of Assertions and Derivations."""

    def __init__(
        self,
        runtime: SemanticRuntime,
    ) -> None:
        self._runtime = runtime

        self._values: dict[
            str,
            KnownValue,
        ] = {}

        self._states: dict[
            str,
            KnowledgeState,
        ] = {}

        self._dependents: dict[
            str,
            set[str],
        ] = {}

    def __contains__(
        self,
        identifier: str,
    ) -> bool:
        return identifier in self._values

    def _require_unique(
        self,
        identifier: str,
    ) -> None:
        if identifier in self._values:
            raise DuplicateKnowledge(
                identifier
            )

    def _require_known(
        self,
        identifier: str,
    ) -> KnownValue:
        try:
            return self._values[
                identifier
            ]
        except KeyError as exc:
            raise UnknownKnowledge(
                identifier
            ) from exc

    def state(
        self,
        identifier: str,
    ) -> KnowledgeState:
        self._require_known(
            identifier
        )

        return self._states[
            identifier
        ]

    def get(
        self,
        identifier: str,
        *,
        require_active: bool = True,
    ) -> KnownValue:
        value = self._require_known(
            identifier
        )

        if (
            require_active
            and self.state(identifier)
            is not KnowledgeState.ACTIVE
        ):
            raise InvalidKnowledge(
                f"{identifier}: "
                f"{self.state(identifier).value}"
            )

        return value

    def assert_value(
        self,
        identifier: str,
        field_value: FieldValue,
        *,
        provenance: Provenance,
    ) -> KnownValue:
        self._require_unique(
            identifier
        )

        known = KnownValue(
            identifier=identifier,
            field_value=field_value,
            origin=Assertion(
                provenance=provenance
            ),
        )

        self._values[
            identifier
        ] = known

        self._states[
            identifier
        ] = KnowledgeState.ACTIVE

        self._dependents.setdefault(
            identifier,
            set(),
        )

        return known

    def derive(
        self,
        identifier: str,
        operation: Operation,
        *operand_ids: str,
    ) -> KnownValue:
        self._require_unique(
            identifier
        )

        operands = tuple(
            self.get(
                operand_id
            )
            for operand_id
            in operand_ids
        )

        result = execute(
            self._runtime,
            operation,
            *(
                operand.field_value
                for operand in operands
            ),
        )

        if result.output is None:
            raise KnowledgeError(
                "Derivation produced no semantic output Field"
            )

        output_field = replace(
            result.output.field,
            name=identifier,
        )

        field_value = FieldValue(
            field=output_field,
            value=result.output.value,
        )

        rule = result.admission.rule.name

        known = KnownValue(
            identifier=identifier,
            field_value=field_value,
            origin=Derivation(
                operation=operation,
                operands=tuple(
                    operand.identifier
                    for operand
                    in operands
                ),
                rule=rule,
                governing_laws=(
                    rule,
                ),
            ),
        )

        self._values[
            identifier
        ] = known

        self._states[
            identifier
        ] = KnowledgeState.ACTIVE

        self._dependents.setdefault(
            identifier,
            set(),
        )

        for operand in operands:
            self._dependents.setdefault(
                operand.identifier,
                set(),
            ).add(
                identifier
            )

        return known

    def direct_dependents(
        self,
        identifier: str,
    ) -> tuple[str, ...]:
        self._require_known(
            identifier
        )

        return tuple(
            sorted(
                self._dependents.get(
                    identifier,
                    set(),
                )
            )
        )

    def dependents(
        self,
        identifier: str,
    ) -> tuple[str, ...]:
        self._require_known(
            identifier
        )

        discovered: set[str] = set()
        pending = list(
            self._dependents.get(
                identifier,
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
        identifier: str,
    ) -> None:
        """Mark downstream derivations non-current without declaring
        their historical warrants invalid.
        """

        for dependent in self.dependents(
            identifier
        ):
            if (
                self._states[
                    dependent
                ]
                is KnowledgeState.ACTIVE
            ):
                self._states[
                    dependent
                ] = KnowledgeState.STALE

    def revise_assertion(
        self,
        identifier: str,
        field_value: FieldValue,
        *,
        provenance: Provenance,
    ) -> KnownValue:
        current = self._require_known(
            identifier
        )

        if not current.asserted:
            raise InvalidRevision(
                "Derived knowledge cannot be silently "
                "replaced as an Assertion"
            )

        self._stale_dependents(
            identifier
        )

        revised = KnownValue(
            identifier=identifier,
            field_value=field_value,
            origin=Assertion(
                provenance=provenance
            ),
        )

        self._values[
            identifier
        ] = revised

        self._states[
            identifier
        ] = KnowledgeState.ACTIVE

        return revised

    def retract(
        self,
        identifier: str,
    ) -> None:
        self._require_known(
            identifier
        )

        self._states[
            identifier
        ] = KnowledgeState.RETRACTED

        self._stale_dependents(
            identifier
        )

    def explain(
        self,
        identifier: str,
    ) -> Explanation:
        known = self._require_known(
            identifier
        )

        unit = (
            known.field.unit_symbol
            if known.field.unit is not None
            else None
        )

        if isinstance(
            known.origin,
            Assertion,
        ):
            return Explanation(
                identifier=identifier,
                classification=(
                    known.field.classification_path
                ),
                datum=known.datum,
                unit=unit,
                origin="asserted",
                provenance=(
                    known.origin.provenance
                ),
            )

        dependencies = tuple(
            self.explain(
                operand
            )
            for operand
            in known.origin.operands
        )

        return Explanation(
            identifier=identifier,
            classification=(
                known.field.classification_path
            ),
            datum=known.datum,
            unit=unit,
            origin="derived",
            operation=known.origin.operation,
            rule=known.origin.rule,
            governing_laws=(
                known.origin.governing_laws
            ),
            dependencies=dependencies,
        )


def format_explanation(
    explanation: Explanation,
    *,
    depth: int = 0,
) -> str:
    indent = "    " * depth

    unit = (
        f" {explanation.unit}"
        if explanation.unit
        else ""
    )

    lines = [
        (
            f"{indent}{explanation.identifier}"
            f" = {explanation.datum}{unit}"
            f" [{explanation.origin}]"
        )
    ]

    if explanation.provenance is not None:
        lines.append(
            f"{indent}source: "
            f"{explanation.provenance.source}"
        )

        if (
            explanation.provenance.method
            is not None
        ):
            lines.append(
                f"{indent}method: "
                f"{explanation.provenance.method}"
            )

    if explanation.operation is not None:
        lines.append(
            f"{indent}operation: "
            f"{explanation.operation.value}"
        )

    if explanation.rule is not None:
        lines.append(
            f"{indent}rule: "
            f"{explanation.rule}"
        )

    if explanation.dependencies:
        lines.append(
            f"{indent}derived from:"
        )

        for dependency in (
            explanation.dependencies
        ):
            lines.append(
                format_explanation(
                    dependency,
                    depth=depth + 1,
                )
            )

    return "\n".join(
        lines
    )


__all__ = [
    "Assertion",
    "Derivation",
    "DuplicateKnowledge",
    "Explanation",
    "InvalidKnowledge",
    "InvalidRevision",
    "KnowledgeError",
    "KnowledgeOrigin",
    "KnowledgeState",
    "KnowledgeStore",
    "KnownValue",
    "Provenance",
    "UnknownKnowledge",
    "format_explanation",
]
