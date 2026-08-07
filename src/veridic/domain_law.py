"""Domain-grounded semantic laws.

A DomainLaw represents behavior derived from the semantics of an
external problem domain rather than invented solely to exercise the
Field hierarchy.
"""

from __future__ import annotations

from dataclasses import dataclass

from .dimensions import SemanticDimension
from .operator import AdmissionRule, OperatorRule, TransferRule
from .vocabulary import Operation


@dataclass(frozen=True, slots=True)
class DomainLaw:
    """One domain-derived semantic operation law."""

    name: str
    domain: str
    statement: str
    operation: Operation
    arity: int
    depends_on: frozenset[SemanticDimension]
    admit: AdmissionRule
    transfer: TransferRule | None = None

    def as_operator_rule(self) -> OperatorRule:
        """Compile the domain law into the runtime rule form."""

        return OperatorRule(
            name=self.name,
            operation=self.operation,
            arity=self.arity,
            admit=self.admit,
            transfer=self.transfer,
            depends_on=self.depends_on,
        )
